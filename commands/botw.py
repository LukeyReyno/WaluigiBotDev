import discord

from discord.ext import commands, tasks
from json import *
from functions.botwFuncs import botwFunction

class botw(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def botw(self, ctx, *, name_num=None):
        result = botwFunction(name_num)
        if type(result) == discord.Embed:
            return await ctx.send(embed=result)
        return await ctx.send(result)

def setup(client):
    client.add_cog(botw(client))