from opsdroid.matchers import match_regex
import logging
import random

from .maps_connector import rank_alternative_routes


# @match_always()
@match_regex(r'from (.*) to (.*)', case_sensitive=False)
async def start(opsdroid, config, message):
    origin = message.regex.group(1)
    destination = message.regex.group(2)
    text = rank_alternative_routes(origin, destination)
    if text:
        await message.respond(text)
    else:
        await message.respond("Not sure what you mean. Could you be more specific?")
