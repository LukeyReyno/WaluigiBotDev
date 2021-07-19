import discord
import random
import asyncio

from json import *
from discord.ext import commands
from functions.general import getResponse
from functions.statsFuncs import waluigiBotStats
from functions.redditFuncs import hmmmFunction
from functions.pokemonFuncs import mainPokemonCommand
from functions.constants import GAME_STATS_FILE, SONG_FILE

MUSIC = "songChanList"
STATS = "statChanList"
HMMM = "hmmmChanList"
POKEMON = "pokemonChanList"

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

async def dailyCommandFunction(discordClient, ctx, dailyType):
    sendPerms = ctx.channel.permissions_for(await ctx.guild.fetch_member(discordClient.user.id)).send_messages
    if not sendPerms:
        return await ctx.author.send("`I cannot send messages in that text channel`")
    
    c = ctx.channel.id

    dailyChannelList = updateChannelList(dailyType)
    
    if c not in dailyChannelList:
        with open(GAME_STATS_FILE, "r") as INFile:
            WahDict = load(INFile)
        WahDict[dailyType] += [c]
        dailyChannelList = WahDict[dailyType]
        with open(GAME_STATS_FILE, "w") as OUTFile:
            dump(WahDict, OUTFile, indent="  ")
        return await ctx.send(f"`This Channel Will Now Receive Routine Messages for {dailyType}`")

    await ctx.send("`This Channel Already Receives Routine Messages\nDo you want me to stop sending Messages? (yes/no)`")

    response = await getResponse(discordClient, ctx)

    if response.content.lower() == "yes":
        with open(GAME_STATS_FILE, "r") as INFile:
            WahDict = load(INFile)
        WahDict[dailyType].remove(c)
        dailyChannelList = WahDict[dailyType]
        with open(GAME_STATS_FILE, "w") as OUTFile:
            dump(WahDict, OUTFile, indent="  ")
        return await ctx.send("`This Channel Will No Longer Receive Routine Messages`")
    return await ctx.send("`No changes have been made.`")

async def dailySongMessage(c: commands.Bot):
    songChannelList = updateChannelList(MUSIC)
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
    statChannelList = updateChannelList(STATS)
    stat_embed = waluigiBotStats(c.user, len(c.guilds), len(c.users))

    for chan_id in statChannelList:
        stat_channel = c.get_channel(chan_id)
        try:
            await stat_channel.send(embed=stat_embed)
        except:
            print(f"Error in Routine Message for {chan_id}")

async def dailyHmmmMessage(c: commands.Bot):
    statChannelList = updateChannelList(HMMM)
    imgUrl = await hmmmFunction()

    for chan_id in statChannelList:
        channel = c.get_channel(chan_id)
        try:
            await channel.send(imgUrl)
        except:
            print(f"Error in Routine Message for {chan_id}")

async def dailyPokemonMessage(c: commands.Bot):
    statChannelList = updateChannelList(POKEMON)
    name_num = str(random.choice(range(1,899)))
    pokeEmbed = mainPokemonCommand(name_num)

    for chan_id in statChannelList:
        channel = c.get_channel(chan_id)
        try:
            await channel.send(embed=pokeEmbed)
        except:
            print(f"Error in Routine Message for {chan_id}")