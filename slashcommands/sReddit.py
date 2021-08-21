import discord

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.constants import GUILDS
from functions.redditFuncs import imageFunction, redditFunction

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
        result = await imageFunction(showEmbed=showEmbed)
        if type(result) == discord.Embed:
            return await ctx.send(embed=result)
        return await ctx.send(result)

    @cog_ext.cog_slash(name="reddit")
    async def reddit(self, ctx: SlashContext):
        await ctx.send("This should never ever send.")

    @cog_ext.cog_subcommand(base="reddit", name="search",
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
    async def reddit_search(self, ctx: SlashContext, subreddit: str="all", sort_type: str="top"):
        await ctx.defer()
        return await redditFunction(None, ctx, subreddit, sort_type)

    @cog_ext.cog_subcommand(base="reddit", name="picture",
        description="grabs random picture from chosen category", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="category",
                description="Choose a picture type",
                option_type=str,
                required=True,
                choices=[
                    create_choice(
                        name="🤔 Hmmm",
                        value="hmmm"
                    ),
                    create_choice(
                        name="🤡 Meme",
                        value="meme"
                    ),
                    create_choice(
                        name="🎨 Art",
                        value="art"
                    ),
                    create_choice(
                        name="📷 Photography",
                        value="photos"
                    ),
                    create_choice(
                        name="❓ Random Gifs",
                        value="gifs"
                    )
                ]
            )
        ])
    async def reddit_picture(self, ctx: SlashContext, category: str):
        await ctx.defer()
        result = await imageFunction(category, showEmbed=False)
        return await ctx.send(result)

def setup(client):
    client.add_cog(sReddit(client))