import json
import scheduler

import utils
import interactions

#Obtain login token from hidden file
with open('.secret', 'r') as f:
    token = json.loads(f.read())['token']

#Init bot
bot = interactions.Client(token=token)

#API Connectivity Test Command
@bot.command(
        name="ping",
        description="test",
)
async def ping(ctx: interactions.CommandContext):
    await ctx.send("pong")

### Command: create ###
# Usage: /create event_name start_time [end_time]
#
# Creates an event in the calendar
#####
@bot.command(
        name="create",
        description="Create a new event object in the calendar",
        options = [
            interactions.Option(
                name = "name",
                description = "Name of the event",
                type = interactions.OptionType.STRING,
                required = True,
            ),
            interactions.Option(
                name = "start",
                description = "Datetime when the event begins",
                type = interactions.OptionType.STRING,
                required = True,
            ),
            interactions.Option(
                name = "end",
                description = "Datetime when the event ends. If none provided, event will run all day",
                type = interactions.OptionType.STRING,
                required = False,
            ),
        ],
        scope=680111789647855660,   #TEMP: prevent needing to wait for /command to register with API
)
async def newevent(ctx: interactions.CommandContext, name: str, start: str, end: str = None):
    try:
        sdt = await utils.parse_time(start)
        edt = await utils.parse_time(end) if end else None
    except Exception as e:
        await ctx.send(embeds=await utils.err_embed(f"Invalid time format"))
        return
    
    event_embed = await scheduler.request('create', [name, sdt, edt, ctx.author])
    await ctx.send(embeds=event_embed)

### Command: get ###
# Usage: /get [id|name|creator=search] [query=expression]
#
# Retreive event(s) in the calendar matching an ID, name, or creator value, or
# run an advanced query expression on the follwing properties:
# _id, name, start, end, author_id, author_name, created
#####
@bot.command(
        name="get",
        description="Get an existing event object in the calendar",
        options = [
            interactions.Option(
                name = "id",
                description = "ID of the event",
                type = interactions.OptionType.STRING,
                required = False,
            ),
            interactions.Option(
                name = "name",
                description = "Name of the event",
                type = interactions.OptionType.STRING,
                required = False,
            ),
            interactions.Option(
                name = "creator",
                description = "Events created by user (name or ID)",
                type = interactions.OptionType.STRING,
                required = False,
            ),
            interactions.Option(
                name = "query",
                description = "Comma-separated query on an event's properties",
                type = interactions.OptionType.STRING,
                required = False,
            ),
        ],
        scope=680111789647855660,   #TEMP: prevent needing to wait for /command to register with API
)
async def findevent(ctx: interactions.CommandContext, id: str = None, name: str = None, creator: str = None, query: str = None):
    if creator:
        #Resolve Discord user/id
        res = await ctx.guild.search_members(creator)
        if len(res)<1:
            err = await utils.err_embed(f"Could not find user {creator}")
            return await ctx.send(embeds=err)
        
        creator_id = int(res[0].user.id)

        embed = await scheduler.request('query', doc={'author_id': creator_id})
    elif id:
        embed = await scheduler.request('read', doc={"_id": id})
    elif name:
        embed = await scheduler.request('query', doc={"name": name})
    elif query:
        doc = await utils.strtoqry(query)
        embed = await scheduler.request('query', doc = doc)
    else:
        embed = await scheduler.request('query', doc={})
    await ctx.send(embeds=embed)

### Command: delete ###
# Usage: /delete id|name=value
#
# Delete a specific event associated with the user's account from the calendar
#####
@bot.command(
        name="delete",
        description="Delete an event from the calendar",
        options = [
            interactions.Option(
                name = "id",
                description = "ID of the event",
                type = interactions.OptionType.STRING,
                required = False,
            ),
            interactions.Option(
                name = "name",
                description = "Name of the event",
                type = interactions.OptionType.STRING,
                required = False,
            ),
        ],
        scope=680111789647855660,
)
async def deleteevent(ctx: interactions.CommandContext, id: str = None, name: str = None):
    if id:
        embed = await scheduler.request('delete', doc={'_id': id, 'author_id': int(ctx.author.id)})
    elif name:
        embed = await scheduler.request('delete', doc={'name': name, 'author_id': int(ctx.author.id)})
    else:
        embed = await utils.err_embed("Must provide an attribute of the event you want to delete")
    
    await ctx.send(embeds=embed)

@bot.event()
async def on_start():
    print("Bot started")

def start():
    bot.start()