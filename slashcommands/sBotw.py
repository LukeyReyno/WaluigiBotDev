import discord

from discord.ext import commands, tasks
from json import *
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.botwFuncs import botwFunction
from functions.constants import GUILDS

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
        result = botwFunction(name_num)
        if type(result) == discord.Embed:
            return await ctx.send(embed=result)
        return await ctx.send(result)

def setup(client):
    client.add_cog(sBotw(client))