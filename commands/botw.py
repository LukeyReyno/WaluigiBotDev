import discord
import math
import random
import asyncio

from discord.ext import commands, tasks
from json import *

with open("data/compendiumImages.txt") as f:
    imageList = f.read().splitlines()

with open("data/hyruleCompendium.json") as j:
    compendiumList = load(j)
    nameList = []
    for dict in compendiumList:
        nameList.append(dict["name"])

class botw(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def botw(self, ctx, *, arg=None):
        if arg == None:
            compObject = random.choice(compendiumList) #gets dict of a compendium Object
        elif arg.isdigit():
            if 0 < int(arg) < 390:
                compObject = compendiumList[int(arg)-1]
            else:
                return await ctx.send("`Not a valid Hyrule Compendium ID [1, 389]`")
        elif arg.lower() in nameList:
            nameIndex = nameList.index(arg.lower())
            compObject = compendiumList[nameIndex]
        else:
            return await ctx.send("`Not a valid Hyrule Compendium entry`")
        botwEmbed = createBotwEmbed(compObject)
        return await ctx.send(embed=botwEmbed)

def createBotwEmbed(D):
    id = D["id"]
    index = id - 1 #used for image index
    e = discord.Embed()
    e.color = 0x7027C3
    e.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")
    e.title = f"{D['name'].upper()}\nID: {id}"
    e.description = D["description"]
    e.set_image(url=imageList[index])
    return e

def setup(client):
    client.add_cog(botw(client))