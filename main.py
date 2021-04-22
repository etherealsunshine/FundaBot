import discord
from discord.ext import commands
import json

from cogs import translate, misc

description = '''
A bot dedicated to helping the members of the fundamics community
'''

with open("config.json", "r") as file:
    config = json.load(file)

client = commands.Bot(command_prefix=commands.when_mentioned_or("-"), description=description)

client.add_cog(translate.Translate(client))
client.add_cog(misc.Miscellaneous(client))

# on ready event, set status here
@client.event
async def on_ready():
    game = discord.Game("-help")
    await client.change_presence(status=discord.Status.idle, activity=game)

    print('Logged in as')
    print(client.user.name + client.user.discriminator)
    print('------')


client.run(config["token"])
