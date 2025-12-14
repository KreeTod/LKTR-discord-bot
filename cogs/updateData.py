import disnake
from disnake.ext import commands
import datetime
from datetime import datetime
import os
import json

bot_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(bot_path)
bot_path = parent_dir

#bot_path = os.path.dirname(os.path.realpath(__file__))
bot_data_path = os.path.join(bot_path, "data")
bot_banners_path = os.path.join(bot_path, "banners")

bot_rules_message_txt = os.path.join(bot_data_path, "RulesMessage.txt")

class ApplicationUpdateRulesText(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="UpdateData",
                placeholder="writeurmessage",
                custom_id="text1",
                max_length=4000,
                style=disnake.TextInputStyle.paragraph
            )
        ]
        super().__init__(title="Application", components=components)
    async def callback(self, inter:disnake.ModalInteraction):
        embed= disnake.Embed(title="text",)
        for key, value in inter.text_values.items():
            #embed.add_field(
            #    name=key.capitalize(),
            #    value=value[:1024],
            #    inline=False
            #)
            with open(bot_rules_message_txt, "w", encoding="utf-8") as file:
                file.write(value[:1024])
        #await inter.response.send_message(embed=embed)



class updateData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = "updaterulestext")
    async def updaterulestext(self,inter: disnake.AppCmdInter):
        modal = ApplicationUpdateRulesText()
        await inter.response.send_modal(modal=modal) 


def setup(bot):
    bot.add_cog(updateData(bot))