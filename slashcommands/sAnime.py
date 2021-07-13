import discord

from discord.ext import commands, tasks
from json import *
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.animeFuncs import AnimeCredentials, searchAnime, animeStats, ANIME_CREDENTIAL
from functions.constants import GUILDS

class sAnime(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @cog_ext.cog_slash(name="anime")
    async def anime(self, ctx: SlashContext):
        await ctx.send("This should never ever send.")

    @cog_ext.cog_subcommand(base="anime", name="search", 
        description="grabs link of first result from MyAnimeList.com", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="query",
                description="Name of an Anime or Manga",
                option_type=str,
                required=True,
            )
        ])
    async def anime_search(self, ctx: SlashContext, query : str = None):
        anime_embed = searchAnime(ANIME_CREDENTIAL, query)
        if (anime_embed == None):
            return await ctx.send("`Anime Token Error: Bot Needs to Refresh access to MyAnimeList, this may take some time.`")
        return await ctx.send(embed=anime_embed)

    @cog_ext.cog_subcommand(base="anime", name="popularity", 
        description="displays Top Ten Searched Anime", 
        guild_ids=GUILDS
        )
    async def anime_popularity(self, ctx: SlashContext):
        statsEmbed = animeStats()
        if statsEmbed == None:
            print("Error in AnimeStats Command")
            return await ctx.send("`Unkown Error`")
        return await ctx.send(embed=statsEmbed)

def setup(client):
    client.add_cog(sAnime(client))