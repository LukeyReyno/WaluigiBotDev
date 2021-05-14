import discord
from discord.ext import commands, tasks
import datetime
import shutil

from json import *

class admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.admins = []
        self.adminChannelID = 0
        self.wordChannelID = 0
        self.initialize_admins()
    
    def initialize_admins(self):
        with open("data/admins.json", "r") as INFile:
            adminDict = load(INFile)
        self.admins = adminDict["admins"]
        self.adminChannelID = adminDict["adminChannelID"]
        self.wordChannelID = adminDict["wordChannelID"]


    @commands.command()
    async def copy(self, ctx, infile, outfile):
        if await self.adminCheck(ctx):
            pass
        else:
            try:
                try: 
                    DestinationFile = discord.File(outfile)
                    await ctx.author.send("`Unchanged`", file=DestinationFile)
                except:
                    await ctx.channel.send("`New file being created`")
                shutil.copyfile(infile, outfile)
                DestinationFile = discord.File(outfile)
                await ctx.author.send("`Changed`", file=DestinationFile)
            except Exception as e:
                return await ctx.channel.send("`Error has occurred`\n" + str(e))

    @commands.command()
    async def grab(self, ctx, infile):
        if await self.adminCheck(ctx):
            pass
        else:
            try: 
                DestinationFile = discord.File(infile)
                await ctx.channel.send("`Here's your file:`", file=DestinationFile)
                return await ctx.channel.send("`I sent you your file`")
            except Exception as e:
                return await ctx.channel.send(f"`Error has occurred: {e}`")

    @commands.command()
    async def cat(self, ctx, infile):
        if await self.adminCheck(ctx):
            pass
        else:
            try:
                f = open(infile)
                str = ""
                for line in f:
                    str += line
                return await ctx.channel.send(f"`{str}`")
            except Exception as e:
                return await ctx.channel.send(f"`Error has occurred: {e}`\n`If file is too large use wah grab (file)`")

    @commands.command()
    async def logs(self, ctx):
        if await self.adminCheck(ctx):
            pass
        else:
            logfile = discord.File("log.txt")
            await ctx.channel.send("`Logs Delivered.`")
            try:
                await ctx.author.send(datetime.datetime.now(), file=logfile)
            except:
                pass

    @commands.command()
    async def guilds(self, ctx):
        if await self.adminCheck(ctx):
            pass
        else:
            await ctx.send(f"`Total Number of Guilds: {len(self.client.guilds)}`")
            gList = ""
            for g in self.client.guilds:
               gList += f"- {g.name}\n"
            outfile = open("guilds.txt", 'w')
            outfile.write(gList)
            outfile.close()
            destinationFile = discord.File("guilds.txt")
            await ctx.send("`Guild List File: `", file=destinationFile)

    """@commands.command()
    async def randomReact(self, ctx):
        if await self.adminCheck(ctx):
            pass
        else:
            failList = ""
            failure = False
            for g in self.client.guilds:
                    try:
                        textChannel = random.choice(g.text_channels)
                        messages = await textChannel.history(limit=5).flatten()                   
                        await random.choice(messages).add_reaction(random.choice(["🤓", "🤡", "👽", "🤔", "🤥", "😳"]))
                    except:
                        failure = True
                        failList += f"` - {g.name}`\n"
                        print("WaluigiBot React Error")
                        pass
            if failure:
                await ctx.send("`I have failed to react in a server - ><_><`")
                await ctx.send(failList)
            await ctx.send("`I have reacted - 0w0`")"""

    @commands.command()
    async def word(self, ctx, w, flag : str=None):
        if ctx.author.id not in self.admins:
            adminChannel = self.client.get_channel(self.adminChannelID)
            await adminChannel.send(f'`The word "{w}" has been recommended for bot use.`\n`Admins can approve the word by using the wah word (word) command.`')
            return await ctx.send(f"`Request for word: {w} has been sent\nVisit the Support Server to see word list.`")
        else:
            with open("data/words.json", "r") as INFile:
                wordDict = load(INFile)
            
            if w.isalpha() == False or len(w) < 4:
                return await ctx.send("`Let's not add a scuffed word`")
            for key in list(wordDict.keys()): # could be more efficient
                if w in wordDict[key]:
                    if flag == "-d" or "remove":
                        wordDict[key].remove(w)
                        with open("data/words.json", "w") as OUTFile:
                            dump(wordDict, OUTFile, indent="  ")
                        return await ctx.send(f"`Deleted word: {w}`")

                    return await ctx.send("`Let's not add a double.`")
            
            await ctx.send(f"`Word: {w} being added`\n`Enter a hint/category for the word below:`")
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                hint = await self.client.wait_for('message', check=check, timeout=60)
            except:
                return await ctx.send("`TimeoutError: Word Not added.`")
            
            try:
                wordDict[hint.content].append(w)
            except:
                await ctx.send("`Creating New Category`")

            with open("data/words.json", "w") as OUTFile:
                dump(wordDict, OUTFile, indent="  ")
            wordChannel = self.client.get_channel(792539728993320989)
            await wordChannel.send(f"`New Word Added: {w} - {hint.content}`")
            return await ctx.send("`Word was added.`")

    async def adminCheck(self, ctx):
        if ctx.author.id not in self.admins:
            await ctx.channel.send(f"`{ctx.author}" + " is not authorized to run this command.`")
            return True
        return False


def setup(client):
    client.add_cog(admin(client))