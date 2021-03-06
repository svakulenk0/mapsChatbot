#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jul 24, 2018

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Connects to Google Maps API via the offcial Python library

https://github.com/googlemaps/google-maps-services-python

Test API call: https://maps.googleapis.com/maps/api/directions/json?origin=WU+Wien&destination=Zoo+Schoenbrunn&mode=transit&key=x
Test API call: https://maps.googleapis.com/maps/api/directions/json?origin=WU+Wien&destination=Zoo+Schoenbrunn&mode=driving&key=x
Test API call: https://maps.googleapis.com/maps/api/directions/json?origin=WU+Wien&destination=Zoo+Schoenbrunn&mode=bicycling&key=x

Link to the map with the route on Google maps:
https://www.google.com/maps/dir/?api=1&origin=tu+wien&destination=wu+wien&travelmode=transit

'''
import time
from heapq import heappush, heappop

import googlemaps

from .settings import API_KEY

MODES = {"car": "driving", "offi": "transit", "bike": "bicycling"}
GM_LINK = "https://www.google.com/maps/dir/?api=1&origin=%s&destination=%s&travelmode=%s"


# connect to Google Maps API
gmaps = googlemaps.Client(key=API_KEY)


def get_route(origin, destination, mode):
    # Request directions via public transit
    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode=mode)
    return directions_result


class TripPlanner(object):
    """Each object of the class holds information about the planned trip"""

    def __init__(self, origin=None, destination=None):
        # plan route details
        self.origin = origin
        self.destination = destination
        # make transport choice
        self.transport = None
        # estimate prediction
        self.starting_time = None
        self.estimated_arrival = None
        # record observation
        self.actual_arrival = None
        self.error = None
        self.error_minutes = None
        self.error_sign = None

    def get_link(self):
        return GM_LINK % ('+'.join(self.origin.split()), '+'.join(self.destination.split()), MODES[self.transport])

    def rank_alternative_routes(self):
        '''
        Collects Google Maps routes API results for different transport options
        '''
        estimates = []
        for transport, mode in MODES.items():
            response = get_route(self.origin, self.destination, mode)
            if response:
                estimate = response[0]['legs'][0]['duration']
                # rank estimates
                heappush(estimates, (estimate['value'], (transport, estimate['text'])))
            else:
                return None

        route = "From: %s" % response[0]['legs'][0]['start_address'].split(',')[0]
        route += "\nTo: %s\n" % response[0]['legs'][0]['end_address'].split(',')[0]

        while estimates:
            time, (transport, time_str) = heappop(estimates)
            route += "\n%s %s" % (transport, time_str)
        return route

    def choose_transport(self, transport):
        self.transport = transport

    def format_time(self, timestamp):
        return time.strftime("%H:%M", time.localtime(timestamp))


    def record_estimate(self):
        mode = MODES[self.transport]
        if self.origin and self.destination:
            response = get_route(self.origin, self.destination, mode)
            if response:
                # round up 1 minute
                self.starting_time = time.time() + 60
                
                # save estimate
                if mode == 'transit':
                    self.estimated_arrival = response[0]['legs'][0]['arrival_time']['value']
                else:
                    # estimated trip duration: number of seconds
                    estimated_duration = response[0]['legs'][0]['duration']['value']
                    # calculate arrival time
                    self.estimated_arrival = self.starting_time + estimated_duration

                # format arrival time
                return self.format_time(self.estimated_arrival), self.transport
        return None, self.transport

    def check_estimate(self):
        if self.estimated_arrival:
            self.actual_arrival = time.time()
            self.error = self.actual_arrival - self.estimated_arrival
            if self.error > 0:
                self.error_minutes = int(self.error) / 60 % 60
                self.error_sign = 'late'
            elif self.error < 0:
                self.error_minutes = int(-self.error) / 60 % 60
                self.error_sign = 'early'
            else:
                self.error_minutes = 0
                self.error_sign = 'on time'
        return None


def test_rank_alternative_routes(origin='WU Wien', destination='Zoo Schoenbrunn'):
    '''
    Test for Google Maps routes API for different transport options
    '''
    print(rank_alternative_routes(origin, destination))


def test_none(origin='WU', destination='Zoo'):
    '''
    Unit test for empty result
    '''
    assert rank_alternative_routes(origin, destination) == None


if __name__ == '__main__':
    test_none()
    test_rank_alternative_routes()
