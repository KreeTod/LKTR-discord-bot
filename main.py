import disnake
from disnake.ext import commands
import datetime
from datetime import datetime
import os
import json

# добавить префикс и id бота из файлика

bot = commands.Bot(command_prefix="!", help_command=None, intents=disnake.Intents.all(), test_guilds=[1179685986830131271])
bot_path = os.path.dirname(os.path.realpath(__file__))
bot_data_path = os.path.join(bot_path, "data")
bot_banners_path = os.path.join(bot_path, "banners")

bot_settings_json = os.path.join(bot_data_path, "BotSettings.json")
bot_log_txt = os.path.join(bot_data_path, "BotLog.txt")
bot_moderator_log_txt = os.path.join(bot_data_path, "ModeratorsLog.txt")
bot_user_data_json = os.path.join(bot_data_path, "UserData.json")
bot_chat_log_txt = os.path.join(bot_data_path, "ChatLog.txt")
bot_banwords_json = os.path.join(bot_data_path, "Banwords.json")
bot_auto_role_games_json = os.path.join(bot_data_path, "AutoRoleGames.json")
join_message_txt = os.path.join(bot_data_path, "joinmessage.txt")

bot.load_extension("cogs.bebra")
bot.load_extension("cogs.updateData")
#bot.load_extension("cogs.autoRoleGames")
#bot.load_extension("cogs.writeFunctions")
bot.load_extension("cogs.writeFunctions")
bot.load_extension("cogs.moneyFunction")
bot.load_extension("cogs.userHandler")
bot.load_extension("cogs.achievements")
bot.load_extension("cogs.eventhandler")


#----------------------Events-Events---------------------------------------------Events-Events-----------------------
#----------------------Events-Events---------------------------------------------Events-Events-----------------------
@bot.event
async def on_ready():
    await Log2(0,f"Bot started")
#----------------------Events-Events---------------------------------------------Events-Events-----------------------
#----------------------Events-Events---------------------------------------------Events-Events-----------------------
@bot.event
async def on_member_join(member: disnake.Member):
    bot_newbie_chanel_id = 0
    with open(bot_settings_json, "r") as file:
        data = json.load(file)
        for item in data:
            bot_newbie_chanel_id = item["newbie_chanel_id"]
            break
    channel = bot.get_channel(bot_newbie_chanel_id)
    with open(join_message_txt, "r", encoding="utf-8") as file:
        #data = json.load(file)
        join_message = file.read()
        state_embed = disnake.Embed(
            title="New member",
            description=f"{member.mention}, enjoy! \n {join_message}",
            color=0xfc0303
        )
        await channel.send(embed=state_embed)

#----------------------Events-Events---------------------------------------------Events-Events-----------------------
#----------------------Events-Events---------------------------------------------Events-Events-----------------------

@bot.event
async def on_message(message: disnake.message):
    await bot.process_commands(message)
    with open(bot_banwords_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        for item in data :
        #    if item["word_list"] in message.content.lower():
        #        print(f'banword {item["word_list"]} detected')
        #        await message.channel.send(f"{message.author.mention}, а по жопе?")
        #        await message.delete()
        #        Log2("Banword system work", 0)

            if any(word in message.content.lower() for word in item["word_list"]):
                print(f'banword {item["word_list"]} detected')
                await message.channel.send(f"{message.author.mention}, а по жопе?")
                await message.delete()
                Log2("Banword system work", 0)
#----------------------Events-Events---------------------------------------------Events-Events-----------------------
#----------------------Events-Events---------------------------------------------Events-Events-----------------------
@bot.event
async def on_message_delete(message: disnake.Message):

    bot_log_chanel_id = 0
    with open(bot_settings_json, "r") as file:
        data = json.load(file)
        for item in data:
            bot_log_chanel_id = item["log_chanel_id"]
            break
    time_current = datetime.now()
    channel = bot.get_channel(bot_log_chanel_id)

    deleted_message_embed = disnake.Embed(
        title="Deleted message",
        description=f"```\n{message.content}\n```\nDeleted image/video:",
        color=0xB96471
    )
    await channel.send(embed=deleted_message_embed)
    if message.attachments != None:
        for item in message.attachments:
            await channel.send(item)

    print(f"Message deleted in {time_current} that contains : \n {message.content}")
#----------------------Events-Events---------------------------------------------Events-Events-----------------------
#----------------------Events-Events---------------------------------------------Events-Events-----------------------
@bot.event
async def on_raw_reaction_add(payload):
    with open(bot_settings_json, "r") as file:
        data = json.load(file)
        for item in data:
            auto_role_channel_id = item["auto_role_channel_id"]
            auto_role_message_id = item["auto_role_message_id"]
            break
    if payload.channel_id == auto_role_channel_id and payload.message_id == auto_role_message_id:
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
                        await Log2(f"User ({member.display_name}) get role ({role.name})\n",0)
                    break
#----------------------Events-Events---------------------------------------------Events-Events-----------------------
#----------------------Events-Events---------------------------------------------Events-Events-----------------------
@bot.event
async def on_raw_reaction_remove(payload):
    with open(bot_settings_json, "r") as file:
        data = json.load(file)
        for item in data:
            auto_role_channel_id = item["auto_role_channel_id"]
            auto_role_message_id = item["auto_role_message_id"]
            break
    if payload.channel_id == auto_role_channel_id and payload.message_id == auto_role_message_id:
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
                        await Log2(f"User ({member.display_name}) lost role ({role.name})\n",0)

                    break
#----------------------Events-Events---------------------------------------------Events-Events-----------------------
#----------------------Events-Events---------------------------------------------Events-Events-----------------------


def switchOfLogSeverity(value):
    switch_dict = {
        0: "Log\u00A0\u00A0\u00A0\u00A0\u00A0",
        1: "Warning\u00A0",
        2: "Error\u00A0\u00A0\u00A0"
    }
    return switch_dict.get(value, "Unknown")

async def Log2(warning_level:int = 0, content:str = ""):
    content_to_log = f"[ {datetime.now()} ] -{switchOfLogSeverity(warning_level)}- {content}\n"

    with open(bot_log_txt, "a", encoding="utf-8") as file:
        file.write(content_to_log)
    print(content_to_log)
    with open(bot_settings_json, "r") as file:
        data = json.load(file)
        for item in data:
            bot_log_chanel = bot.get_channel(item["log_chanel_id"])
            break
        ready_msg = disnake.Embed(
            description=f"{content_to_log}",
            color=0x9d03fc
        )
        await bot_log_chanel.send(embed=ready_msg)







bot.Log2 = Log2
with open(bot_settings_json, "r", encoding="utf-8") as file:
    data = json.load(file)
    bot.run(data["token"])
