import discord
import random
import pickle
import discord.ext.commands.context as C
import discord_slash.context as S

from json import *
from discord.ext import commands
from discord import message
from discord.channel import DMChannel
from functions.general import getResponse
from functions.statsFuncs import waluigiBotStats
from functions.redditFuncs import imageFunction
from functions.pokemonFuncs import mainPokemonCommand
from functions.botwFuncs import botwFunction
from functions.animeFuncs import randomAnime, ANIME_CREDENTIAL
from functions.constants import DAILY_CHANNEL_LIST, SONG_FILE, DAILY_MESSAGE_HELP

DAILY_DICT = "dailyChanLists"

MUSIC = "song"
STATS = "stat"
HMMM = "hmmm"
POKEMON = "pokemon"
BOTW = "botw"
ANIME = "anime"
INFO = "info"
validArguments = [MUSIC, STATS, HMMM, POKEMON, BOTW, ANIME, INFO]

try:
    with open("data/prevDaily.pickle", "rb") as pickleFile:
        prevDict = pickle.load(pickleFile)
except:
    prevDict = {}

def getChannelList(channelList: str):
    with open(DAILY_CHANNEL_LIST, "r") as INFile:
        WahDict = load(INFile)
    try:
        return WahDict[DAILY_DICT][channelList]
    except:
        print(f"DictError: {channelList} not Found")

def getChannelInfo(chan_id):
    results ="```\nThis channel is receiving the following daily messages:\n"
    numDailys = 0
    with open(DAILY_CHANNEL_LIST, "r") as INFile:
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
    with open(DAILY_CHANNEL_LIST, "r") as INFile:
        WahDict = load(INFile)
    WahDict[DAILY_DICT][dailyType].remove(channel)
    with open(DAILY_CHANNEL_LIST, "w") as OUTFile:
        dump(WahDict, OUTFile, indent="  ")

def updateSongList():
    infile = open(SONG_FILE, "r")
    songs = []
    for song in infile:
        songs += [song]
    return songs

async def showPreviousDaily(ctx, dailyType):
    try:
        previousResult = prevDict[dailyType]
        if previousResult != None:
            prefix = "`Example of Previous Daily:`\n"
            if type(previousResult) == discord.Embed:
                return await ctx.send(content=prefix, embed=previousResult)
            return await ctx.send(prefix + previousResult)
    except Exception as e:
        print(f"{__name__}: {e}")
        pass
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
    if dailyType == None or dailyType not in validArguments:
        return await ctx.send(DAILY_MESSAGE_HELP)
    if dailyType == INFO:
        info = getChannelInfo(chan_id)
        return await ctx.send(info)

    dailyChannelList = getChannelList(dailyType)
    
    # activate daily message
    if chan_id not in dailyChannelList:
        with open(DAILY_CHANNEL_LIST, "r") as INFile:
            WahDict = load(INFile)
        WahDict[DAILY_DICT][dailyType] += [chan_id]
        dailyChannelList = WahDict[DAILY_DICT][dailyType]
        with open(DAILY_CHANNEL_LIST, "w") as OUTFile:
            dump(WahDict, OUTFile, indent="  ")
        await ctx.send(f"`This Channel Will Now Receive Routine Messages for {dailyType}`")
        return await showPreviousDaily(ctx, dailyType)

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

def updateDailyJSON(func):
    async def inner(*args, **kwargs):
        with open(DAILY_CHANNEL_LIST, "r") as INFile:
            WahDict = load(INFile)
        await func(WahDict, *args, **kwargs)
        with open(DAILY_CHANNEL_LIST, "w") as OUTFile:
            dump(WahDict, OUTFile, indent="  ")
    return inner

