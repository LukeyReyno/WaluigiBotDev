from discord.ext import commands
from functions.twitterFuncs import fetchMostRecentTweetURL, getTweetURLFromHashtag

class twitter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["tweet"])
    async def twitter(self, ctx, *, query):
        results = fetchMostRecentTweetURL(query)
        return await ctx.send(results)

    @commands.command()
    async def hashtag(self, ctx, *, query):
        results = getTweetURLFromHashtag(query)
        return await ctx.send(results)

def setup(client):
    client.add_cog(twitter(client))
