import json
import scheduler

import utils

import interactions
import interactions.api.models as models

with open('.secret', 'r') as f:
    token = json.loads(f.read())['token']

bot = interactions.Client(token=token)

@bot.event()
async def on_start():
    print("Bot started")

@bot.command(
        name="ping",
        description="test",
)
async def ping(ctx: interactions.CommandContext):
    await ctx.send("pong")

@bot.command(
        name="newevent",
        description="Create a new event object in the calendar.",
        options = [
            interactions.Option(
                name = "name",
                description = "Name of the event",
                type = interactions.OptionType.STRING,
                required = True,
            ),
            interactions.Option(
                name = "startdate",
                description = "Datetime when the event begins",
                type = interactions.OptionType.STRING,
                required = True,
            ),
        ],
        scope=545410383339323403,
)
async def newevent(ctx: interactions.CommandContext, name: str, startdate: str):
    try:
        dt = await utils.parse_time(startdate)
    except Exception as e:
        await ctx.send(embeds=utils.err_embed(f"Invalid time format: {startdate}"))
        return
    
    event_embed = await scheduler.request('create', [name, dt])
    await ctx.send(embeds=event_embed)

@bot.command(
        name="findevent",
        description="Find an existing event object in the calendar.",
        options = [
            interactions.Option(
                name = "id",
                description = "ID of the event",
                type = interactions.OptionType.STRING,
                required = False,
            ),
        ],
        scope=545410383339323403,
)
async def findevent(ctx: interactions.CommandContext, id: str = None):
    event_embed = await scheduler.request('read', [id])
    await ctx.send(embeds=event_embed)


def start():
    bot.start()