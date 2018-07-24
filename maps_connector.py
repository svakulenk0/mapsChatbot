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

from settings import API_KEY


# connect to Google Maps API
gmaps = googlemaps.Client(key=API_KEY)


def get_route(origin, destination):
    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions("Sydney Town Hall",
                                         "Parramatta, NSW",
                                         mode="transit",
                                         departure_time=now)
    return directions_result


def test_get_route(origin='WU Wien', destination='Zoo Schoenbrunn'):
    print get_route(origin, destination)


if __name__ == '__main__':
    test_get_route()
