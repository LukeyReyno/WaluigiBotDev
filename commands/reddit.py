import re
import asyncpraw
import discord
import json

from discord.ext import commands, tasks
from functions.redditFuncs import imageFunction, redditFunction
from discord_slash.utils.manage_components import *

class reddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["hmm", "hmmmm"])
    async def hmmm(self, ctx, showEmbed : bool = False):
        result = await imageFunction(showEmbed=showEmbed)
        if type(result) == discord.Embed:
            return await ctx.send(embed=result)
        return await ctx.send(result)

    @commands.command(aliases=["picture"])
    async def pic(self, ctx, showEmbed : bool = False):
        select = create_select(
            options=[# the options in your dropdown
                create_select_option("Hmmm", value="hmmm", emoji="🤔"),
                create_select_option("Meme", value="meme", emoji="🤡"),
                create_select_option("Art", value="art", emoji="🎨"),
                create_select_option("Photography", value="photos", emoji="📷"),
                create_select_option("Random Gifs", value="gifs", emoji="❓")
            ],
            placeholder="Choose your option",  # the placeholder text to show when no options have been chosen
            min_values=1,  # the minimum number of options a user must select
            max_values=1,  # the maximum number of options a user can select
        )

        action_row = create_actionrow(select)
        await ctx.send("`Choose to receive a type of image:`", components=[action_row])

        select_ctx: ComponentContext = await wait_for_component(self.client, components=action_row)
        await select_ctx.defer(edit_origin=True)
        selectValue = select_ctx.values[0]

        result = await imageFunction(selectValue, showEmbed)
        if type(result) == discord.Embed:
            return await select_ctx.edit_origin(content=f"`You selected {selectValue}`", embed=result, components=None)
        await select_ctx.edit_origin(content=f"`You selected {selectValue}`\n{result}", components=None)

    @commands.command()
    async def reddit(self, ctx, sub : str="all", sortType : str="top"):
        return await redditFunction(self.client, ctx, sub, sortType)

def setup(client):
    client.add_cog(reddit(client))