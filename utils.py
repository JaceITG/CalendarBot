import interactions
import interactions.api.models as models

from datetime import datetime, timedelta
from dateutil.parser import parse

async def parse_time(time):
    if time.lower() == "now":
        return datetime.now()
    
    return parse(time)

#Embed representation of event document
async def event_embed(event:dict, action:str = None):
    colors = {
        'New Event Created': models.misc.Color.GREEN,
        'Existing Event': models.misc.Color.WHITE,
    }

    emb = models.Embed(title=action, color=colors[action])

    emb.add_field(name="Event", value=event['name'])
    emb.add_field(name="Start Time", value=event['start'].strftime('%#m/%d/%Y %#I:%M%p'))
    
    if event['end']:
        #Construct duration string
        td = event['end'] - event['start']
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

#Embed representation of multiple event documents
async def query_embed(cursor, q:dict = None):
    emb = models.Embed(title="Results", description=f"Query: `{str(q)}`", color=models.misc.Color.WHITE)
    
    num_events = 0
    for e in cursor:
        if num_events >= 5:
            num_events += 1
            continue

        time_str = e['start'].strftime('%#m/%d/%Y %#I:%M%p')
        if e['end']:
            time_str += " -\n" + e['end'].strftime('%#m/%d/%Y %#I:%M%p')

        emb.add_field(name=e['name'], value=f"{time_str}\nID: {e['_id']}", inline=True)
        emb.add_field(name=" ", value=f"👤 {e['author_name']}", inline=True)

        emb.add_field(name=" ",value=" ", inline=False)

        num_events += 1
    
    emb.set_footer(f"Showing {5 if num_events>=5 else num_events} of {num_events} events. {'Refine search query to see more results' if num_events>=5 else ''}")
    
    return emb

#Format a string expression into a query document
async def strtoqry(q):
    doc = {}

    terms = [t.strip() for t in q.split(',')]

    operators = {
        ' before ':'lt',
        ' after ':'gt',
        ' in ':'regex',
        '>=':'gte',
        '<=':'lte',
        '==':'eq',
        '!=':'ne',
        '<':'lt',
        '>':'gt',
        '=':'eq'
    }

    fields = ["name", "start", "end", "author_id", "author_name", "created"]

    for t in terms:
        for o in operators.keys():
            if o in t:
                #Separate operands
                tokens = [token.strip() for token in t.split(o)]

                if len(tokens) != 2:
                    return await err_embed(f"Malformed operator expression: {t}")
                
                #Determine whether left or right operand is the property specifier
                if tokens[0] in fields:
                    prop = tokens[0]
                    value = tokens[1]
                elif tokens[1] in fields:
                    prop = tokens[1]
                    value = tokens[0]
                else:
                    return await err_embed(f"Invalid query property in {' '.join(tokens)}")
                
                if prop in ["start", "end", "created"]:
                    #parse value as datetime
                    try:
                        value = await parse_time(value)
                    except Exception as e:
                        return await err_embed(f"Invalid time format")

                doc[prop] = {f"${operators[o]}": value}

                if operators[o] == "regex":
                    #add case-insensitivity
                    doc[prop]['$options'] = 'i'
                
                break
    return doc

async def err_embed(msg, example=None):
    emb = models.message.Embed(description=msg, color=models.misc.Color.RED)

    if example:
        emb.add_field(name='Example:', value=example)

    return emb