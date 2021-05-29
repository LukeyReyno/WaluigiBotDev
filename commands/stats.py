from discord.ext import commands, tasks
from json import *
from functions.statsFuncs import waluigiBotStats, userStats

class stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx):
        if len(ctx.message.mentions) == 0:
            await ctx.send("`You must @mention someone`")
            return await ctx.send("Example: `wah stats @Waluigi Bot`")

        user = ctx.message.mentions[0]

        if user.id == self.client.user.id:
            stats_embed = waluigiBotStats(user, len(self.client.guilds), len(self.client.users))
        else:
            stats_embed = userStats(user)
        await ctx.send(embed=stats_embed)

def setup(client):
    client.add_cog(stats(client))