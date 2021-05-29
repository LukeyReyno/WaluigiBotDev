import discord
import math
import random
import asyncio

from discord.ext import commands, tasks
from json import *
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.constants import GUILDS

with open("data/compendiumImages.txt") as f:
    imageList = f.read().splitlines()

with open("data/hyruleCompendium.json") as j:
    compendiumList = load(j)
    nameList = []
    for dict in compendiumList:
        nameList.append(dict["name"])

class sBotw(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @cog_ext.cog_slash(
        name="botw", 
        description="Generates an embded detailing a Breath of the Wild Entity", 
        guild_ids=GUILDS,
        options=[
            create_option(
                name="name_num",
                description="Find by Name or Number",
                option_type=str,
                required=False,
                )
        ])
    async def botw(self, ctx: SlashContext, name_num:str=None):
        if name_num == None:
            compObject = random.choice(compendiumList) #gets dict of a compendium Object
        elif name_num.isdigit():
            if 0 < int(name_num) < 390:
                compObject = compendiumList[int(name_num)-1]
            else:
                return await ctx.send("`Not a valid Hyrule Compendium ID [1, 389]`")
        elif name_num in nameList:
            nameIndex = nameList.index(name_num.lower())
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
    client.add_cog(sBotw(client))