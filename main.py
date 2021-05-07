import discord
from discord.ext import commands, tasks
import json
import os, sys
import traceback

description = '''
A bot dedicated to helping the members of the Fundamics community
'''
intents = discord.Intents.all()

with open("config.json", "r") as file:
    config = json.load(file)

client = commands.Bot(command_prefix=commands.when_mentioned_or("-"), description=description,intents=intents)

@tasks.loop(minutes=1)
async def get_member_count():
    fundamics = client.get_guild(config["serverid"])
    count = len([s for s in fundamics.members if s.bot != True])
    
    game = discord.Game(f"-help | Watching {count} members")
    await client.change_presence(status=discord.Status.idle, activity=game)
    

@client.event
async def on_ready():
    get_member_count.start()
    
    print('---------------------------------------------------------------------------\n')
    print(f'Logged in as : {client.user.display_name}#{client.user.discriminator} ({client.user.id})')
    print(f'Connected to : {len(client.guilds)} guilds\n')
    print('---------------------------------------------------------------------------\n')
            
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
    else:
        print(f'Unable to load {filename[:-3]}')        
        

@client.event
async def on_command_error(ctx, exception):
    if isinstance(exception, commands.NoPrivateMessage):
        await ctx.author.send('This command cannot be used in private messages.')
    elif isinstance(exception, commands.DisabledCommand):
        await ctx.author.send('Sorry. This command is disabled and cannot be used.')
    elif isinstance(exception, commands.CommandInvokeError):
        original = exception.original
        if not isinstance(original, discord.HTTPException):
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(original.__traceback__)
            print(f'{original.__class__.__name__}: {original}', file=sys.stderr)
        elif isinstance(exception, commands.ArgumentParsingError):
            await ctx.send(exception)
    elif isinstance(exception, commands.errors.CommandOnCooldown):
        await ctx.send(f"You're on cooldown, you can try again in {round(exception.retry_after)}")
    else:
        print(exception, file=sys.stderr)


client.run(config["token"])
