import discord
import pokebase

from json import *
from functions.constants import POKEMON_STATS_FILE

def getBaseEmbed():
    stats_embed = discord.Embed()
    stats_embed.color = 0x7027C3
    stats_embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")

    return stats_embed

def mainPokemonCommand(name_num : str):
    descript_string = ""
    pokemon_embed = getBaseEmbed()

    if (name_num.isdigit()):
        pokeObject = pokebase.pokemon(int(name_num))
    else:
        pokeObject = pokebase.pokemon(name_num.lower())

    try:
        pokeID = pokeObject.id
    except:
        return None

    if pokeID < 10:
        name_num = "0"+"0"+str(pokeID)
    elif pokeID < 100:
        name_num = "0"+str(pokeID)
    else:
        name_num = str(pokeID)

    pokemon_embed.set_image(url="https://assets.pokemon.com/assets/cms2/img/pokedex/full/%s.png" % name_num)
    pokemon_embed.set_thumbnail(url=pokeObject.sprites.front_default)
    pokemon_embed.title = f"Pokémon: {pokeObject.name.upper()}\nNumber: {name_num}"
    
    pokemon_embed.description = "```TYPE: "
    i = 0
    while i < len(pokeObject.types):
        if (i > 0):
            pokemon_embed.description += ", "
        pokemon_embed.description += pokeObject.types[i].type.name.upper()
        i += 1

    pokemon_embed.description += "\n\nABILITY: "
    i = 0
    while i < len(pokeObject.abilities):
        if (i > 0):
            pokemon_embed.description += ", "
        pokemon_embed.description += pokeObject.abilities[i].ability.name.upper()
        i += 1
    #pokemon_embed.description += f"\nHEIGHT: {pokeObject.height}"
    #pokemon_embed.description += f"\nWEIGHT: {pokeObject.weight}"
    pokemon_embed.description += "```"

    with open(POKEMON_STATS_FILE, "r") as INFile:
        pokeDict = load(INFile)
    try:
        pokeDict[pokeObject.name] += 1
    except:
        pokeDict[pokeObject.name] = 1
    with open(POKEMON_STATS_FILE, "w") as OUTFile:
        dump(pokeDict, OUTFile, indent="  ")

    return pokemon_embed

def pokemonStats():
    descript_string = ""
    stats_embed = getBaseEmbed()
    
    with open(POKEMON_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)

    tupleSortValues = sorted(WahDict.items(), key=lambda item: item[1])
    tupleSortValues.reverse()
    commandSorted = {key: value for key, value in tupleSortValues}
    WahDict = commandSorted
    
    descript_string += "```"

    i = 1
    for comm in commandSorted:
        descript_string += f"{i:2d}. {comm.upper():12s}  {commandSorted[comm]:7d}\n"
        i += 1
        if i > 10:
            break
    with open(POKEMON_STATS_FILE, "w") as OUTFile:
        dump(WahDict, OUTFile, indent="  ")
    descript_string += "```"

    stats_embed.description = descript_string
    stats_embed.title = "Top Ten Pokémon Searched"
    stats_embed.set_thumbnail(url="https://pngimg.com/uploads/pokeball/pokeball_PNG21.png")

    return stats_embed