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
    estimate = tp.record_estimate('driving')
    await message.respond("You are going with a car arriving at %s" % estimate)


@match_regex(r'public transport|public|öffi|oeffi|offi|bim|ubahn|u-bahn|metro|bus|trolley', case_sensitive=False)
async def choose_public(opsdroid, config, message):
    estimate = tp.record_estimate('transit')
    await message.respond("You are going with a public transport arriving at %s" % estimate)


@match_regex(r'bike|bicycle|cycle|cycling', case_sensitive=False)
async def choose_bike(opsdroid, config, message):
    estimate = tp.record_estimate('bicycling')
    await message.respond("You are going by bike arriving at %s" % estimate)


# @match_regex(r'check|check in|ready|finish|fin|ok', case_sensitive=False)
#     async def finish(opsdroid, config, message):
#         await message.respond(text)
