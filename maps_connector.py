#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jul 24, 2018

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Connects to Google Maps API
https://cloud.google.com/maps-platform/routes/
https://developers.google.com/maps/documentation/directions/start

'''
# URL = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&key=%s"
URL = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&key=%s"

def get_route(origin='WU Wien', destination='Zoo Schoenbrunn'):
