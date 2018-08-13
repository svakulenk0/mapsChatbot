from opsdroid.matchers import match_regex, match_always
import logging
import random

from .maps_connector import TripPlanner


INSTRUCTION = '1) Define the route, e.g. "from karlsplatz to rathausplatz"\n2) Choose transportation option: "car", "offi" or "bike"\n3) Say "check" when you arrive at the destination'

tp = TripPlanner()
match = False


@match_regex(r'from (.*) to (.*)', case_sensitive=False)
async def start(opsdroid, config, message):
    '''
    sample request: From tu wien to Schönbrunn
    '''
    match = True
    origin = message.regex.group(1)
    destination = message.regex.group(2)
    text = tp.rank_alternative_routes(origin, destination)
    if text:
        await message.respond(text)
    else:
        await message.respond("Not sure what you mean. Could you be more specific?")


@match_regex(r'car|auto', case_sensitive=False)
async def choose_car(opsdroid, config, message):
    match = True
    estimate = tp.record_estimate('driving')
    await message.respond("You are going with a car estimated arrival time %s" % estimate)


@match_regex(r'public transport|public|öffi|oeffi|offi|bim|ubahn|u-bahn|metro|bus|trolley', case_sensitive=False)
async def choose_public(opsdroid, config, message):
    match = True
    estimate = tp.record_estimate('transit')
    await message.respond("You are going with a public transport estimated arrival time %s" % estimate)


@match_regex(r'bike|bicycle|cycle|cycling', case_sensitive=False)
async def choose_bike(opsdroid, config, message):
    match = True
    estimate = tp.record_estimate('bicycling')
    await message.respond("You are going by bike estimated arrival time %s" % estimate)


@match_regex(r'check|check in|ready|finish|fin|ok|here', case_sensitive=False)
async def finish(opsdroid, config, message):
    '''
    calculates difference between the estimated and actual arrival time
    '''
    match = True
    error = tp.check_estimate()
    if error > 0:
        minutes = int(error) / 60 % 60
        await message.respond("You are %d minutes late" % minutes)
    elif error < 0:
        minutes = int(-error) / 60 % 60
        await message.respond("You are %d minutes early" % minutes)
    else:
        await message.respond("You are just on time!")


@match_regex(r'help', case_sensitive=False)
async def help(opsdroid, config, message):
    match = True
    await message.respond(INSTRUCTION)


@match_always()
async def unknown_command(opsdroid, config, message):
    '''
    default response if the utterance did not match any of the regex commands defined above
    '''
    if not match:
        await message.respond("Not sure what you mean!\n" + INSTRUCTION)
