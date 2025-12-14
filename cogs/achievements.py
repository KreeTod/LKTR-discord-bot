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

guild_id = 1179685986830131271
nsfwChannelId = 1331757650429349969
memeChannelId = 1331767235794042941
artChannelId = 1331767209856598106
content_types_list = ["image/png","image/jpeg","image/bmp","image/gif",
                      "video/mp4","video/webp","video/avi","video/mkp","video/mov", "video/wmv", "video/webm", "video/mpeg", "video/mpg", "video/ogv","video/asf"]
class achievements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        guild = self.bot.get_guild(guild_id)
        #////////////////////////////////////////////////////////////////////////////////////////////////////////////////               
        if message.channel.id == nsfwChannelId:
            for attachment in message.attachments:
                print(f"{attachment.content_type}")
                if attachment.content_type.lower() in content_types_list:
                    with open(bot_user_data_json, "r", encoding="utf-8") as f:
                        userdata = json.load(f)
                    user_found = False
                    for user in userdata:
                        if user.get("UserId", 0) == message.author.id:
                            user["NSFWSend"] = user.get("NSFWSend", 0) + 1
                            user_found = True
                            break
                    with open(bot_user_data_json, "w", encoding="utf-8") as f:
                        json.dump(userdata, f, ensure_ascii=False, indent=4)
                        await self.bot.Log2(0, "User Data ['NSFWSend'] updated +1")
        if message.channel.id == memeChannelId:
            for attachment in message.attachments:
                print(f"{attachment.content_type}")
                if attachment.content_type.lower() in content_types_list:
                    with open(bot_user_data_json, "r", encoding="utf-8") as f:
                        userdata = json.load(f)
                    user_found = False
                    for user in userdata:
                        if user.get("UserId", 0) == message.author.id:
                            user["MemesSend"] = user.get("MemesSend", 0) + 1
                            user_found = True
                            break
                    with open(bot_user_data_json, "w", encoding="utf-8") as f:
                        json.dump(userdata, f, ensure_ascii=False, indent=4)
                        await self.bot.Log2(0, "User Data ['MemesSend'] updated +1")
        if message.channel.id == artChannelId:
            for attachment in message.attachments:
                print(f"{attachment.content_type}")
                if attachment.content_type.lower() in content_types_list:
                    with open(bot_user_data_json, "r", encoding="utf-8") as f:
                        userdata = json.load(f)
                    user_found = False
                    for user in userdata:
                        if user.get("UserId", 0) == message.author.id:
                            user["ArtsSend"] = user.get("ArtsSend", 0) + 1
                            user_found = True
                            break
                    with open(bot_user_data_json, "w", encoding="utf-8") as f:
                        json.dump(userdata, f, ensure_ascii=False, indent=4)
                        await self.bot.Log2(0, "User Data ['ArtsSend'] updated +1")
        #////////////////////////////////////////////////////////////////////////////////////////////////////////////////               

        with open(bot_curse_words_list, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                if item.get("word", "").lower() in message.content.lower():
                    with open(bot_user_data_json, "r", encoding="utf-8") as f:
                        userdata = json.load(f)
                    user_found = False
                    for user in userdata:
                        if user.get("UserId", 0) == message.author.id:
                            user["SwearingWritten"] = user.get("SwearingWritten", 0) + 1
                            user_found = True
                            break
                    with open(bot_user_data_json, "w", encoding="utf-8") as f:
                        json.dump(userdata, f, ensure_ascii=False, indent=4)
                    return 
        #////////////////////////////////////////////////////////////////////////////////////////////////////////////////               
    def writeAcvmnts(userID):
        ListOfAchievements = []
        with open(bot_user_data_json, "r", encoding="utf-8") as f:
            usersData = json.load(f)
        with open(bot_achievements_list, "r", encoding="utf-8") as f:
            achiementsData = json.load(f)
        for u in usersData:
            if u.get("UserId",0) == userID:
                user = u
        if user.get("NSFWSend","") >= 1000:
            for achievement in achiementsData:
                if achievement.get("Name","") == "NSFWSend" and achievement.get("Value",0)>=1000:
                    sex=0
                    ListOfAchievements.append(achievement)

        print(ListOfAchievements)

            
                


def setup(bot):
    bot.add_cog(achievements(bot))