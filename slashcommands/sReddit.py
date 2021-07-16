import re
import asyncpraw
import discord
import json

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.constants import GUILDS
from urllib.request import urlopen
from bs4 import BeautifulSoup
from functions.redditFuncs import hmmmFunction, redditFunction

class sReddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="hmmm", 
        description="grabs a random image from r/hmmm", 
        guild_ids=GUILDS,
        options=[
            create_option(
                name="show_embed",
                description="View the full Reddit post",
                option_type=bool,
                required=False
            )
        ])
    async def hmmm(self, ctx: SlashContext, showEmbed: bool = False):
        await ctx.defer()
        result = await hmmmFunction(showEmbed)
        if type(result) == discord.Embed:
            return await ctx.send(embed=result)
        return await ctx.send(result)
    
    @cog_ext.cog_slash(name="reddit", 
        description="grabs top post from chosen subreddit", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="subreddit",
                description="Non-Private Valid Subreddit",
                option_type=str,
                required=True,
            ),
            create_option(
                name="sort_type",
                description="Gets the first post using a different sort option",
                option_type=str,
                required=False,
                choices=[
                    create_choice(
                        name="random",
                        value="random"
                    ),
                    create_choice(
                        name="controversial",
                        value="controversial"
                    ),
                    create_choice(
                        name="hot",
                        value="hot"
                    ),
                    create_choice(
                        name="new",
                        value="new"
                    ),
                    create_choice(
                        name="top",
                        value="top"
                    )
                ]
            )
        ])
    async def reddit(self, ctx: SlashContext, sub : str="all", sortType : str="top"):
        await ctx.defer()
        return await redditFunction(None, ctx, sub, sortType)

def setup(client):
    client.add_cog(sReddit(client))