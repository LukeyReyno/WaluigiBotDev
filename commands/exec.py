import discord
import os
import subprocess

from discord.ext import commands, tasks
from json import *

DISCORD_MESSAGE_CHAR_LIMIT = 2000
MESSAGEHISTORYLIMIT = 35

async def getMostRecentFile(ctx):
    messages = await ctx.channel.history(limit=MESSAGEHISTORYLIMIT).flatten()
    j = 0
    while (j < len(messages)):
        if (len(messages[j].attachments) > 0):
            return messages[j].attachments[0]
        j += 1
    return None

async def basicExecWithFile(ctx, command):
    messageAttachment = await getMostRecentFile(ctx)
    if (messageAttachment != None):
        outputPath = f"exec/{command}Result.txt"

        fname = f"exec/{messageAttachment.filename}"
        await messageAttachment.save(fname)
        stdOutput = subprocess.Popen([command, fname], stdout=subprocess.PIPE).communicate()[0]
        stdOutput = stdOutput.decode('utf-8')
        if (len(stdOutput) >= DISCORD_MESSAGE_CHAR_LIMIT):
            outfile = open(outputPath, 'w')
            outfile.write(stdOutput)
            outfile.close()
            destinationFile = discord.File(f"{outputPath}")
            await ctx.send(f"`{command.upper()} file: `", file=destinationFile)
            os.remove(f"{outputPath}")
        else:
            await ctx.send(f"```{stdOutput}```")
        os.remove(fname)
    else:
        return await ctx.send(f"`No recent files (Last {MESSAGEHISTORYLIMIT} messages). Send a new one.`")

class exec(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["wc"])
    async def wordcount(self, ctx):
        await basicExecWithFile(ctx, "wc")

    @commands.command(aliases=["hex"])
    async def xxd(self, ctx):
        await basicExecWithFile(ctx, "xxd")

    @commands.command(aliases=["wf"])
    async def wordfrequency(self, ctx):
        await basicExecWithFile(ctx, "wf")

def setup(client):
    client.add_cog(exec(client))