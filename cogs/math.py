import asyncio
from os import error
from discord.ext import commands

class Math(commands.Cog, name='Math'):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="calc")
    async def calc(self, ctx):
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        await ctx.send("Type something!")
        
        try:
            input = await self.bot.wait_for('message', timeout = 100.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send('You took too long!') 
        
        await ctx.send(input.clean_content)
        
            
    
def setup(bot):
    bot.add_cog(Math(bot))
