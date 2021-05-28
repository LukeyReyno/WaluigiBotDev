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

    @cog_ext.cog_slash(name="stats", 
        description="displays mentioned user's Waluigi Bot stats", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="mention",
                description="@User",
                option_type=str,
                required=True,
            )
        ])
    async def stats(self, ctx: SlashContext, mention:str):
        user = self.client.get_user(int(mention.strip("<@!>")))

        stats_embed = discord.Embed()
        stats_embed.title = f"Waluigi Bot Stats: {user.name}"
        stats_embed.color = 0x7027C3
        stats_embed.set_thumbnail(url=user.avatar_url)
        stats_embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")

        descript_string = ""
        with open("data/WahNCounter.json", "r") as INFile:
            WahDict = load(INFile)

        if user.id == self.client.user.id:
            cCount = WahDict["command_count"]
            mCount = WahDict["mentions"]
            updateDate = WahDict["upDate"]
            descript_string += f"`COMMAND COUNT: {cCount}`\n"
            descript_string += f"`GUILD COUNT: {len(self.client.guilds)}`\n"
            descript_string += f"`USER COUNT: {len(self.client.users)}`\n"
            descript_string += f"`MENTION COUNT: {mCount}`\n"
            descript_string += f"`UPDATED: {updateDate}`\n"
            stats_embed.description = descript_string
        else:
            games = WahDict["games"]
            rank_score = 0
            for game in games:
                try:
                    game_data = games[game][str(user.id)]
                except:
                    game_data = 0
                descript_string += f"`{game.upper()}: {game_data}`\n"
                if game == "commands":
                    rank_score += int(game_data) // 30
                else:
                    rank_score += int(game_data)
            stats_embed.description = descript_string

            rank = rank_score // 10
            animals = '🐶 🐱 🐭 🐹 🐰 🦊 🐻 🐼 🐨 🐯 🦁 🐮 🐷 🐸 🐵 🐔 🐧 🐦 🐤 🦆 🦅 🦉 🦇 🐺 🐗 🐴 🦄 🐝 🐛 🦋 🐌 🐞 🐜 🦟 🦗 🕷 🦂 🐢 🐍 🦎 🦖 🦕 🐙 🦑 🦐 🦞 🦀 🐡 🐠 🐟 🐬 🐳 🐋 🦈 🐊 🐅 🐆 🦓 🦍 🦧 🐘 🦛 🦏 🐪 🐫 🦒 🦘 🐃 🐂 🐄 🐎 🐖 🐏 🐑 🦙 🐐 🦌 🐕 🐩 🦮 🐕‍🦺 🐈 🐓 🦃 🦚 🦜 🦢 🦩 🕊 🐇 🦝 🦨 🦡 🦦 🦥 🐁 🐀 🐿 🦔 🐉'
            animals_list = animals.split()
            stats_embed.add_field(name=f"Waluigi Bot Rank: {rank}   {animals_list[rank%len(animals_list)]}", value="`Keep using Waluigi Bot to increase Rank`")
        await ctx.send(embed=stats_embed)

def setup(client):
    client.add_cog(sBasic(client))