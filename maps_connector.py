#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jul 24, 2018

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Connects to Google Maps API via the offcial Python library

https://github.com/googlemaps/google-maps-services-python

'''
import googlemaps
from datetime import datetime
from heapq import heappush, heappop

from settings import API_KEY

MODES = {"driving": "car", "transit": "public transport", "bicycling": "bicycle"}


# connect to Google Maps API
gmaps = googlemaps.Client(key=API_KEY)


def get_route(origin, destination, mode):
    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode=mode)
                                         # departure_time=now)
    return directions_result


class TripPlanner(object):
    """Each object of the class holds information about the planned trip"""

    def __init__(self):
        self.origin = None
        self.destination = None
        self.estimates = {'bicycle': None, 'public transport': None,  'car': None}

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
                # store estimates
                self.estimates[transport] = estimate['text']
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
