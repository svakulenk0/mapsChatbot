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

'''
import time
from heapq import heappush, heappop

import googlemaps

from .settings import API_KEY

MODES = {"driving": "car", "transit": "public transport", "bicycling": "bicycle"}


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

    def __init__(self):
        self.origin = None
        self.destination = None
        self.choice = None

    def rank_alternative_routes(self, origin, destination):
        '''
        Collects Google Maps routes API results for different transport options
        '''
        self.origin = origin
        self.destination = destination

        estimates = []
        for mode, transport in MODES.items():
            response = get_route(origin, destination, mode)
            if response:
                estimate = response[0]['legs'][0]['duration']
                # rank estimates
                heappush(estimates, (estimate['value'], (transport, estimate['text'])))
            else:
                return None

        route = "From: %s" % response[0]['legs'][0]['start_address'].split(',')[0]
        route += "\nTo: %s" % response[0]['legs'][0]['end_address'].split(',')[0]

        while estimates:
            time, (transport, time_str) = heappop(estimates)
            route += "\n%s %s" % (transport, time_str)
        return route

    def record_estimate(self, mode):
        response = get_route(self.origin, self.destination, mode)
        if response:
            # round up 1 minute
            now = time.time() + 60
            
            # save estimate
            if mode == 'transit':
                estimated_arrival = response[0]['legs'][0]['arrival_time']['value']
            else:
                # estimated trip duration: number of seconds
                estimated_duration = response[0]['legs'][0]['duration']['value']
                # calculate arrival time
                estimated_arrival = now + estimated_duration

            self.estimate = (mode, estimated_arrival, now)
            
            # format arrival time
            return time.strftime("%H:%M", time.localtime(estimated_arrival))

    def check_estimate(self):
        now = time.time()
        error = now - self.estimate[1]
        return error


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
