import pymongo
from interactions.api.models.message import Embed

async def request():
    return Embed(title="New Event")