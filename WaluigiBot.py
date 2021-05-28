import discord
import random
import asyncio
import time
import datetime

from discord.ext import commands, tasks
from json import *
from discord.ext.commands.errors import *
from discord_slash import SlashCommand

TOKEN = ""
TOKENFile = open("WahToken.txt", "r")
for line in TOKENFile:
    TOKEN = line

GUILDS=[674409360948068372] #TestingServer
GAME_STATS_FILE="data/WahNCounter.json"
COMMAND_STATS_FILE="data/commandStats.json"
ADMIN_FILE="data/admins.json"
WORDS_FILE="data/words.json"
SONG_FILE="data/songs.txt"

intents = discord.Intents.default()
intents.members = True

c = commands.Bot(command_prefix = "dwah ", case_insensitive=True, intents=intents)
slash = SlashCommand(c, sync_commands=True)

c.remove_command('help')

def updateChannelList():
    with open(GAME_STATS_FILE, "r") as INFile:
                WahDict = load(INFile)
    return WahDict["chanList"]

def updateSongList():
    infile = open(SONG_FILE, "r")
    songs = []
    for song in infile:
        songs += [song]
    return songs

dailyChannelList = updateChannelList()
songs_command = updateSongList()

async def background_loop():
    await c.wait_until_ready()
    while not c.is_closed():
        dailyChannelList = updateChannelList()
        for chan_id in dailyChannelList:
            chan = c.get_channel(chan_id)
            foods = '🍏 🍎 🍐 🍊 🍋 🍌 🍉 🍇 🍓 🍈 🍒 🍑 🥭 🍍 🥥 🥝 🍅 🍆 🥑 🥦 🥬 🥒 🌶 🌽 🥕 🧄 🧅 🥔 🍠 🥐 🥯 🍞 🥖 🥨 🧀 🥚 🍳 🧈 🥞 🧇 🥓 🥩 🍗 🍖 🦴 🌭 🍔 🍟 🍕 🥪 🥙 🧆 🌮 🌯 🥗 🥘 🥫 🍝 🍜 🍲 🍛 🍣 🍱 🥟 🦪 🍤 🍙 🍚 🍘 🍥 🥠 🥮 🍢 🍡 🍧 🍨 🍦 🥧 🧁 🍰 🎂 🍮 🍭 🍬 🍫 🍿 🍩 🍪 🌰 🥜 🍯 🥛 🍼 🍵 🧃 🥤 🍶 🍺 🍻 🥂 🍷 🥃 🍸 🍹 🧉 🍾 🧊 :poop:'
            food_list = foods.split()
            animals = '🐶 🐱 🐭 🐹 🐰 🦊 🐻 🐼 🐨 🐯 🦁 🐮 🐷 🐸 🐵 🐔 🐧 🐦 🐤 🦆 🦅 🦉 🦇 🐺 🐗 🐴 🦄 🐝 🐛 🦋 🐌 🐞 🐜 🦟 🦗 🕷 🦂 🐢 🐍 🦎 🦖 🦕 🐙 🦑 🦐 🦞 🦀 🐡 🐠 🐟 🐬 🐳 🐋 🦈 🐊 🐅 🐆 🦓 🦍 🦧 🐘 🦛 🦏 🐪 🐫 🦒 🦘 🐃 🐂 🐄 🐎 🐖 🐏 🐑 🦙 🐐 🦌 🐕 🐩 🦮 🐕‍🦺 🐈 🐓 🦃 🦚 🦜 🦢 🦩 🕊 🐇 🦝 🦨 🦡 🦦 🦥 🐁 🐀 🐿 🦔 🐉'
            animals_list = animals.split()
            try:
                await chan.send(f"{random.choice(food_list)}{random.choice(animals_list)}")
            except:
                print(f"Error in Routine Message for {chan_id}")
        lt = time.localtime(time.time())
        if False: #1pm in UTC
            songs = updateSongList()
            spotify_link = random.choice(songs)
            with open(GAME_STATS_FILE, "r") as INFile:
                WahDict = load(INFile)
            day = WahDict["music_day"]
            for chan_id in dailyChannelList:
                mus_channel = c.get_channel(chan_id)
                try:
                    await mus_channel.send("`Waluigi's Daily `:calendar:` Music `:musical_note:` Recommendation `:point_down:` Day:` " + str(day) + "\n" + str(spotify_link))
                except:
                    print(f"Error in Routine Message for {chan_id}")
            WahDict["music_day"] += 1
            with open(GAME_STATS_FILE, "w") as OUTFile:
                dump(WahDict, OUTFile, indent="  ")
            MP_num = random.choice(range(2,11))
            await c.change_presence(activity=discord.Game(name=f"Mario Party {MP_num} | dwah help"))
            for g in c.guilds:
                try: #check for empty channels or missing permissions
                    textChannel = random.choice(g.text_channels)
                    messages = await textChannel.history(limit=5).flatten()
                    await random.choice(messages).add_reaction(random.choice(["🤓", "🤡", "👽", "🤔", "🤥", "😳"]))
                except:
                    print("Failed to React in: " + f"{g.name}")
                    pass
        await asyncio.sleep(3600)

