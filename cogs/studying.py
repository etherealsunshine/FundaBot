from discord.ext import commands
import discord
from itertools import zip_longest

class Studying(commands.Cog):
    """Check who all is studying"""
    def __init__(self, bot):
        self.bot = bot
        
    def create_groups(iterable, n):
        args = [iter(iterable)] * n
        return zip_longest(*args)
        
    @commands.command(name='available')
    async def is_available(self, ctx):
        """Allows you to see who all is currently studying"""
        studying_role = ctx.guild.get_role(834800433046224937)
        members = studying_role.members
        user_msg = ""
        for m in members:
            user_msg += f"\n{m.mention}"
        embed = discord.Embed(title='Studying members', color=0xBFEDDD, description=user_msg)
        await ctx.send(embed=embed)
        
    @commands.command(name='studying')
    async def is_studying(self, ctx : commands.Context):
        """Mark yourself as studying
        Allows you to access the studying voice channels
        Call the command again to remove the studying role"""
        studying_role = ctx.guild.get_role(834800433046224937)
        if studying_role in ctx.author.roles:
            await ctx.author.remove_roles(studying_role)
            return await ctx.message.reply("You are no longer studying!", mention_author=False)
        
        await ctx.author.add_roles(studying_role)
        await ctx.message.reply("You are now studying!", mention_author=False)
                    
        
        
        
    
def setup(bot):
    bot.add_cog(Studying(bot))
