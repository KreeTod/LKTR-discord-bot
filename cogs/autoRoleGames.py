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
bot_settings_json = os.path.join(bot_data_path, "BotSettings.json")
bot_auto_role_games_json = os.path.join(bot_data_path, "AutoRoleGames.json")

guild_id = 1111111111111111111 #what guild i dont remember

class autoRoleGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



        @commands.Cog.listener()
        async def on_raw_reaction_add(payload):
            with open(bot_settings_json, "r") as file:
                data = json.load(file)
                for item in data:
                    AutoRoleChannelID = item["auto_role_channel_id"]
                    AutoRoleMessageID = item["auto_role_message_id"]
            if payload.channel_id == AutoRoleChannelID and payload.message_id == AutoRoleMessageID:
                guild = bot.get_guild(payload.guild_id)
                with open(bot_auto_role_games_json, "r") as file:
                    data = json.load(file)
                    for item in data:
                        if item["emoji_id"] == payload.emoji.name:
                            role_id = item["role_id"]
                            role = guild.get_role(role_id)
                            member = guild.get_member(payload.user_id)
                            if member.id != 1250377102306443345:
                                await member.add_roles(role)
                                await self.bot.Log2(0,f"Added role ({role.name}) to member ({member.display_name})")
                            break


        @commands.Cog.listener()
        async def on_raw_reaction_remove(payload):
            with open(bot_settings_json, "r") as file:
                data = json.load(file)
                for item in data:
                    AutoRoleChannelID = item["auto_role_channel_id"]
                    AutoRoleMessageID = item["auto_role_message_id"]
            if payload.channel_id == AutoRoleChannelID and payload.message_id == AutoRoleMessageID:
                guild = bot.get_guild(payload.guild_id)
                with open(bot_auto_role_games_json, "r") as file:
                    data = json.load(file)
                    for item in data:
                        if item["emoji_id"] == payload.emoji.name:
                            role_id = item["role_id"]
                            role = guild.get_role(role_id)
                            member = guild.get_member(payload.user_id)
                            if member.id != 1250377102306443345:
                                await member.remove_roles(role)
                                await self.bot.Log2(0,f"Deleted role ({role.name}) to member ({member.display_name})")

                            break





        def create_auto_role_embed(guild):
            descr = ""
            emojiList = []

            with open(bot_auto_role_games_json, "r") as file:
                data = json.load(file)
                count = 0
                for item in data:
                    emoji_id = item["emoji_id"]
                    game_full_name = item["game_full_name"]
                    role_id = item["role_id"]
                    gameEmoji = disnake.utils.get(guild.emojis, name=emoji_id)
                    emojiList.append(gameEmoji)
                    role = guild.get_role(role_id)
                    descr += f"\n{gameEmoji} - {game_full_name}"

            auto_role_embed = disnake.Embed(
                title="_________________Auto Roles__________________",
                description=f"To get a role, click on the corresponding reaction\n!!! All auto-roles will be reset after the server release!!!\n{descr}",
                color=0xfc0303
            )
            
            print(auto_role_embed, emojiList)
            return auto_role_embed, emojiList
        ##############################################################################################
        @bot.command()
        @commands.has_permissions(manage_roles=True, administrator=True)
        async def MakeNewAutoRoleMsg(ctx):
            guild = ctx.guild
            banner = "AutoRolesBanner.png"

            rules_banner_path = os.path.join(bot_banners_path, banner)
            if os.path.isfile(rules_banner_path):
                with open(rules_banner_path, "rb") as f:
                    picture = disnake.File(f)


            try:
                auto_role_embed, emojis = create_auto_role_embed(guild)
            except ValueError as e:
                await ctx.send(str(e))
                return

            msg = await ctx.channel.send(file = picture,embed=auto_role_embed)

            for emoji in emojis:
                await msg.add_reaction(emoji)
                await self.bot.Log2(f"Added reaction ({emoji}) to auto tole message")
        ##############################################################################################
        @bot.slash_command(
            name = "update_autorole_message",
            description ="Write an event to the news channel"
        )
        async def UpdateAutoRoleMsg(inter: disnake.ApplicationCommandInteraction):
            auto_role_embed, emojis = create_auto_role_embed(inter.guild)

            channel = inter.channel
            try:
                msg = await channel.fetch_message(1251584181922955325)
                await msg.edit(embed=auto_role_embed)
                await bot.Log2("Message was deleted",0)

                for em in emojis :
                    await msg.add_reaction(em)
                    await bot.Log2(0,f"Readction added {em.name} to autorole message")
                await inter.response.send_message("Message succsesfuly updated")

            except disnake.NotFound:
                await bot.Log2(0,f"Could not find message with ID {AutoRoleMessageID}")
                await inter.response.send_message(f"Could not find message with ID {AutoRoleMessageID}",0)




        async def AutoUpdateAutoRoleMsg():
            guild = self.bot.get_guild(guild_id)
            auto_role_embed, emojis = create_auto_role_embed(guild)
            with open(bot_settings_json, "r") as file:
                data = json.load(file)
                for item in data:
                    AutoRoleChannelID = item["auto_role_channel_id"]
                    AutoRoleMessageID = item["auto_role_message_id"]
            channel = guild.fetch_channel(AutoRoleChannelID)
            msg = await channel.fetch_message(1251584181922955325)
            try:
                msg = await disnake.channel.fetch_message(AutoRoleMessageID)

            except disnake.NotFound:
                await bot.Log2(0,f"Can't find auto-role message. Making new auto-role message...")



            try:
                msg = await channel.fetch_message(AutoRoleMessageID)
                await msg.edit(embed=auto_role_embed)
                await bot.Log2("Сообщение успешно обновлено",0)

                for em in emojis :
                    await msg.add_reaction(em)
                    await bot.Log2(0,f"Added {em.name} reaction to auto roles message")
                await inter.response.send_message("Message successfully updated")

            except disnake.NotFound:
                await bot.Log2(0,f"Could not find message with ID {AutoRoleMessageID}")
                await inter.response.send_message(f"Could not find message with ID {AutoRoleMessageID}",0)




def setup(bot):
    bot.add_cog(autoRoleGames(bot))