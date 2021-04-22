import discord
import random
from discord.ext import commands

class Miscellaneous(commands.Cog, name='Miscellaneous'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='choice')
    async def random_choice(self, ctx, *, arg):
        """Gives you a random choice
        to choose ?choice options split by '|'
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
