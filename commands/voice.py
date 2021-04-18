import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import youtube_dl
import os
import ctypes.util

class voice(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel #voice channel caller is connected to

        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
                if voice.channel != channel:
                    await ctx.send(f"`Moving to channel: {channel.name}`")
                    await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send(f"`Joined {channel.name}`")

    @commands.command(pass_context=True, aliases=['l', 'lea'])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"`Left {channel}`")
        else:
            await ctx.send("`Don't think I am in a voice channel`")

    @commands.command(pass_context=True, aliases=['p', 'pla'])
    async def play(self, ctx, url: str):
        channel = ctx.message.author.voice.channel
        song_there = os.path.isfile("song.mp3")
        name="previous song"

        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
                if voice.channel != channel:
                    await ctx.send(f"`Moving to channel: {channel.name}`")
                    await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send(f"`Joined {channel.name}`")

        if url != "again":
            try:
                if song_there:
                    os.remove("song.mp3")
                    print("Removed old song file")
            except PermissionError:
                print("Trying to delete song file, but it's being played")
                await ctx.send("`ERROR: Music playing`")
                return

            await ctx.send("`WAH Getting everything ready now`")

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                await ctx.send("`Processing the Audio`")
                ydl.download([url])

            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    name = file
                    print(f"Renamed File: {file}\n")
                    os.rename(file, "song.mp3")

            #ctypes.util.find_library()

        if song_there:
            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07

            nname = name.rsplit("-", 2)
            await ctx.send(f"`Playing: {nname[0]}`")
            print("playing\n")
        else:
            await ctx.send(f"`Cannot play again, send Youtube Link`")

    @commands.command()
    async def finesse(self, ctx, url: str):

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                infile = file
                DestinationFile = discord.File(infile)
                await ctx.send("`Finessed:`", file=DestinationFile)
                os.remove(infile)
            else:
                await ctx.send("`MP3 not Found`")

def setup(client):
    client.add_cog(voice(client))