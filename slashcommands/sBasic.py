import random
import discord

from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.dailyRequests import dailyCommandFunction
from functions.constants import GUILDS
from json import *

class sBasic(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="random")
    async def random(self, ctx: SlashContext):
        await ctx.send("This should never ever send.")

    @cog_ext.cog_subcommand(base="random", name="coinflip", description="Flips for heads or tails", guild_ids=GUILDS)
    async def random_flip(self, ctx: SlashContext):
        results = ["`Heads`", "`Tails`"]
        return await ctx.send(random.choice(results))

    @cog_ext.cog_subcommand(base="random", name="diceroll", description="Rolls a 6 sided die", guild_ids=GUILDS)
    async def random_roll(self, ctx: SlashContext):
        result = random.choice(range(1,7))
        return await ctx.send(f"`{result}`")

    @cog_ext.cog_slash(name="consume", description="Sends a random Food and Animal Emoji", guild_ids=GUILDS)
    async def consume(self, ctx: SlashContext):
        foods = '🍏 🍎 🍐 🍊 🍋 🍌 🍉 🍇 🍓 🍈 🍒 🍑 🥭 🍍 🥥 🥝 🍅 🍆 🥑 🥦 🥬 🥒 🌶 🌽 🥕 🧄 🧅 🥔 🍠 🥐 🥯 🍞 🥖 🥨 🧀 🥚 🍳 🧈 🥞 🧇 🥓 🥩 🍗 🍖 🦴 🌭 🍔 🍟 🍕 🥪 🥙 🧆 🌮 🌯 🥗 🥘 🥫 🍝 🍜 🍲 🍛 🍣 🍱 🥟 🦪 🍤 🍙 🍚 🍘 🍥 🥠 🥮 🍢 🍡 🍧 🍨 🍦 🥧 🧁 🍰 🎂 🍮 🍭 🍬 🍫 🍿 🍩 🍪 🌰 🥜 🍯 🥛 🍼 🍵 🧃 🥤 🍶 🍺 🍻 🥂 🍷 🥃 🍸 🍹 🧉 🍾 🧊 :poop:'
        food_list = foods.split()
        animals = '🐶 🐱 🐭 🐹 🐰 🦊 🐻 🐼 🐨 🐯 🦁 🐮 🐷 🐸 🐵 🐔 🐧 🐦 🐤 🦆 🦅 🦉 🦇 🐺 🐗 🐴 🦄 🐝 🐛 🦋 🐌 🐞 🐜 🦟 🦗 🕷 🦂 🐢 🐍 🦎 🦖 🦕 🐙 🦑 🦐 🦞 🦀 🐡 🐠 🐟 🐬 🐳 🐋 🦈 🐊 🐅 🐆 🦓 🦍 🦧 🐘 🦛 🦏 🐪 🐫 🦒 🦘 🐃 🐂 🐄 🐎 🐖 🐏 🐑 🦙 🐐 🦌 🐕 🐩 🦮 🐕‍🦺 🐈 🐓 🦃 🦚 🦜 🦢 🦩 🕊 🐇 🦝 🦨 🦡 🦦 🦥 🐁 🐀 🐿 🦔 🐉'
        animals_list = animals.split()
        return await ctx.send(f'{random.choice(food_list)}{random.choice(animals_list)}')

    @cog_ext.cog_slash(name="daily", 
        description="sets up a daily message for bot to send", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="daily_type",
                description="Decide what kind of message for bot to send each day",
                option_type=str,
                required=True,
                choices=[
                    create_choice(
                        name="song",
                        value="song"
                    ),
                    create_choice(
                        name="stat",
                        value="stat"
                    ),
                    create_choice(
                        name="hmmm",
                        value="hmmm"
                    ),
                    create_choice(
                        name="pokemon",
                        value="pokemon"
                    ),
                    create_choice(
                        name="botw",
                        value="botw"
                    ),
                    create_choice(
                        name="info",
                        value="info"
                    )
                ]
            )
        ])
    async def daily(self, ctx: SlashContext, dailyType : str = None):
        await ctx.defer()
        return await dailyCommandFunction(self.client, ctx, dailyType)

def setup(client):
    client.add_cog(sBasic(client))
