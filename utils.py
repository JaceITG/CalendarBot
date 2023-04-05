import interactions
import interactions.api.models as models

from datetime import datetime, timedelta
from dateutil.parser import parse

async def parse_time(time):
    if time.lower() == "now":
        return datetime.now()
    
    return parse(time)

async def event_embed(event:dict, action:str = None):
    colors = {
        'New Event Created': models.misc.Color.GREEN,
        'Existing Event': models.misc.Color.WHITE,
    }

    emb = models.Embed(title=action, color=colors[action])

    emb.add_field(name="Event", value=event['name'])
    emb.add_field(name="Start Time", value=event['time'].strftime('%#m/%d/%Y %#I:%M%p'))
    
    if event['end']:
        #Construct duration string
        td = event['end'] - event['time']
        duration = f"{td.days} days " if td.days > 0 else ""
        duration += f"{td.seconds//3600} hr " if td.seconds//3600 > 0 else ""
        duration += f"{(td.seconds//60)%60} min " if (td.seconds//60)%60 > 0 else ""

        emb.add_field(name="End Time", value=f"{event['end'].strftime('%#m/%d/%Y %#I:%M%p')} ( Duration: {duration})")
    else:
        #All day event
        emb.add_field(name="End Time", value="All day")

    emb.add_field(name="Creator", value=f"{event['author_name']} (ID: {event['author_id']})")
    
    emb.set_footer(f"Event ID {event['_id']}")
    return emb

async def query_embed(cursor, q:dict = None):
    emb = models.Embed(title="Results", description=f"Query: `{str(q)}`", color=models.misc.Color.WHITE)
    
    for e in cursor:
        time_str = e['time'].strftime('%#m/%d/%Y %#I:%M%p')
        if e['end']:
            time_str += " -\n" + e['end'].strftime('%#m/%d/%Y %#I:%M%p')

        emb.add_field(name=e['name'], value=f"{time_str}\nID: {e['_id']}", inline=True)
        emb.add_field(name=" ", value=f"👤 {e['author_name']}", inline=True)

        emb.add_field(name=" ",value=" ", inline=False)
    
    return emb

async def err_embed(msg, example=None):
    emb = models.message.Embed(description=msg, color=models.misc.Color.RED)

    if example:
        emb.add_field(name='Example:', value=example)

    return emb