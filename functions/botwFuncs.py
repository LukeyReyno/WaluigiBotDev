import discord
import random

from json import *

with open("data/compendiumImages.txt") as f:
    imageList = f.read().splitlines()

with open("data/hyruleCompendium.json") as j:
    compendiumList = load(j)
    nameList = []
    for dict in compendiumList:
        nameList.append(dict["name"])

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

def botwFunction(name_num:str):
    if name_num == None:
        compObject = random.choice(compendiumList) #gets dict of a compendium Object
    elif name_num.isdigit():
        if 0 < int(name_num) < 390:
            compObject = compendiumList[int(name_num)-1]
        else:
            return "`Not a valid Hyrule Compendium ID [1, 389]`"
    elif name_num.lower() in nameList:
        nameIndex = nameList.index(name_num.lower())
        compObject = compendiumList[nameIndex]
    else:
        return "`Not a valid Hyrule Compendium entry`"
    botwEmbed = createBotwEmbed(compObject)
    return botwEmbed
