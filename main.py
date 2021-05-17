import chatterbot
import discord
from discord.ext import commands, tasks
import json
import os, sys
import traceback
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import chatterbot.response_selection
from utils import chat_utils, meta

# top level global variables
funda_id = 834066741076295750
blackrose_id = 840618751648595978

description = '''
A bot dedicated to helping the members of the Fundamics community
'''
intents = discord.Intents.all()

message_queue = []

chatbot = ChatBot(
    "FundaBot",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance',
        }
    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    filters=[
        'chatterbot.filters.get_recent_repeated_responses'
    ],
    input_adapter='chatterbot.input.VariableInputTypeAdapter',
    output_adapter="chatterbot.output.OutputAdapter",
    output_format="text",
)


trainer = ChatterBotCorpusTrainer(chatbot)
list_trainer = ListTrainer(chatbot)


trainer.train('chatterbot.corpus.english.')
list_trainer.train(chat_utils.base_data)
list_trainer.train(chat_utils.movie_data)
list_trainer.train(chat_utils.thing_data)
list_trainer.train(chat_utils.name_data)
list_trainer.train(chat_utils.gender_data)


async def get_response(input):
    return chatbot.get_response(input)

with open("config.json", "r") as file:
    config = json.load(file)


client = commands.Bot(command_prefix="-", description=description,intents=intents) 
client.help_command = meta.FundaHelp()

@client.listen('on_message')
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != blackrose_id:
        return
    if message.content == None:
        return
    query_string = message.content
    response = await get_response(query_string)
    await message.reply(response, mention_author=False)


@tasks.loop(minutes=1)
async def get_member_count():
    fundamics = client.get_guild(config["serverid"])
    count = len([s for s in fundamics.members if not s.bot])
    
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
async def on_disconnect():
    get_member_count.stop()
        

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
