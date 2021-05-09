import discord
from discord.ext import commands, tasks
import json
import os, sys
import traceback
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from utils import chat_utils

# top level global variables
fundachannel_id = 834066741076295750
blackrose_id = 840618751648595978
embed_color = 0xBFEDDD

description = '''
A bot dedicated to helping the members of the Fundamics community
'''
intents = discord.Intents.all()


chatbot = ChatBot(
    "FundaBot",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance'
        }
    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
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


async def get_response(input):
    return chatbot.get_response(input)

with open("config.json", "r") as file:
    config = json.load(file)


client = commands.Bot(command_prefix="-", description=description,intents=intents)

class FundaHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)
    
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error,color=embed_color)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help",color=embed_color)
        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_command_signature(c) for c in filtered]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
        
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command),color=embed_color)
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
        
    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.qualified_name,description=cog.description,color=embed_color)
        commands = cog.get_commands()
        filtered = await self.filter_commands(commands, sort=True)
        embed.add_field(name='Commands', value="\n".join([c.name for c in filtered]))
        
        channel = self.get_destination()
        await channel.send(embed=embed)
        
        
client.help_command = FundaHelp()

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
    await message.channel.send(response)


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
