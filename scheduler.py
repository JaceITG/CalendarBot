from pymongo import MongoClient
from bson.objectid import ObjectId

from interactions.api.models.message import Embed
import utils
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client.calendar

async def _create(name: str, dt: datetime):
    event = {
        "name": name,
        "time": dt
    }
    event_id = db.events.insert_one(event).inserted_id
    event = db.events.find_one({"_id": event_id})

    return await utils.event_embed(event, "New Event Created")

async def _read(id: str = None):
    if id:
        #Get indexed event
        event = db.events.find_one({"_id": ObjectId(id)})
    else:
        #Get a random event
        event = db.events.find_one()
    
    if not event:
        return await utils.err_embed("Could not find event")
    
    return await utils.event_embed(event, "Existing Event")

async def request(type, args: list = None):
    if type == 'create':
        return await _create(*args)
    elif type == 'read':
        return await _read(*args)
    