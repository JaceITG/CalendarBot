import json
import scheduler

import utils

import interactions
import interactions.api.models as models

with open('.secret', 'r') as f:
    token = json.loads(f.read())['token']

bot = interactions.Client(token=token)

@bot.command(
        name="ping",
        description="test",
)
async def ping(ctx: interactions.CommandContext):
    await ctx.send("pong")

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
        scope=545410383339323403,   #TEMP: prevent needing to wait for /command to register with API
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
        ],
        scope=545410383339323403,   #TEMP: prevent needing to wait for /command to register with API
)
async def findevent(ctx: interactions.CommandContext, id: str = None, name: str = None, creator: str = None):
    if creator:
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
    await ctx.send(embeds=embed)

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
        ]
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