from opsdroid.matchers import match_regex
import logging
import random

from .maps_connector import rank_alternative_routes


@match_regex(r'from (.*) to (.*)')
async def start(opsdroid, config, message):
    origin = message.regex.group(1)
    destination = message.regex.group(2)
    text = rank_alternative_routes(origin, destination)
    await message.respond(text)
