import disnake
from disnake.ext import commands
import datetime
from datetime import datetime
import os
import json


class moneyFunction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def bebra221(self, ctx):
        await ctx.send(f"НЮХАЙ БЕБРУ!")
        await self.bot.Log2(2,f"{ctx.author} Понюхал смачной бебры")


def setup(bot):
    bot.add_cog(moneyFunction(bot))