import discord
from discord.ext import commands
from googletrans import Translator
from utils import misc, formatter


class Translate(commands.Cog, name='Translate'):
    """Translation related commands"""
    def __init__(self, bot):
        self.bot = bot
        self._translator = Translator()

    @commands.command(name='translate')
    async def translate(self, ctx, language, *, text):
        """Translate text into english"""
        check_language = language.lower()
        
        if not misc.check_language(check_language):
            return await ctx.send(f"Sorry, but {language} doesn't seem to be a valid language for translation, try `-languages` to get a list of translation languages")
        
        dest = misc.get_language_code(check_language)
        
        output = self._translator.translate(text, dest=dest)
        embed = discord.Embed(title='Translated', color=0xBFEDDD)
        embed.add_field(name=f'From {output.src}', value=output.origin, inline=False)
        embed.add_field(name=f'To {output.dest}', value=output.text, inline=False)
        await ctx.send(embed=embed)
 
    @translate.error
    async def translate_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"missing an arguement, {error.param}")  
            
    @commands.command(name='languages')
    async def languages(self, ctx):
        langs = misc.get_languages()
        lang_output = formatter.quote_list(langs)
        embed = discord.Embed(title='Translation Languages', color=0xBFEDDD, description=lang_output)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Translate(bot))
