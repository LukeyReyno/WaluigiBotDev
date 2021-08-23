from discord.ext import commands
from functions.twitterFuncs import fetchMostRecentTweetURL

class twitter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tweet(self, ctx, *, query):
        results = fetchMostRecentTweetURL(query)
        return await ctx.send(results)

def setup(client):
    client.add_cog(twitter(client))