import discord
import WaluigiBot
import asyncio

from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.statsFuncs import waluigiBotStats, userStats
from functions.constants import GUILDS
from json import *

class sStats(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    @cog_ext.cog_slash(name="stats", 
        description="displays mentioned user's Waluigi Bot stats", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="user",
                description="@User",
                option_type=6,
                required=True,
            )
        ])
    async def stats(self, ctx: SlashContext, user: discord.User):
        if (type(user) == str):
            user = self.client.get_user(int(user))
        if user.id == self.client.user.id:
            stats_embed = waluigiBotStats(user, len(self.client.guilds), len(self.client.users))
        else:
            stats_embed = userStats(user)
        await ctx.send(embed=stats_embed)

def setup(client):
    client.add_cog(sStats(client))