import asyncio
import re
import discord
import random
import aiohttp
import json
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from utils import misc, formatter

class Miscellaneous(commands.Cog, name='Miscellaneous'):
    """A bunch of miscellaneous commands for fun"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='choice')
    async def random_choice(self, ctx, *, arg):
        """Gives you a random choice
        To choose: ?choice options split by '|'
        ex. ?choice hey|hello"""
        options = arg.split('|')

        if len(options) < 2:
            await ctx.send("need more options")
            return

        await ctx.send(random.choice(options))


    @random_choice.error
    async def random_choice_error(self, ctx, error):
     if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("need more options")
        
    
    @commands.command(name='say', aliases = ['echo', 'repeat'])
    async def say(self, ctx, *, echo_message):
        """repeats whatever you say"""
        await ctx.send(f'{echo_message}')
        
    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("need something to echo")
            
    @commands.command(name='flip')
    async def flip(self, ctx):
        """Do a coin flip"""
        flip_choices = ['heads', 'tails']
        await ctx.send(f"I choose: {random.choice(flip_choices)}")
        
    @commands.command(name='8ball', aliases=['eight-ball', 'eightball'])
    async def eight_ball(self, ctx, *, question):
        """Consult the magic Eight Ball
        Usage: -8ball your question
        """
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        
        await ctx.send(random.choice(responses))
        
    @commands.command(name='ping', aliases=['pong'])
    async def ping(self, ctx):
        """Play a game of ping pong
        Use this to check if the bot is alive
        Also provides latency"""
        await ctx.send(f"Pong!, latency is {round(ctx.bot.latency * 1000)}ms")
        
    @commands.command(name='trivia')
    async def trivia(self, ctx):
        """Answer a randomly selected trivia question
        FundaBot gets a question and you have to type out the answer
        """
        await ctx.send('Im getting a question for you, please be patient')
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        async with aiohttp.ClientSession() as session:
            async with session.get('https://jservice.io/api/random') as resp:
                trivia_questions = await resp.json()
                trivia_question = trivia_questions[0]
                question = trivia_question['question']
                answer = trivia_question['answer']
                clean_answer = misc.strip_tags(answer)
                
                await ctx.send(f"Alright here's your question, {question}\nType out your answer!")
                
                try:
                    input = await self.bot.wait_for('message', timeout = 60.0, check = check)
                except asyncio.TimeoutError:
                    return await ctx.send('You took too long!')
                
                if input.content.lower() == clean_answer.lower():
                    return await ctx.send("Correct answer!")
                else:
                    return await ctx.send(f"Incorrect answer, the right answer was: {clean_answer}")
                
    @commands.command(name='fundachannelsort', hidden=True)
    @commands.is_owner()
    async def fundachannelsort(self, ctx):
        fundamics = self.bot.get_guild(815595847135395880)
        groups = fundamics.get_channel(815952796883877928)
        channels = []
        for channel in groups.text_channels:
            channels.append(channel.name)
        
        channels.sort()
        output = formatter.quote_list(channels)
        await ctx.send(output)
        
    @fundachannelsort.error
    async def sorter_error(self, ctx, error):
        if isinstance(error, commands.errors.NotOwner):
            await ctx.send("You're not shift-eleven#7304")
            
    @commands.command(name='poll')
    async def poll(self, ctx, *, question):
        await ctx.message.delete()
        poll_message = await ctx.send(question)
        await poll_message.add_reaction("👍")
        await poll_message.add_reaction("👎")
        
    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Need a poll question")
        
                           
def setup(bot):
    bot.add_cog(Miscellaneous(bot))
