import discord
import random

from discord.ext import commands, tasks
from json import *
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.pokemonFuncs import mainPokemonCommand, pokemonStats
from functions.constants import GUILDS

with open("data/compendiumImages.txt") as f:
    imageList = f.read().splitlines()

with open("data/hyruleCompendium.json") as j:
    compendiumList = load(j)
    nameList = []
    for dict in compendiumList:
        nameList.append(dict["name"])

class sPokemon(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @cog_ext.cog_slash(name="pokemon", 
        description="displays information on a Pokemon", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="name_number",
                description="Pokemon Name or Pokedex Number",
                option_type=str,
                required=False,
            )
        ])
    async def pokemon(self, ctx: SlashContext, name_num : str = None):
        if name_num == None:
            name_num = str(random.choice(range(1,899)))
        pokeEmbed = mainPokemonCommand(name_num)
        if pokeEmbed == None:
            return await ctx.send("`Use a valid Pokémon Name or Number [1, 898]`")
        return await ctx.send(embed=pokeEmbed)

    @cog_ext.cog_slash(name="pokemonStats", 
        description="displays Top Ten Searched Pokemon", 
        guild_ids=GUILDS
        )
    async def pokemonStats(self, ctx: SlashContext):
        statsEmbed = pokemonStats()
        if statsEmbed == None:
            print("Error in PokemonStats Command")
            return await ctx.send("`Unkown Error`")
        return await ctx.send(embed=statsEmbed)

def setup(client):
    client.add_cog(sPokemon(client))