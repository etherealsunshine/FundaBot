import discord
from discord.ext import commands
from googletrans import Translator


class Translate(commands.Cog, name='Translate'):
    def __init__(self, bot):
        self.bot = bot
        self._translator = Translator()

    @commands.command(name='translate')
    async def translate(self, ctx, *, arg):
        output = self._translator.translate(arg)
        embed = discord.Embed(title='Translated', color=0xBFEDDD)
        embed.add_field(name=f'From {output.src}', value=output.origin, inline=False)
        embed.add_field(name=f'To {output.dest}', value=output.text, inline=False)
        await ctx.send(embed=embed)

    @translate.error
    async def translate_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("need something to translate")
