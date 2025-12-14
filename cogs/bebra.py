import disnake
from disnake.ext import commands
import datetime
from datetime import datetime
import os
import json


class Application(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Text",
                placeholder="Text",
                custom_id="text1",
                max_length=1500,
                style=disnake.TextInputStyle.paragraph
            )
        ]
        super().__init__(title="Application", components=components)
    async def callback(self, inter:disnake.ModalInteraction):
        embed= disnake.Embed(title="text",)
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False
            )
        await inter.response.send_message(embed=embed)



class bebra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = "app")
    async def appsex(self,inter: disnake.AppCmdInter):
        modal = Application()
        await inter.response.send_modal(modal=modal)

    @commands.command()
    async def bebra(self, ctx):
        await ctx.send(f"НЮХАЙ БЕБРУ!")
        await self.bot.Log2(2,f"{ctx.author} Понюхал смачной бебры")


def setup(bot):
    bot.add_cog(bebra(bot))