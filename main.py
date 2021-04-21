import discord
from discord.ext import commands
from googletrans import Translator
import random
import json

from cogs.translate import Translate

client = commands.Bot(command_prefix=commands.when_mentioned_or("?"), help_command=None)
translator = Translator()

with open("config.json", "r") as file:
    config = json.load(file)

client.add_cog(Translate(client))


@client.event
async def on_ready():
    game = discord.Game("?help")
    await client.change_presence(status=discord.Status.idle, activity=game)

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command(name='choice')
async def random_choice(ctx, *, arg):
    options = arg.split('|')

    if len(options) < 2:
        await ctx.send("need more options")
        return

    await ctx.send(random.choice(options))


@random_choice.error
async def random_choice_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("need more options")


client.run(config["token"])