@updateDailyJSON
async def dailySongMessage(WahDict, c: commands.Bot):
    songChannelList = getChannelList(MUSIC)
    songs = updateSongList()
    spotify_link = random.choice(songs)
    day = WahDict["music_day"]
    messageContent = "`Waluigi's Daily `:calendar:` Music `:musical_note:` Recommendation `:point_down:` Day:` " + str(day) + "\n" + str(spotify_link)
    prevDict[MUSIC] = messageContent

    for chan_id in songChannelList:
        mus_channel = c.get_channel(chan_id)
        try:
            await mus_channel.send(messageContent)
        except:
            print(f"Error in Routine Message for {chan_id}")
            WahDict[DAILY_DICT][MUSIC].remove(chan_id) # remove no longer valid channel id
    WahDict["music_day"] += 1

@updateDailyJSON
async def dailyStatMessage(WahDict, c: commands.Bot):
    statChannelList = getChannelList(STATS)
    stat_embed = waluigiBotStats(c.user, len(c.guilds), len(c.users))
    prevDict[STATS] = stat_embed

    for chan_id in statChannelList:
        stat_channel = c.get_channel(chan_id)
        try:
            await stat_channel.send(embed=stat_embed)
        except:
            print(f"Error in Routine Message for {chan_id}")
            WahDict[DAILY_DICT][STATS].remove(chan_id)

@updateDailyJSON
async def dailyHmmmMessage(WahDict, c: commands.Bot):
    statChannelList = getChannelList(HMMM)
    imgUrl = await imageFunction()
    prevDict[HMMM] = imgUrl

    for chan_id in statChannelList:
        channel = c.get_channel(chan_id)
        try:
            await channel.send(imgUrl)
        except:
            print(f"Error in Routine Message for {chan_id}")
            WahDict[DAILY_DICT][HMMM].remove(chan_id)

@updateDailyJSON
async def dailyPokemonMessage(WahDict, c: commands.Bot):
    statChannelList = getChannelList(POKEMON)
    name_num = str(random.choice(range(1,899)))
    pokeEmbed = mainPokemonCommand(name_num)
    prevDict[POKEMON] = pokeEmbed

    for chan_id in statChannelList:
        channel = c.get_channel(chan_id)
        try:
            await channel.send(embed=pokeEmbed)
        except:
            print(f"Error in Routine Message for {chan_id}")
            WahDict[DAILY_DICT][POKEMON].remove(chan_id)

@updateDailyJSON
async def dailyBotwMessage(WahDict, c: commands.Bot):
    statChannelList = getChannelList(BOTW)
    botwEmbed = botwFunction(None)
    prevDict[BOTW] = botwEmbed

    for chan_id in statChannelList:
        channel = c.get_channel(chan_id)
        try:
            await channel.send(embed=botwEmbed)
        except:
            print(f"Error in Routine Message for {chan_id}")
            WahDict[DAILY_DICT][BOTW].remove(chan_id)

@updateDailyJSON
async def dailyAnimeMessage(WahDict, c: commands.Bot):
    statChannelList = getChannelList(ANIME)
    try:
        anime_embed = randomAnime(ANIME_CREDENTIAL)
    except:
        # Token Likely expired
        ANIME_CREDENTIAL.reAuthorize()
        print("MAL Token Regenerated and set as current Access Token")
        try:
            anime_embed = randomAnime(ANIME_CREDENTIAL)
        except:
            print("Token Error Daily Anime not possible!\n")

    if (anime_embed == None):
        await print("`Anime Token Error: Bot Needs to Refresh access to MyAnimeList, this may take some time.`")

    else:
        prevDict[ANIME] = anime_embed

        for chan_id in statChannelList:
            channel = c.get_channel(chan_id)
            try:
                await channel.send(embed=anime_embed)
            except:
                print(f"Error in Routine Message for {chan_id}")
                WahDict[DAILY_DICT][ANIME].remove(chan_id)

def dumpPrevDict():
    with open("data/prevDaily.pickle", "wb") as pickleFile:
        pickle.dump(prevDict, pickleFile, pickle.HIGHEST_PROTOCOL)

async def fullDailyRoutine(c: commands.Bot):
    await dailySongMessage(c)
    await dailyStatMessage(c)
    await dailyHmmmMessage(c)
    await dailyPokemonMessage(c)
    await dailyBotwMessage(c)
    await dailyAnimeMessage(c)
    dumpPrevDict()