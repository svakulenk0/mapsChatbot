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

from .settings import API_KEY

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


def rank_alternative_routes(origin, destination):
    estimates = []
    for mode, transport in MODES.items():
        response = get_route(origin, destination, mode)
        
        estimate = response[0]['legs'][0]['duration']
        heappush(estimates, (estimate['value'], (transport, estimate['text'])))

    route = "From: %s" % response[0]['legs'][0]['start_address'].split(',')[0]
    route += "\nTo: %s" % response[0]['legs'][0]['end_address'].split(',')[0]

    while estimates:
        time, (transport, time_str) = heappop(estimates)
        route += "\n%s %s" % (transport, time_str)
    return route


def test_get_route(origin='WU Wien', destination='Zoo Schoenbrunn'):
    '''
    Unit test for Google Maps routes API for different transport options
    '''
    print(rank_alternative_routes(origin, destination))


if __name__ == '__main__':
    test_get_route()
