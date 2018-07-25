from opsdroid.matchers import match_always
import logging
import random

from .maps_connector import rank_alternative_routes


@match_always()
@match_regex(r'from (.*) to (.*)', case_sensitive=False)
async def start(opsdroid, config, message):
    origin = message.regex.group(1)
    destination = message.regex.group(2)
    text = rank_alternative_routes(origin, destination)
    await message.respond(text)
