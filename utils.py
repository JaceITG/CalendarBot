import interactions
import interactions.api.models as models

from datetime import datetime
from dateutil.parser import parse


async def parse_time(time):
    if time.lower() == "now":
        return datetime.now()
    
    return parse(time)

async def event_embed(event:dict, action:str = None):
    emb = models.Embed(title=action, description=f"{event['name']}\nStart time: {event['time']}")
    emb.set_footer(f"Event ID {event['_id']}")
    return emb

async def err_embed(msg, example=None):
    emb = models.message.Embed(description=msg, color=models.misc.Color.RED)

    if example:
        emb.add_field(name='Example:', value=example)

    return emb