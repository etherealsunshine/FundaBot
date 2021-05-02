import asyncio
from os import error
from discord.ext import commands
from utils import misc
from utils import dynacalc_methods as dyna

class Math(commands.Cog, name='Math'):
    """Math related commands"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="calc", aliases=['dyna'])
    async def calc(self, ctx):
        """Dynamic calculator
        Allows you to type out what you wanna do and then will ask for input accordingly
        Example: I wish to add"""
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        await ctx.send("What would you like to do?")
        
        try:
            input = await self.bot.wait_for('message', timeout = 100.0, check = check)
        except asyncio.TimeoutError:
            return await ctx.send('You took too long!') 
        
        if "add" in input.clean_content.lower():
            await ctx.send("Alright you want to add! How many numbers do you wanna add?")
            try:
                num_amount = await self.bot.wait_for('message', timeout = 60.0, check = check)
            except asyncio.TimeoutError:
                return await ctx.send('You took too long!')
            
            if misc.check_number(num_amount.clean_content) == False:
                return await ctx.send("Not a valid input, retry the command!")
            
            nums = []
            looper = 0
            while looper < int(num_amount.clean_content):
                await ctx.send("Enter a number")
                try:
                    num = await self.bot.wait_for('message', timeout = 60.0, check = check)
                    
                    if not misc.check_number(num.clean_content):
                        return await ctx.send("Not a valid input, retry the command!")
                except asyncio.TimeoutError:
                    return await ctx.send('You took too long!')
                nums.append(int(num.clean_content))
                looper += 1
            
            answer = dyna.add(nums) 
            await ctx.send(f'The answer is {answer}')           
        elif "subtract" in input.clean_content.lower():
            await ctx.send("Alright you wanna subtract! How many numbers do you wanna subtract?")
            try:
                num_amount = await self.bot.wait_for('message', timeout = 60.0, check = check)
            except asyncio.TimeoutError:
                return await ctx.send('You took too long!')
            
            if not misc.check_number(num_amount.clean_content):
                return await ctx.send("Not a valid input, retry the command!")
            
            nums = []
            looper = 0
            while looper < int(num_amount.clean_content):
                await ctx.send("Enter a number")
                try:
                    num = await self.bot.wait_for('message', timeout = 60.0, check = check)
                    
                    if not misc.check_number(num.clean_content):
                        return await ctx.send("Not a valid input, retry the command!")
                except asyncio.TimeoutError:
                    return await ctx.send('You took too long!')
                nums.append(int(num.clean_content))
                looper += 1
            
            answer = dyna.subtract(nums) 
            await ctx.send(f'The answer is {answer}')
        elif "multiply" in input.clean_content.lower() or "multiplication" in input.clean_content.lower():
            await ctx.send("Alright you want to multiply! How many numbers do you wanna multiply")
            try:
                num_amount = await self.bot.wait_for('message', timeout = 60.0, check = check)
            except asyncio.TimeoutError:
                return await ctx.send('You took too long!')
            
            if not misc.check_number(num_amount.clean_content):
                return await ctx.send("Not a valid input, retry the command!")
            
            nums = []
            looper = 0
            while looper < int(num_amount.clean_content):
                await ctx.send("Enter a number")
                try:
                    num = await self.bot.wait_for('message', timeout = 60.0, check = check)
                    
                    if not misc.check_number(num.clean_content):
                        return await ctx.send("Not a valid input, retry the command!")
                except asyncio.TimeoutError:
                    return await ctx.send('You took too long!')
                nums.append(int(num.clean_content))
                looper += 1
            
            answer = dyna.multiply(nums) 
            await ctx.send(f'The answer is {answer}')
        elif "divide" in input.clean_content.lower() or "division" in input.clean_content.lower():
            await ctx.send("Alright we're dividing!")
            try:
                await ctx.send("Enter the dividend")
                x_input = await self.bot.wait_for('message', timeout = 60.0, check = check)
                
                if not misc.check_number(x_input.clean_content):
                    return await ctx.send("Not a valid input, try again!")
                
                x = int(x_input.clean_content.lower())
            except asyncio.TimeoutError:
                return await ctx.send("You took too long!")
            
            try:
                await ctx.send("Enter the divisor")
                y_input = await self.bot.wait_for('message', timeout=60.0, check=check)

                if not misc.check_number(y_input.clean_content):
                    return await ctx.send("Not a valid input, try again!")

                y = int(y_input.clean_content.lower())
                
                if misc.is_zero(y):
                    return await ctx.send("Cannot divide by zero!")
            except asyncio.TimeoutError:
                return await ctx.send("You took too long!")
            
            answer = dyna.divide(x, y)
            await ctx.send(f"Quotient is {answer}")
        
            
    
def setup(bot):
    bot.add_cog(Math(bot))
