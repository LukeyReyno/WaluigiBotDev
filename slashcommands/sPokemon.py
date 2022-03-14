import discord
import random

from discord.ext import commands, tasks
from json import *
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.pokemonFuncs import mainPokemonCommand, pokemonImageCommand, pokemonStats
from functions.constants import GUILDS

class sPokemon(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @cog_ext.cog_slash(name="pokemon")
    async def pokemon(self, ctx: SlashContext):
        await ctx.send("This should never ever send.")

    @cog_ext.cog_subcommand(base="pokemon", name="default", 
        description="displays information on a Pokemon", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="name_num",
                description="Pokemon Name or Pokedex Number",
                option_type=str,
                required=False,
            )
        ])
    async def pokemon_default(self, ctx: SlashContext, name_num : str = None):
        if name_num == None:
            name_num = str(random.choice(range(1,899)))
        pokeEmbed = mainPokemonCommand(name_num)
        if pokeEmbed == None:
            return await ctx.send("`Use a valid Pokémon Name or Number [1, 898]`")
        return await ctx.send(embed=pokeEmbed)

    @cog_ext.cog_subcommand(base="pokemon", name="image", 
        description="sends image of a Pokemon", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="name_num",
                description="Pokemon Name or Pokedex Number",
                option_type=str,
                required=False,
            ),
            create_option(
                name="image_type",
                description="Choose an image",
                option_type=4,
                required=False,
                choices=[
                    create_choice(
                        name="official art",
                        value=0
                    ),
                    create_choice(
                        name="front sprite",
                        value=1
                    ),
                    create_choice(
                        name="back sprite",
                        value=2
                    ),
                    create_choice(
                        name="shiny front sprite",
                        value=3
                    ),
                    create_choice(
                        name="shiny back sprite",
                        value=4
                    )
                ]
            )
        ])
    async def pokemon_image(self, ctx: SlashContext, name_num : str = None, image_type : int = None):
        if name_num == None:
            name_num = str(random.choice(range(1,899)))
        if image_type == None:
            image_type = 0

        image = pokemonImageCommand(name_num, image_type)
        if (image == None):
            return await ctx.send("`Use a valid Pokémon Name or Number [1, 898]`")
        return await ctx.send(image)

    @cog_ext.cog_subcommand(base="pokemon", name="popularity", 
        description="displays Top Ten Searched Pokemon", 
        guild_ids=GUILDS
        )
    async def pokemon_popularity(self, ctx: SlashContext):
        statsEmbed = pokemonStats()
        if statsEmbed == None:
            print("Error in PokemonStats Command")
            return await ctx.send("`Unkown Error`")
        return await ctx.send(embed=statsEmbed)

def setup(client):
    client.add_cog(sPokemon(client))