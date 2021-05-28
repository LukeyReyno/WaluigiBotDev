import random
import discord

from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from WaluigiBot import GUILDS
from json import *

class sBasic(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="pokemon", 
        description="displays an image of a pokemon", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="number",
                description="Pokedex Number",
                option_type=4,
                required=False,
            )
        ])
    async def pokemon(self, ctx: SlashContext, x: int):
        if (x == None):
            x = random.choice(range(1,899))
        if not 0 < int(x) < 899:
            return await ctx.send("`Use a valid Dex Number [1, 898]`")

        if int(x) < 10:
            x = "0"+"0"+str(int(x))
        elif int(x) < 100:
            x = "0"+str(int(x))
        await ctx.send("`Number: %s`\nhttps://assets.pokemon.com/assets/cms2/img/pokedex/full/%s.png" % (x, x))

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

def setup(client):
    client.add_cog(sBasic(client))