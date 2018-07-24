from opsdroid.matchers import match_regex
import logging
import random

from .maps_connector import rank_alternative_routes


@match_regex(r'(.*)')
async def start(opsdroid, config, message):
    request = message.regex.group(1)
    
    origin='WU Wien'
    destination='Zoo Schoenbrunn'
    
    text = rank_alternative_routes(origin, destination)
    await message.respond(text)
