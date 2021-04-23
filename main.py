import discord
from discord.ext import commands, tasks
import json

from cogs import translate, misc

description = '''
A bot dedicated to helping the members of the Fundamics community
'''

intents = discord.Intents.default()
intents.members = True

with open("config.json", "r") as file:
    config = json.load(file)

client = commands.Bot(command_prefix=commands.when_mentioned_or("-"), description=description,intents=intents)

client.add_cog(translate.Translate(client))
client.add_cog(misc.Miscellaneous(client))

@tasks.loop(minutes=1)
async def get_member_count():
    fundamics = client.get_guild(config["serverid"])
    count = len([s for s in fundamics.members if s.bot != True])
    
    game = discord.Game(f"-help | Watching {count} members")
    await client.change_presence(status=discord.Status.idle, activity=game)
    

@client.event
async def on_ready():
    get_member_count.start()

    print('Logged in as')
    print(client.user.name + "#" + client.user.discriminator)
    print('------')


client.run(config["token"])
