import discord
from discord import embeds
from discord.embeds import Embed

from discord.ext import commands, tasks
from functions.animeFuncs import randomAnime, searchAnime, animeStats, ANIME_CREDENTIAL

class anime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["as", "animesearch", "anime_search", "asearch"])
    async def anime(self, ctx, *, query):
        if query == "random":
            anime_embed = randomAnime(ANIME_CREDENTIAL)
        else:
            anime_embed = searchAnime(ANIME_CREDENTIAL, query)
        if (anime_embed == None):
            return await ctx.send("`Anime Token Error: Bot Needs to Refresh access to MyAnimeList, this may take some time.`")
        return await ctx.send(embed=anime_embed)

    @commands.command(aliases=["animeStats"])
    async def anime_stats(self, ctx):
        statsEmbed = animeStats()
        if statsEmbed == None:
            print("Error in anime_stats Command")
            return await ctx.send("`Unkown Error`")
        return await ctx.send(embed=statsEmbed)

    @commands.command()
    async def animeTokenRefresh(self, ctx):
        ANIME_CREDENTIAL.reAuthorize()
        print("MAL Token Regenerated and set as current Access Token")
        return await ctx.send("`Check the Logs for anime refresh errors`")

def setup(client):
    client.add_cog(anime(client))