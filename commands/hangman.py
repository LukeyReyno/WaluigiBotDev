import discord
from discord.ext import commands, tasks
import math
import random
import asyncio
import copy

from json import *
from WaluigiBot import WORDS_FILE, GAME_STATS_FILE

class hangman(commands.Cog):

    def __init__(self, client):
        self.client = client

    def getWordDict(self):
        with open(WORDS_FILE, "r") as INFile:
            return load(INFile)

    def check_word(self, guess_list, secret_word):
        for letter in secret_word.lower():
            if not letter in guess_list:
                return False
        return True
    
    def final_statement(self, original_embed, NS, display_list, guess_list, imgnum, chances):
        em = copy.deepcopy(original_embed)
        String = NS + f"\nThis is your word: `{display_list}`\n"
        String += f"\n`{guess_list}`"
        imgnum = 6 - chances
        em.set_image(url=f"https://lukeyreyno.github.io/lukeyreyno-website/pictures/Hangman.{imgnum}.png")
        em.description = String
        return em

    async def getGuess(self, ctx): #method for getting guesses and deleting author message
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            guess = await self.client.wait_for('message', check=check, timeout=120)
        except:
            await ctx.send("`TimeoutError: Game Ended.`")
            return -1

        try:
            await guess.delete()
        except:
            pass

        return guess
    
    @commands.command()
    async def hangman(self, ctx):
        guess_list = [] 
        display_list=""
        wordDict = self.getWordDict()
        secret_word_hint = random.choice(list(wordDict.keys()))
        secret_word = random.choice(wordDict[secret_word_hint])
        chances = 6
        first_time = True
        
        embmsg=""
        imgnum=0

        original_embed = discord.Embed()
        original_embed.title = f"{ctx.author.name} is playing Waluigi Hangman"
        original_embed.color = 0x7027C3
        original_embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")

        for letter in secret_word:
            display_list += "_ "
        
        NS = ""

        while self.check_word(guess_list, secret_word) == False and chances > 0:
            display_list = ""

            for letter in secret_word:
                if letter.lower() in guess_list:
                    display_list += letter
                else:
                    display_list += "_ "

            em = copy.deepcopy(original_embed)
            String = NS + f"\nThis is your word: `{display_list}`"
            String += "\nYou have 2 minutes per answer"
            imgnum = 6 - chances
            em.set_image(url=f"https://lukeyreyno.github.io/lukeyreyno-website/pictures/Hangman.{imgnum}.png")
            if chances < 3:
                String += f"\n(Hint: {secret_word_hint})"
            String += f"\nYou have {chances} chances. \nWhat letter will you guess?\n"
            String += f"\n`{guess_list}`"
            em.description = String

            if first_time == True:
                embmsg = await ctx.send(embed=em)
                first_time = False
            else:
                await embmsg.edit(embed=em)

            guess = await self.getGuess(ctx)
            if guess == -1:
                return

            if guess.content.lower() == secret_word.lower():
                break
            elif len(guess.content) == len(secret_word):
                NS = f"Nope, ({guess.content}) is not the solution"
                chances -= 1
                continue

            while guess.content.isalpha() == False or len(guess.content) > 1 or guess.content.lower() in guess_list:
                em.add_field(name="Error", value="Please enter a single letter that was not already chosen.")
                await embmsg.edit(embed=em)

                guess = await self.getGuess(ctx)

            guess_list.append(guess.content.lower())
            if guess == -1:
                return

            if guess.content.lower() == secret_word.lower():
                break
            elif len(guess.content) == len(secret_word):
                NS = f"Nope, ({guess.content}) is not the solution"
                chances -= 1
                continue
            elif guess.content.lower() in secret_word.lower():
                NS = f"Yes, ({guess.content}) is in the word."
            else:
                NS = f"Nope, ({guess.content}) is not in the word."
                chances -= 1

        if chances == 0:
            em = self.final_statement(original_embed, NS, display_list, guess_list, imgnum, chances)
            await embmsg.edit(embed=em)
            return await ctx.send("`Sorry, you lost. The word was %s`" % secret_word)
        else:
            em = self.final_statement(original_embed, NS, display_list, guess_list, imgnum, chances)
            await embmsg.edit(embed=em)
            await ctx.send("`Congratulations, you are a super star!`")
            await ctx.send(f"`The word was {secret_word}`")
            await ctx.send(f"`Thanks for playing you can request words to be added by using the command`\n\
                `wah word (word)`")
            with open(GAME_STATS_FILE, "r") as INFile:
                WahDict = load(INFile)
            try:
                WahDict["games"]["hangman"][str(ctx.author.id)] += 1
            except:
                WahDict["games"]["hangman"][str(ctx.author.id)] = 1
            with open(GAME_STATS_FILE, "w") as OUTFile:
                dump(WahDict, OUTFile, indent="  ")
            return

def setup(client):
    client.add_cog(hangman(client))