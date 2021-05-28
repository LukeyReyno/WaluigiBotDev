import discord
import os
import subprocess
from discord.errors import HTTPException

from discord.ext import commands, tasks

DISCORD_MESSAGE_CHAR_LIMIT = 2000
MESSAGE_HISTORY_LIMIT = 35

async def getMostRecentFile(ctx):
    messages = await ctx.channel.history(limit=MESSAGE_HISTORY_LIMIT).flatten()
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
        my_env = os.environ.copy()
        my_env["PATH"] = my_env["PATH"] + ":/waluigibot/data/CExecutables"
        stdOutput = subprocess.Popen([command, fname], stdout=subprocess.PIPE, env=my_env).communicate()[0]
        stdOutput = stdOutput.decode('utf-8')
        if (len(stdOutput) >= DISCORD_MESSAGE_CHAR_LIMIT):
            outfile = open(outputPath, 'w')
            outfile.write(stdOutput)
            outfile.close()
            destinationFile = discord.File(f"{outputPath}")
            try:
                await ctx.send(f"`{command.upper()} file: `", file=destinationFile)
            except HTTPException as e: #Most likely, file is too large
                if (e.code == 40005):
                    await ctx.send(f"`{command.upper()} tried sending a file that's too big for Discord`")
                else:
                    print(f"{command.upper()}: {e}")
                    await ctx.send(f"`{command.upper()} caused a file error to occurr`")
            os.remove(f"{outputPath}")
        else:
            await ctx.send(f"```{stdOutput}```")
        os.remove(fname)
    else:
        return await ctx.send(f"`No recent files (Last {MESSAGE_HISTORY_LIMIT} messages). Send a new one.`")

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