import json
import scheduler

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
                name = "startdate",
                description = "Datetime when the event begins.",
                type = interactions.OptionType.STRING,
                required = True,
            ),
        ],
        scope=545410383339323403,
)
async def newevent(ctx: interactions.CommandContext, startdate: str):
    event_embed = await scheduler.request()
    await ctx.send(embeds=event_embed)


######## HELPER FUNCS ########

async def _err_embed(msg, example=None):
    emb = models.message.Embed(description=msg, color=models.misc.Color.dark_red())

    if example:
        emb.add_field(name='Example:', value=example)

    return emb

bot.start()