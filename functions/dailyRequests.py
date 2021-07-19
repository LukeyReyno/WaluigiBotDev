import discord
import random
import asyncio

from discord import embeds
from json import *
from discord.ext import commands
from functions.statsFuncs import waluigiBotStats
from functions.redditFuncs import hmmmFunction
from functions.constants import GAME_STATS_FILE, SONG_FILE

def updateChannelList(channelList: str):
    with open(GAME_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)
    try:
        return WahDict[channelList]
    except:
        print(f"DictError: {channelList} not Found")

def updateSongList():
    infile = open(SONG_FILE, "r")
    songs = []
    for song in infile:
        songs += [song]
    return songs

async def dailySongMessage(c: commands.Bot):
    songChannelList = updateChannelList("songChanList")
    songs = updateSongList()
    spotify_link = random.choice(songs)
    with open(GAME_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)
    day = WahDict["music_day"]
    for chan_id in songChannelList:
        mus_channel = c.get_channel(chan_id)
        try:
            await mus_channel.send("`Waluigi's Daily `:calendar:` Music `:musical_note:` Recommendation `:point_down:` Day:` " + str(day) + "\n" + str(spotify_link))
        except:
            print(f"Error in Routine Message for {chan_id}")
    WahDict["music_day"] += 1
    with open(GAME_STATS_FILE, "w") as OUTFile:
        dump(WahDict, OUTFile, indent="  ")

async def dailyStatMessage(c: commands.Bot):
    statChannelList = updateChannelList("statChanList")
    for chan_id in statChannelList:
        stat_channel = c.get_channel(chan_id)
        try:
            stat_embed = waluigiBotStats(c.user, len(c.guilds), len(c.users))
            await stat_channel.send(embed=stat_embed)
        except:
            print(f"Error in Routine Message for {chan_id}")

async def dailyHmmmMessage(c: commands.Bot):
    statChannelList = updateChannelList("hmmmChanList")
    for chan_id in statChannelList:
        channel = c.get_channel(chan_id)
        try:
            imgUrl = hmmmFunction()
            await channel.send(imgUrl)
        except:
            print(f"Error in Routine Message for {chan_id}")