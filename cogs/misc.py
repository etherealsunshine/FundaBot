import discord
import random
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class Miscellaneous(commands.Cog, name='Miscellaneous'):
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
        
    
    @commands.command(name='say')
    async def say(self, ctx, *, echo_message):
        await ctx.send(f'{ctx.author.mention}, {echo_message}')
        
    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("need something to echo")
            
            
    @commands.command(name='poke')
    @commands.cooldown(1, 60, BucketType.member)
    async def poke(self, ctx, poke_member: discord.Member):
        await ctx.send(f"{ctx.author.display_name} pokes {poke_member.mention}")
        
    @poke.error
    async def poke_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Couldnt find that member')
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"You're on cooldown, retry after {round(error.retry_after)} seconds")
            
def setup(bot):
    bot.add_cog(Miscellaneous(bot))