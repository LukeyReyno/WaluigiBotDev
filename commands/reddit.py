import re
import asyncpraw
import discord
import json

from discord.ext import commands, tasks
from functions.redditFuncs import hmmmFunction, redditFunction

class reddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["hmm", "hmmmm"])
    async def hmmm(self, ctx, showEmbed : bool = False):
        result = await hmmmFunction(showEmbed)
        if type(result) == discord.Embed:
            return await ctx.send(embed=result)
        return await ctx.send(result)

    @commands.command()
    async def reddit(self, ctx, sub : str="all", sortType : str="top"):
        return await redditFunction(self.client, ctx, sub, sortType)

def setup(client):
    client.add_cog(reddit(client))