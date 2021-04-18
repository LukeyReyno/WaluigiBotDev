import discord
from discord.embeds import Embed
from discord.ext import commands, tasks
import math
import random
import asyncio
import copy
from json import *

from discord.flags import alias_flag_value

ROWCOUNT = 15
COLUMNCOUNT = 17

class wordsearch(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def getGuess(self, ctx): #method for getting guesses and deleting author message
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            guess = await self.client.wait_for('message', check=check, timeout=240)
        except:
            await ctx.send("`TimeoutError: Game Ended.`")
            return ""

        return guess
    
    @commands.command(aliases=["word-search", "word_search", "ws"])
    async def wordsearch(self, ctx, difficulty : str = None):
        wordDict = getWordDict()
        secret_word_hint = random.choice(list(wordDict.keys()))
        secret_word = random.choice(wordDict[secret_word_hint])
        game =  gameGridSetup(secret_word)
        gameGrid = game[0]
        startingRow = game[1]
        startingCol = game[2]
        mutationType = game[3]
        gameGridString = ""
        for row in gameGrid:
            gameGridString += f"{' '.join(list(row))}\n"

        original_embed = discord.Embed()
        original_embed.title = f"{ctx.author.name} is playing Waluigi Word Search"
        original_embed.color = 0x7027C3
        original_embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")
        if difficulty == "hard" or difficulty == "-h":
            original_embed.description = f"Wow, playing hard mode I see\nYou have 4 minutes to find the secret word\nWords can be forwards horizontal or vertical\nNo wrong answers!!\n"
        else:
            original_embed.description = f"You have 4 Minutes to find the secret word\nWords can be forwards or down\nNo wrong answers!!\n\nYour word hint is: {secret_word_hint}\n"#The word starts with the letter: `{secret_word[0]}`"
        em = copy.deepcopy(original_embed)
        original_embed.add_field(name="Word Search", value=f"\n`{gameGridString}`")

        message = await ctx.send(embed=original_embed)
        
        guess = await self.getGuess(ctx)

        if guess.content.lower() == secret_word.lower():
            await ctx.send("`Congratulations, you are a super star!`")
            await ctx.send(f"`The word was {secret_word}`")
            await ctx.send(f"`Thanks for playing you can request words to be added by using the command:`\n\
                `wah word (word)`")
            with open("data/WahNCounter.json", "r") as INFile:
                WahDict = load(INFile)
            try:
                WahDict["games"]["wordsearch"][str(ctx.author.id)] += 1
            except:
                WahDict["games"]["wordsearch"][str(ctx.author.id)] = 1
            with open("data/WahNCounter.json", "w") as OUTFile:
                dump(WahDict, OUTFile, indent="  ")
        else:
            await ctx.send("`Sorry, you lost. The word was %s`" % secret_word)

        #This section is used to highlight the correct answer
        r = startingRow
        c = startingCol
        gameGridString = ""
        s = secret_word.upper()
        i = 0
        rValue = list(gameGrid[r])
        while i < len(s):
            rValue[c] = f"`{s[i]}`"
            if mutationType == 0: #Forward
                c += 1
                if i == len(s) - 1:
                    nrValue = "".join(rValue)
                    gameGrid[r] = "".join(nrValue.split("``"))
            elif mutationType == 1: #Down
                gameGrid[r] = "".join(rValue)
                r += 1
                if i != 0:
                    rValue = list(gameGrid[r])
            i += 1

        for row in gameGrid:
            gameGridString += f"{' '.join(list(row))}\n"
        em.add_field(name="Word Search Answer", value=f"\n`{gameGridString}`")
        return await message.edit(embed=em)

def getWordDict():
        with open("data/words.json", "r") as INFile:
            return load(INFile)

def gameGridSetup(sWord):
    sWord = sWord.upper()
    capitals = [chr(i) for i in range(65,91)]
    r = 0
    c = 0
    rValue = ""
    grid = []
    while r < ROWCOUNT:
        while c < COLUMNCOUNT:
            rValue += random.choice(capitals)
            c += 1
        r += 1
        c = 0
        grid += [rValue]
        rValue = ""
    return gridMutate(grid, sWord)

def gridMutate(grid, sWord):
    g = copy.deepcopy(grid)
    r = random.choice(range(ROWCOUNT))
    c = random.choice(range(COLUMNCOUNT))
    startingRow = r
    startingColumn = c
    mutateNum = random.choice(range(2))
    for char in sWord:
        rValue = list(grid[r])
        rValue[c] = char
        grid[r] = "".join(rValue)
        if mutateNum == 0: #Forward
            c += 1
        elif mutateNum == 1: #Down
            r += 1
        if not (0 <= r < ROWCOUNT) or not (0 <= c < COLUMNCOUNT):
            return gridMutate(g, sWord)
    return (grid, startingRow, startingColumn, mutateNum)

def setup(client):
    client.add_cog(wordsearch(client))