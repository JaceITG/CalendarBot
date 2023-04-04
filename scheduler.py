from pymongo import MongoClient
from bson.objectid import ObjectId

from interactions.api.models.message import Embed
from interactions.api.models.user import User
import utils
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client.calendar

async def _create(name: str, sdt: datetime, edt: datetime, author: User):
    user = await _get_user(int(author.id))
    if not user:
        user = await _create_user(author)
    
    event = {
        "name": name,
        "time": sdt,
        "end": edt,
        "author_id": user['_id']
    }
    event_id = db.events.insert_one(event).inserted_id
    event = db.events.find_one({"_id": event_id})

    creator = await _get_user(event['author_id'])
    return await utils.event_embed(event, creator, "New Event Created")

async def _read(id: str = None):
    if id:
        #Get indexed event
        event = db.events.find_one({"_id": ObjectId(id)})
    else:
        #Get a random event
        event = db.events.find_one()
    
    if not event:
        return await utils.err_embed("Could not find event")
    
    creator = await _get_user(event['author_id'])
    return await utils.event_embed(event, creator, "Existing Event")

async def _get_user(id: int):
    user = db.users.find_one({'_id': id})
    return user

async def _create_user(discord_user: User):
    user = {
        "_id": int(discord_user.id),
        "name": discord_user.username
    }
    user_id = db.users.insert_one(user)
    return db.users.find_one({'_id':user_id})

async def request(action, args: list = None):
    if action == 'create':
        return await _create(*args)
    elif action == 'read':
        return await _read(*args)
    elif action == 'update':
        return None
    elif action == 'delete':
        return None
    elif action == 'read_user':
        return await _get_user(*args)
    