import interactions
import interactions.api.models as models

from datetime import datetime, timedelta
from dateutil.parser import parse

async def parse_time(time):
    if time.lower() == "now":
        return datetime.now()
    
    return parse(time)

async def event_embed(event:dict, creator: dict, action:str = None):
    colors = {
        'New Event Created': models.misc.Color.GREEN,
        'Existing Event': models.misc.Color.WHITE,
    }

    emb = models.Embed(title=action, color=colors[action])

    emb.add_field(name="Event", value=event['name'])
    emb.add_field(name="Start Time", value=event['time'].strftime('%#m/%d/%Y %#I:%M%p'))
    
    if event['end']:
        #Construct duration string
        td = event['time'] - event['end']
        duration = f"{td.days} days " if td.days > 0 else ""
        duration += f"{td.seconds//3600} hr " if td.seconds//3600 > 0 else ""
        duration += f"{(td.seconds//60)%60} min " if (td.seconds//60)%60 > 0 else ""

        emb.add_field(name="End Time", value=f"{event['end'].strftime('%#m/%d/%Y %#I:%M%p')} ( Duration: {duration})")
    else:
        #All day event
        emb.add_field(name="End Time", value="All day")

    emb.add_field(name="Creator", value=f"{creator['name']} (ID: {creator['_id']})")
    
    emb.set_footer(f"Event ID {event['_id']}")
    return emb

async def err_embed(msg, example=None):
    emb = models.message.Embed(description=msg, color=models.misc.Color.RED)

    if example:
        emb.add_field(name='Example:', value=example)

    return emb