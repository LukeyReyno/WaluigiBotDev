import discord
import os
import requests
import WaluigiBotDev

from discord.ext import commands, tasks
from json import *

WCFILE = "data/wordcount.txt"
XXDFILE = "data/xxd.txt"

async def getMostRecentFile(ctx):
    messages = await ctx.channel.history(limit=45).flatten()
    j = 0
    while (j < len(messages)):
        if (len(messages[j].attachments) > 0):
            return messages[j].attachments[0]
        j += 1
    return None

class exec(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["wc"])
    async def wordcount(self, ctx):
        messageAttachment = await getMostRecentFile(ctx)
        if (messageAttachment != None):
            print(messageAttachment.content_type)
            fname = f"data/{messageAttachment.filename}"
            await messageAttachment.save(fname)
            exitcode = os.system(f"wc {fname} > {WCFILE}")
            destinationFile = discord.File(f"{WCFILE}")
            await ctx.send("`WordCount File: `", file=destinationFile)
            os.remove(fname)
            os.remove(f"{WCFILE}")
        else:
            await ctx.send("`No recent files were sent in this chat.`")

    @commands.command(aliases=["hex"])
    async def xxd(self, ctx):
        messageAttachment = await getMostRecentFile(ctx)
        if (messageAttachment != None):
            print(messageAttachment.content_type)
            fname = f"data/{messageAttachment.filename}"
            await messageAttachment.save(fname)
            exitcode = os.system(f"xxd {fname} > {XXDFILE}")
            destinationFile = discord.File(f"{XXDFILE}")
            await ctx.send("`XXD file: `", file=destinationFile)
            os.remove(fname)
            os.remove(f"{XXDFILE}")
        else:
            await ctx.send("`No recent files were sent in this chat.`")
        

def setup(client):
    client.add_cog(exec(client))