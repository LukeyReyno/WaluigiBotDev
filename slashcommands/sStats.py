import discord
import WaluigiBot
import asyncio

from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from json import *

class sStats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="stats", 
        description="displays mentioned user's Waluigi Bot stats", 
        guild_ids=WaluigiBot.GUILDS, 
        options=[
            create_option(
                name="mention",
                description="@User",
                option_type=6,
                required=True,
            )
        ])
    async def stats(self, ctx: SlashContext, user:str):
        if user.id == self.client.user.id:
            stats_embed = waluigiBotStats(user, len(self.client.guilds), len(self.client.users))
        else:
            stats_embed = userStats(user)
        await ctx.send(embed=stats_embed)

def getBaseEmbed(user):
    stats_embed = discord.Embed()
    stats_embed.title = f"Waluigi Bot Stats: {user.name}"
    stats_embed.color = 0x7027C3
    stats_embed.set_thumbnail(url=user.avatar_url)
    stats_embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")

    return stats_embed

def waluigiBotStats(user, numGuilds, numUsers):
    descript_string = ""
    stats_embed = getBaseEmbed(user)

    with open(WaluigiBot.GAME_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)

    cCount = WahDict["command_count"]
    mCount = WahDict["mentions"]
    updateDate = WahDict["upDate"]
    descript_string += f"`COMMAND COUNT: {cCount}`\n"
    descript_string += f"`GUILD COUNT: {numGuilds}`\n"
    descript_string += f"`USER COUNT: {numUsers}`\n"
    descript_string += f"`MENTION COUNT: {mCount}`\n"
    descript_string += f"`UPDATED: {updateDate}`\n\n"

    with open("data/commandStats.json", "r") as INFile:
        WahDict = load(INFile)

    tupleSortValues = sorted(WahDict["commands"].items(), key=lambda item: item[1])
    tupleSortValues.reverse()
    commandSorted = {key: value for key, value in tupleSortValues}
    WahDict["commands"] = commandSorted

    descript_string += "`TOP TEN USED COMMANDS: `\n"

    i = 1
    for comm in commandSorted:
        descript_string += f"`{i}. {comm}: {commandSorted[comm]}`\n"
        i += 1
        if i > 10:
            break
    with open("data/commandStats.json", "w") as OUTFile:
        dump(WahDict, OUTFile, indent="  ")

    stats_embed.description = descript_string

    return stats_embed

def userStats(user):
    descript_string = ""
    stats_embed = getBaseEmbed(user)

    with open(WaluigiBot.GAME_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)

    games = WahDict["games"]
    rank_score = 0
    for game in games:
        try:
            game_data = games[game][str(user.id)]
        except:
            game_data = 0
        descript_string += f"`{game.upper()}: {game_data}`\n"
        if game == "commands":
            rank_score += int(game_data) // 30
        else:
            rank_score += int(game_data)
    rank = rank_score // 10
    animals = '🐶 🐱 🐭 🐹 🐰 🦊 🐻 🐼 🐨 🐯 🦁 🐮 🐷 🐸 🐵 🐔 🐧 🐦 🐤 🦆 🦅 🦉 🦇 🐺 🐗 🐴 🦄 🐝 🐛 🦋 🐌 🐞 🐜 🦟 🦗 🕷 🦂 🐢 🐍 🦎 🦖 🦕 🐙 🦑 🦐 🦞 🦀 🐡 🐠 🐟 🐬 🐳 🐋 🦈 🐊 🐅 🐆 🦓 🦍 🦧 🐘 🦛 🦏 🐪 🐫 🦒 🦘 🐃 🐂 🐄 🐎 🐖 🐏 🐑 🦙 🐐 🦌 🐕 🐩 🦮 🐕‍🦺 🐈 🐓 🦃 🦚 🦜 🦢 🦩 🕊 🐇 🦝 🦨 🦡 🦦 🦥 🐁 🐀 🐿 🦔 🐉'
    animals_list = animals.split()
    stats_embed.add_field(name=f"Waluigi Bot Rank: {rank}   {animals_list[rank%len(animals_list)]}", value="`Keep using Waluigi Bot to increase Rank`")
    stats_embed.description = descript_string

    return stats_embed

def setup(client):
    client.add_cog(sStats(client))