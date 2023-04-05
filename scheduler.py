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
        "author_id": user['_id'],
        "author_name": user['name']
    }
    event_id = db.events.insert_one(event).inserted_id
    event = db.events.find_one({"_id": event_id})

    return await utils.event_embed(event, "New Event Created")

async def _read_one(q: dict = None):
    if q:
        #convert id queries
        if "_id" in q.keys():
            q["_id"] = ObjectId(q["_id"])

        #Get indexed event
        event = db.events.find_one(q)
    else:
        #Get a random event
        event = db.events.find_one()
    
    if not event:
        return await utils.err_embed("Could not find event")
    
    creator = await _get_user(event['author_id'])
    return await utils.event_embed(event, creator, "Existing Event")

async def _query(q: dict):
    cursor = db.events.find(q)
    if not cursor:
        return await utils.err_embed("Could not find events")

    return await utils.query_embed(cursor, q=q)

async def _delete(q: dict):
    deleted = db.events.delete_one(q)

    if deleted.deleted_count < 1:
        return utils.err_embed(f"Could not find event to delete matching query:\n`{q}`")
    
    return Embed(description=f"Event deleted successfully\nQuery: `{q}`")


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

async def request(action, args: list = None, doc: dict = None):
    if action == 'create':
        return await _create(*args)
    elif action == 'read':
        return await _read_one(doc)
    elif action == 'update':
        return None
    elif action == 'delete':
        return await _delete(doc)
    elif action == 'read_user':
        return await _get_user(*args)
    elif action == 'query':
        return await _query(doc)
    