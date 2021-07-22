import discord
import random
import asyncio
from discord import message
import discord.ext.commands.context as C
import discord_slash.context as S

from json import *
from discord.ext import commands
from discord.channel import DMChannel
from functions.general import getResponse
from functions.statsFuncs import waluigiBotStats
from functions.redditFuncs import hmmmFunction
from functions.pokemonFuncs import mainPokemonCommand
from functions.constants import GAME_STATS_FILE, SONG_FILE, DAILY_MESSAGE_HELP

DAILY_DICT = "dailyChanLists"

MUSIC = "song"
STATS = "stat"
HMMM = "hmmm"
POKEMON = "pokemon"
INFO = "info"
VALID_ARGUMENTS = [MUSIC, STATS, HMMM, POKEMON, INFO]

numDailys = 4
MUSIC_INDEX = 0
STATS_INDEX = 1
HMMM_INDEX = 2
POKEMON_INDEX = 3
previousDayMessage = [None for i in range(numDailys)]

def getChannelList(channelList: str):
    with open(GAME_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)
    try:
        return WahDict[DAILY_DICT][channelList]
    except:
        print(f"DictError: {channelList} not Found")

def getChannelInfo(chan_id):
    results ="```\nThis channel is receiving the following daily messages:\n"
    numDailys = 0
    with open(GAME_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)
        WahDict = WahDict[DAILY_DICT]
    for dailyType in WahDict:
        if chan_id in WahDict[dailyType]:
            results += f"\t- {dailyType}\n"
            numDailys += 1
    if numDailys == 0:
        results = "```\nThis channel is not receiving any daily messages.\n"
    else:
        results += f"\n{numDailys} total daily messages\n"
    results += "```"
    return results

def deleteChannelFromList(dailyType, channel):
    with open(GAME_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)
    WahDict[DAILY_DICT][dailyType].remove(channel)
    with open(GAME_STATS_FILE, "w") as OUTFile:
        dump(WahDict, OUTFile, indent="  ")

def updateSongList():
    infile = open(SONG_FILE, "r")
    songs = []
    for song in infile:
        songs += [song]
    return songs

async def showPreviousDaily(ctx, dailyTypeIndex):
    previousResult = previousDayMessage[dailyTypeIndex]
    if previousResult != None:
        prefix = "`Example of Previous Daily:`\n"
        if type(previousResult) == discord.Embed:
            return await ctx.send(content=prefix, embed=previousResult)
        return await ctx.send(prefix + previousResult)
    return None

async def dailyCommandFunction(discordClient, ctx, dailyType):
    # Bot checks if command is invoked in a text channel
    if type(ctx.channel) == DMChannel:
        return await ctx.send("`You can only receive daily messages in a server's text channel`")

    # Bot checks if it can send messages in that channel
    sendPerms = ctx.channel.permissions_for(await ctx.guild.fetch_member(discordClient.user.id)).send_messages
    if not sendPerms:
        return await ctx.author.send("`I cannot send messages in that text channel`")
    
    chan_id = ctx.channel.id

    # determine if the given argument is valid
    if dailyType == None or dailyType not in VALID_ARGUMENTS:
        return await ctx.send(DAILY_MESSAGE_HELP)
    if dailyType == INFO:
        info = getChannelInfo(chan_id)
        return await ctx.send(info)

    dailyChannelList = getChannelList(dailyType)
    
    # activate daily message
    if chan_id not in dailyChannelList:
        with open(GAME_STATS_FILE, "r") as INFile:
            WahDict = load(INFile)
        WahDict[DAILY_DICT][dailyType] += [chan_id]
        dailyChannelList = WahDict[DAILY_DICT][dailyType]
        with open(GAME_STATS_FILE, "w") as OUTFile:
            dump(WahDict, OUTFile, indent="  ")
        await ctx.send(f"`This Channel Will Now Receive Routine Messages for {dailyType}`")
        return await showPreviousDaily(ctx, VALID_ARGUMENTS.index(dailyType))

    if type(ctx) == S.SlashContext:
        deleteChannelFromList(dailyType, chan_id)
        return await ctx.send(f"`This Channel Will No Longer Receive Routine Messages for {dailyType}`")

    # cancel daily message for text command
    await ctx.send("`This Channel Already Receives Routine Messages\nDo you want me to stop sending Messages? (yes/no)`")

    response = await getResponse(discordClient, ctx)

    if response.content.lower() == "yes":
        deleteChannelFromList(dailyType, chan_id)
        return await ctx.send(f"`This Channel Will No Longer Receive Routine Messages for {dailyType}`")
    return await ctx.send("`No changes have been made.`")

async def dailySongMessage(c: commands.Bot):
    songChannelList = getChannelList(MUSIC)
    songs = updateSongList()
    spotify_link = random.choice(songs)
    with open(GAME_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)
    day = WahDict["music_day"]
    messageContent = "`Waluigi's Daily `:calendar:` Music `:musical_note:` Recommendation `:point_down:` Day:` " + str(day) + "\n" + str(spotify_link)
    previousDayMessage[MUSIC_INDEX] = messageContent

    for chan_id in songChannelList:
        mus_channel = c.get_channel(chan_id)
        try:
            await mus_channel.send(messageContent)
        except:
            print(f"Error in Routine Message for {chan_id}")
            WahDict[DAILY_DICT][MUSIC].remove(chan_id) # remove no longer valid channel id

    WahDict["music_day"] += 1
    with open(GAME_STATS_FILE, "w") as OUTFile:
        dump(WahDict, OUTFile, indent="  ")

async def dailyStatMessage(c: commands.Bot):
    statChannelList = getChannelList(STATS)
    stat_embed = waluigiBotStats(c.user, len(c.guilds), len(c.users))
    previousDayMessage[STATS_INDEX] = stat_embed

    for chan_id in statChannelList:
        stat_channel = c.get_channel(chan_id)
        try:
            await stat_channel.send(embed=stat_embed)
        except:
            print(f"Error in Routine Message for {chan_id}")
            deleteChannelFromList(STATS, chan_id)

async def dailyHmmmMessage(c: commands.Bot):
    statChannelList = getChannelList(HMMM)
    imgUrl = await hmmmFunction()
    previousDayMessage[HMMM_INDEX] = imgUrl

    for chan_id in statChannelList:
        channel = c.get_channel(chan_id)
        try:
            await channel.send(imgUrl)
        except:
            print(f"Error in Routine Message for {chan_id}")
            deleteChannelFromList(HMMM, chan_id)

async def dailyPokemonMessage(c: commands.Bot):
    statChannelList = getChannelList(POKEMON)
    name_num = str(random.choice(range(1,899)))
    pokeEmbed = mainPokemonCommand(name_num)
    previousDayMessage[POKEMON_INDEX] = pokeEmbed

    for chan_id in statChannelList:
        channel = c.get_channel(chan_id)
        try:
            await channel.send(embed=pokeEmbed)
        except:
            print(f"Error in Routine Message for {chan_id}")
            deleteChannelFromList(POKEMON, chan_id)
