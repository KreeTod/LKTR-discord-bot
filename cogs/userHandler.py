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

guild_id = 1179685986830131271


class UserData:
    def __init__(self, username: str = "", user_id: int = 0, xp: int = 10, gold: int = 10, roles_id: list[int] = None):
        self.UserName = username
        self.UserId = user_id
        self.XP = xp
        self.Gold = gold
        self.RolesID = roles_id if roles_id is not None else [1179690579647529021, 1180954834153771118]
    
    def CheckCorrectnessOfData(self) -> bool:
        if self.UserName == None or not isinstance(self.UserName, str):
            return False
        
        if self.UserId == None or not isinstance(self.UserId, int):
            return False
        
        if self.XP == None or not isinstance(self.XP, int):
            return False
        
        if self.Gold == None or not isinstance(self.Gold, int):
            return False
        
        if self.RolesID == None or not isinstance(self.RolesID, list):
            return False
        
        return True

class userHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        guild = self.bot.get_guild(guild_id)
        if os.path.isfile(bot_user_data_json):
            with open(bot_user_data_json, "r") as f:
                data = json.load(f)
                if not any(item["UserId"] == member.id for item in data):
                    new_user = UserData(username=f"{member.display_name}", user_id=member.id)
                    await self.bot.Log2(0, "Created new member's profile in data")
                    await self.bot.Log2(0,f"{new_user.UserName, new_user.UserId, new_user.XP, new_user.Gold, new_user.RolesID }")
                    new_position = {
                        "ServerName" :new_user.UserName,
                        "UserId" :new_user.UserId,
                        "XP" :new_user.XP,
                        "Gold" :new_user.Gold,
                        "RolesID" :new_user.RolesID
                    }
                    data.append(new_position)
                    with open(bot_user_data_json, "w") as file:
                        json.dump(data, file, indent=4)
                    with open(bot_user_data_json, "r") as f:
                        data = json.load(f)
                        for item in data:
                            if item["UserId"] == member.id:
                                for role_id in item["RolesID"]:
                                    role = guild.get_role(role_id)
                                    if role != None:
                                        await member.add_roles(role)
                                        await self.bot.Log2(0, "New member get role")
                                    else:
                                        await self.bot.Log2(2, "Invalid role id!")
                else:
                    await self.bot.Log2(0, "New member already in data")
                    for item in data:
                        if item["UserId"] == member.id:
                            for role_id in item["RolesID"]:
                                role = guild.get_role(role_id)
                                if role != None:
                                    await member.add_roles(role)
                                    await self.bot.Log2(0, "New member get role")
                                else:
                                    await self.bot.Log2(2, "Invalid role id!")



        
            
        #newuser = UserData(username = f"{member.display_name}", user_id=member.id, )

    async def Cfa(self, data:UserData):
        if data.CheckCorrectnessOfData() == True:
            await self.bot.Log2(0,"Everything is OK")
        else:
            await self.bot.Log2(2,"Nothing is OK")
        


def setup(bot):
    bot.add_cog(userHandler(bot))