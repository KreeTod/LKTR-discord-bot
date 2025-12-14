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
bot_user_data_json = os.path.join(bot_data_path, "UserData.json")
bot_curse_words_list = os.path.join(bot_data_path, "CurseWordsBase.json")
bot_achievements_list = os.path.join(bot_data_path, "Achievements.json")

# idk what is going on here. I burned down when started to write this year ago

class ApplicationMakeEvent(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="Short name of the event",
                custom_id="eventname",
                max_length=50,
                style=disnake.TextInputStyle.paragraph
            ),
            disnake.ui.TextInput(
                label="Event discription",
                placeholder="Describe the essence of the event, its conditions, rewards, etc.",
                custom_id="eventdiscription",
                max_length=1500,
                style=disnake.TextInputStyle.paragraph
            ),
            disnake.ui.TextInput(
                label="Image URL",
                placeholder="Enter the image link",
                custom_id="eventimage",
                style=disnake.TextInputStyle.short
            )

        ]
        super().__init__(title="Application", components=components)
    async def callback(self, inter:disnake.ModalInteraction):
        embed= disnake.Embed(title=f"**{inter.text_values['eventname']}**",)
        embed.add_field(name="",value=inter.text_values["eventdiscription"], inline=False)
        embed.add_field(name="",value="Event status - Continues", inline=False)
        embed.set_image(url=inter.text_values["eventimage"])
        butt = ButtonView(embed)
        await inter.response.send_message(embed=embed, view=butt)


class ButtonView(disnake.ui.View):
    def __init__(self, embed: disnake.Embed):
        super().__init__()
        self.embed = embed
    @disnake.ui.button(label="Change event state", style=disnake.ButtonStyle.primary)
    async def blue_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        print(self.embed.title)
        newembed= disnake.Embed(title=f"{self.embed.title}")
        for field in self.embed.fields:
            print("field name : "+field.name)
            print("field value : "+field.value)
            if "Event status - Continues" in field.value:
                #field.value = "Event status - Завершён"
                newembed.add_field(name="",value="Event status - Ended", inline=False)
            elif "Event status - Ended" in field.value:
                #field.value = "Event status - Continues"
                newembed.add_field(name="",value="Event status - Continues", inline=False)
            else:
                #field.value = "Event status - unknown"
                newembed.add_field(name="",value=field.value, inline=False)
        print(f"field url : {self.embed.image.url}")
        newembed.set_image(url=self.embed.image.url)
        

        for field in newembed.fields:
            print("field name : "+field.name)
            print("field value : "+field.value)

        print(f"interaction.message : {interaction.message.id}")
        await interaction.message.edit(embed=newembed, view=self)
        self.embed = newembed
        await interaction.response.send_message("The status has been changed.", ephemeral=True)

    #@disnake.ui.button(label="Отключить", style=disnake.ButtonStyle.danger)
    #async def disable_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
    #    button.disabled = True
    #    await interaction.response.edit_message(view=self)
    #@disnake.ui.button(label="Сайт", style=disnake.ButtonStyle.link, url="https://tenor.com/ru/")
    #async def link_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
    #    pass



class eventhandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = "makeevent")
    async def MakeEvent(self,inter: disnake.AppCmdInter):
        modal = ApplicationMakeEvent()
        await inter.response.send_modal(modal=modal)



def setup(bot):
    bot.add_cog(eventhandler(bot))
