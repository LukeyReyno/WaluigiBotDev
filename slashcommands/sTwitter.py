import discord

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.constants import GUILDS
from functions.twitterFuncs import fetchMostRecentTweetURL

class sTwitter(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="twitter")
    async def twitter(self, ctx: SlashContext):
        await ctx.send("This should never ever send.")

    @cog_ext.cog_subcommand(base="twitter", name="search",
        description="posts a link of found user's most recent tweet", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="username",
                description="user's Twitter name",
                option_type=str,
                required=True,
            )
        ])
    async def twitter_search(self, ctx: SlashContext, username: str):
        await ctx.defer()
        results = fetchMostRecentTweetURL(username)
        return await ctx.send(results)

def setup(client):
    client.add_cog(sTwitter(client))
