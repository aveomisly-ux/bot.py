import discord
from discord.ext import commands

class ExampleCog(commands.Cog):
    """Example cog with basic commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='hello')
    async def hello(self, ctx):
        """Simple hello command"""
        await ctx.send(f'Hello {ctx.author.name}! 👋')
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check bot latency"""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f'🏓 Pong! Latency: {latency}ms')

async def setup(bot):
    await bot.add_cog(ExampleCog(bot))
