from opsdroid.matchers import match_regex
import logging
import random

from .maps_connector import TripPlanner

tp = TripPlanner()


# @match_always()
@match_regex(r'from (.*) to (.*)', case_sensitive=False)
async def start(opsdroid, config, message):
    origin = message.regex.group(1)
    destination = message.regex.group(2)
    text = tp.rank_alternative_routes(origin, destination)
    if text:
        await message.respond(text)
    else:
        await message.respond("Not sure what you mean. Could you be more specific?")


@match_regex(r'car|auto', case_sensitive=False)
    async def choose_car(opsdroid, config, message):
        mode = 'car'
        await message.respond("You are going with a car arriving in %s" tp.estimates[mode])


@match_regex(r'public transport|public|öffi|oeffi|offi|bim|ubahn|u-bahn|metro|bus|trolley', case_sensitive=False)
    async def choose_public(opsdroid, config, message):
        mode = 'public transport'
        await message.respond("You are going with a public transport arriving in %s" tp.estimates[mode])


@match_regex(r'bike|bicycle|cycle|cycling', case_sensitive=False)
    async def choose_bike(opsdroid, config, message):
        mode = 'bicycle'
        await message.respond("You are going by bike arriving in %s" tp.estimates[mode])


# @match_regex(r'check|check in|ready|finish|fin|ok', case_sensitive=False)
#     async def finish(opsdroid, config, message):
#         await message.respond(text)
