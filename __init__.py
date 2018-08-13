from opsdroid.matchers import match_regex, match_always
# import DatabaseMongo
import logging
import random

from .maps_connector import TripPlanner

AGENT_ID = 'google_maps'
INSTRUCTION = '1) Define the route, e.g. "from zoo schoenbrunn to wu wien"\n2) Choose transportation option: "car", "offi" or "bike"\n3) Say "check" when you arrive at the destination'
# connect to the DB
# db = DatabaseMongo()

def setup(opsdroid):
    opsdroid.tp = TripPlanner()


def estimate(opsdroid, mode):
    estimate = opsdroid.tp.record_estimate(mode)
    response = "You are going by %s estimated arrival time %s" % (mode, estimate)
    if opsdroid.previous_error:
        response += "\nLast time the error was %s" % opsdroid.previous_error
    return response

@match_regex(r'from (.*) to (.*)', case_sensitive=False)
async def start(opsdroid, config, message):
    '''
    sample request: From tu wien to Schönbrunn
    '''
    origin = message.regex.group(1)
    destination = message.regex.group(2)
    # restart estimates for the new route
    opsdroid.tp = TripPlanner(origin, destination)

    # load error estimate from the previous history
    opsdroid.previous_error = await opsdroid.memory.get(AGENT_ID)

    text = opsdroid.tp.rank_alternative_routes()
    if text:
        await message.respond(text)
    else:
        await message.respond("Not sure what you mean. Could you be more specific?")


@match_regex(r'car|auto', case_sensitive=False)
async def choose_car(opsdroid, config, message):
    response = estimate(opsdroid, 'car')
    await message.respond(response)


@match_regex(r'public transport|public|öffi|oeffi|offi|bim|ubahn|u-bahn|metro|bus|trolley', case_sensitive=False)
async def choose_public(opsdroid, config, message):
    response = estimate(opsdroid, 'public transport')
    await message.respond(response)


@match_regex(r'bike|bicycle|cycle|cycling', case_sensitive=False)
async def choose_bike(opsdroid, config, message):
    response = estimate(opsdroid, 'bike')
    await message.respond(response)


@match_regex(r'check|check in|ready|finish|fin|ok|here', case_sensitive=False)
async def finish(opsdroid, config, message):
    '''
    calculates difference between the estimated and actual arrival time
    '''
    error = opsdroid.tp.check_estimate()
    if error > 0:
        minutes = int(error) / 60 % 60
        await message.respond("You are %d minutes late" % minutes)
    elif error < 0:
        minutes = int(-error) / 60 % 60
        await message.respond("You are %d minutes early" % minutes)
    else:
        await message.respond("You are just on time!")


@match_regex(r'save|speichern', case_sensitive=False)
async def save_to_DB(opsdroid, config, message):
    '''
    save the user_id, route details (origin/destination/transport) and error to DB, e.g. through the mongo connector
    '''
    if opsdroid.tp.error:
        # api_error = (opsdroid.tp.origin, opsdroid.tp.destination, opsdroid.tp.mode, opsdroid.tp.timestamp, opsdroid.tp.error)
        api_error = opsdroid.tp.error
        await opsdroid.memory.put(AGENT_ID, api_error)
        # db.put(key, api_error)
        await message.respond("Saved " + opsdroid.tp.origin)


@match_regex(r'help', case_sensitive=False)
async def help(opsdroid, config, message):
    match = True
    await message.respond(INSTRUCTION)


# @match_regex(r'car|auto', case_sensitive=False)
# async def choose_car(opsdroid, config, message):
#     '''
#     quick command to run all tests
#     '''
#     response = estimate(opsdroid, 'car')
#     await message.respond(response)


# @match_always()
# async def unknown_command(opsdroid, config, message):
#     '''
#     default response if the utterance did not match any of the regex commands defined above
#     '''
#     if not match:
#         await message.respond("Not sure what you mean!\n" + INSTRUCTION)
