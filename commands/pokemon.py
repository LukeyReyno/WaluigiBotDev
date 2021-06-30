from os import name
import discord
import random
import pokebase

from discord.ext import commands
from json import *
from functions.pokemonFuncs import mainPokemonCommand, pokemonStats

class pokemon(commands.Cog):
    @commands.command()
    async def pokemon(self, ctx, name_num : str = None):
        if name_num == None:
            name_num = str(random.choice(range(1,899)))
        pokeEmbed = mainPokemonCommand(name_num)
        if pokeEmbed == None:
            return await ctx.send("`Use a valid Pokémon Name or Number [1, 898]`")
        return await ctx.send(embed=pokeEmbed)

    @commands.command()
    async def pokemonStats(self, ctx):
        statsEmbed = pokemonStats()
        if statsEmbed == None:
            print("Error in PokemonStats Command")
            return await ctx.send("`Unkown Error`")
        return await ctx.send(embed=statsEmbed)

def setup(client):
    client.add_cog(pokemon(client))