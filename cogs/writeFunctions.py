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

bot_settings_json = os.path.join(bot_data_path, "BotSettings.json")
bot_log_txt = os.path.join(bot_data_path, "BotLog.txt")
bot_moderator_log_txt = os.path.join(bot_data_path, "ModeratorsLog.txt")
bot_user_data_json = os.path.join(bot_data_path, "UserData.json")
bot_chat_log_txt = os.path.join(bot_data_path, "ChatLog.txt")
bot_banwords_json = os.path.join(bot_data_path, "Banwords.json")
bot_auto_role_games_json = os.path.join(bot_data_path, "AutoRoleGames.json")
bot_rules_txt = os.path.join(bot_data_path, "RulesMessage.txt")

##################################################################################################################
##################################################################################################################


##################################################################################################################
##################################################################################################################




class writeFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #//////////////////////////////////////////////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////
    @commands.slash_command(
        name = "write_message",
        description ="Написать сообщение от имени бота"
    )
    @commands.has_permissions(administrator=True)
    async def write_message(self,inter: disnake.ApplicationCommandInteraction, *, text: str, channel_mention):
        if channel_mention.startswith("<#") and channel_mention.endswith(">"):
            channel_id = int(channel_mention[2:-1])
            channel = self.bot.get_channel(channel_id)
            await channel.send(f"{text}")
            await self.bot.Log2(0,f"user [{inter.author._user.mention}] made message with '/write_message' with text '{text}' in channel '{channel_mention}'")
            await inter.response.send_message(f"Сообщение успешно отправлено в канал < {channel_mention} >")
        else:
            await self.bot.Log2(0,f"user [{inter.author._user.mention}] tried to use '/write_message' with text '{text}' in channel '{channel_mention}', but failed")

    #//////////////////////////////////////////////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def make_rules_message(self, ctx, *, text: str):
        with open(bot_settings_json, "r") as file:
            settings = json.load(file)
        
        if not settings:
            await self.bot.Log2(2, "Settings file is empty or invalid")
            return

        item = settings[0]
        channel_id = item.get("rules_channel_id")
        channel = self.bot.get_channel(channel_id)
        is_written:bool = item.get("rules_is_written")

        with open(bot_rules_txt, "r") as file:
            rulesText = file.read()

        if is_written == True:
            await self.bot.Log2(1, f"user, {ctx.author} tried to make rules message. Rules message alredy wroten")
            return
        
        banner_name = "RulesBanner.png"
        banner_path = os.path.join(bot_banners_path, banner_name)
        if os.path.isfile(banner_path):
            with open(banner_path, "rb") as f:
                picture = disnake.File(f)
                rules_embed = disnake.Embed(
                    description=rulesText,
                    color=0xB96471
                )
                await channel.send(file=picture, embed=rules_embed)
            await self.bot.Log2(0,f"Rules embed created. Content : \n {text}")
        else:
            await self.bot.Log2(2,f"No <{banner_name}> in dirrectory")

    #//////////////////////////////////////////////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    @commands.slash_command(
        name = "write_news",
        description ="Написать новость от имени бота"
    )
    @commands.has_permissions(administrator=True)
    async def WriteNews(self, inter: disnake.ApplicationCommandInteraction, *, text: str, color_r:int=0,color_g:int=127,color_b:int=0):
        if color_r >=0 and color_r<=255 and color_g >=0 and color_g<=255 and color_b >=0 and color_b<=255:
            embedColor = disnake.Color.from_rgb(color_r,color_g,color_b)
        else:
            await self.bot.Log2(2,f"Invalid color")
            await inter.response.send_message(f"Новость не удалось создать. Неправильный код цвета")
            return
        with open(bot_settings_json, "r") as file:
            settings = json.load(file)

        item = settings[0]
        channel_id = item.get("news_channel_id")
        channel = self.bot.get_channel(channel_id)

        banner_name = "newsfinal.png"
        banner_path = os.path.join(bot_banners_path, banner_name)
        if os.path.isfile(banner_path):
            with open(banner_path, "rb") as f:
                picture = disnake.File(f)
                news_embed = disnake.Embed(
                    title="Новость",
                    description=text,
                    color=embedColor
                )
                await channel.send(file=picture, embed=news_embed)
            await self.bot.Log2(0,f"News embed created. Content : \n {text}")
            await inter.response.send_message(f"Новость успешно создана")
        else:
            await self.bot.Log2(2,f"No <{banner_name}> in dirrectory")
            await inter.response.send_message(f"Новость не удалось создать. Отсутствует баннер в файлах бота")
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////

    @commands.slash_command(
        name = "write_event",
        description ="Написать ивент в канал с новостями"
    )
    @commands.has_permissions(manage_roles=True, administrator=True)
    async def WriteEvent(self, inter: disnake.ApplicationCommandInteraction, *, text):
        with open(bot_settings_json, "r") as file:
            settings = json.load(file)
            for item in settings:
                channel = self.bot.get_channel(item["bot_event_channel_id"])
                break
        banner_name = "event_final.png"
        banner_path = os.path.join(bot_banners_path, banner_name)
        if os.path.isfile(banner_path):
            with open(banner_path, "rb") as f:
                picture = disnake.File(f)
                news_embed = disnake.Embed(
                    title="Ивент!",
                    description=text,
                    color=0xB96471
                )
                await channel.send(file=picture, embed=news_embed)
            await self.bot.Log2(0,f"Event message created. Content : \n {text}")
            await inter.response.send_message("Ивент создан успешно")
        else:
            await self.bot.Log2(2,f"No <{banner_name}> in dirrectory")
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////

    



def setup(bot):
    bot.add_cog(writeFunctions(bot))