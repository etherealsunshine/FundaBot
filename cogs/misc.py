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
            
    @commands.command(name='flip')
    async def flip(self, ctx):
        flip_choices = ['heads', 'tails']
        await ctx.send(f"I choose: {random.choice(flip_choices)}")
        
    @commands.command(name='8ball', aliases=['eight-ball', 'eightball'])
    async def eight_ball(self, ctx, *, question):
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
        await ctx.send(f"Pong!, latency is {round(ctx.bot.latency * 1000)}ms")
            
def setup(bot):
    bot.add_cog(Miscellaneous(bot))