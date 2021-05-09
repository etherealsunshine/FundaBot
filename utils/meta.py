import discord
from discord.ext import commands

embed_color = 0xBFEDDD

GIT_REPO = "https://github.com/shift-eleven/FundaBot"
LIB_REPO = "https://github.com/Rapptz/discord.py"
LIB_VERSION = discord.__version__

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