@c.event
async def on_ready():
    print('Logged in as')
    print(c.user.name)
    print(c.user.id)

    upDate = datetime.datetime.now().date()
    print(upDate)
    with open(GAME_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)
    WahDict["upDate"] = str(upDate)
    with open(GAME_STATS_FILE, "w") as OUTFile:
        dump(WahDict, OUTFile, indent="  ")

    print('-------')
    await c.change_presence(activity=discord.Game(name="Mario Kart 8 Deluxe | dwah help"))

cogs = [
    "commands.basic", 
    "commands.hangman", 
    "commands.wordsearch", 
    "commands.reddit", 
    "commands.botw", 
    "commands.admin", 
    "commands.voice",
    "commands.exec",
    "commands.component",
    "commands.stats",
    "slashcommands.sBasic",
    "slashcommands.sBotw",
    "slashcommands.sReddit"
    ]#, "commands.anime"]
for cog in cogs:
    c.load_extension(cog)

@c.event
async def on_message(message):
    if c.user.mentioned_in(message):
        with open(GAME_STATS_FILE, "r") as INFile:
            WahDict = load(INFile)
        try:
            WahDict["mentions"] += 1
        except:
            WahDict["mentions"] = 1
        with open(GAME_STATS_FILE, "w") as OUTFile:
            dump(WahDict, OUTFile, indent="  ")
    await c.process_commands(message)

def updateCommandData(ctx: commands.context.Context):
    with open(GAME_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)

    #For User's command count
    try:
        WahDict["games"]["commands"][str(ctx.author.id)] += 1
    except:
        WahDict["games"]["commands"][str(ctx.author.id)] = 1
    with open(GAME_STATS_FILE, "w") as OUTFile:
        dump(WahDict, OUTFile, indent="  ")


    with open(COMMAND_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)

    #For Waluigi Bot's command count
    WahDict["command_count"] += 1
    try:
        WahDict["commands"][f"{ctx.command}"] += 1
    except:
        WahDict["commands"][f"{ctx.command}"] = 1
    with open(COMMAND_STATS_FILE, "w") as OUTFile:
        dump(WahDict, OUTFile, indent="  ")

@c.event
async def on_slash_command(ctx):
    updateCommandData(ctx)

@c.event
async def on_command_completion(ctx):
    updateCommandData(ctx)

@c.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, CommandNotFound):
        return await ctx.send("`That is not a valid command\nType 'wah help' for a list`")
    elif isinstance(error, MissingRequiredArgument):
        return await ctx.send("`You need to include correct arguments for this command\nType 'wah help' for an example`")
    elif isinstance(error, MissingPermissions):
        return await ctx.send("`User is missing the valid permissions to use that command`")
    elif isinstance(error, BotMissingPermissions):
        return await ctx.author.send("`I'm missing valid permissions to use that command`")
    elif isinstance(error, AttributeError):
        return await ctx.send("`Make sure you're using correct arguments\nType 'wah help' for an example`")
    elif isinstance(error, CommandInvokeError):
        try:
            if not ctx.channel.permissions_for(await ctx.guild.fetch_member(c.user.id)).send_messages:
                return await ctx.author.send("`Unable to satisfy the command. Make sure I have permission to type in that channel\nYou can also type 'wah help' here for some more information.`")
            elif not ctx.channel.permissions_for(await ctx.guild.fetch_member(c.user.id)).embed_links:
                return await ctx.send("`Make sure I can embed links\nUse 'wah help' somewhere else for more info`")
            return await ctx.send("`Make sure you're using valid arguments\n/are in a valid channel with enough user permissions`")
        except:
            print("Sending Message error")
    else:
        return await ctx.send("`ERROR: Looks like something bad happened.`")

c.loop.create_task(background_loop())
c.run(TOKEN)
