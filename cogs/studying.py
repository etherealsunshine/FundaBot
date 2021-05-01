from discord.ext import commands
import discord

class Studying(commands.Cog):
    """Check who all is studying"""
    def __init__(self, bot):
        self.bot = bot
        
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
    
def setup(bot):
    bot.add_cog(Studying(bot))
