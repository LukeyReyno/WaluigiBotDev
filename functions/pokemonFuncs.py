import discord
import pokebase

from json import *
from functions.constants import POKEMON_STATS_FILE

MIN_POKE_ID = 1
MAX_POKE_ID = 898

def getBaseEmbed():
    embed = discord.Embed()
    embed.color = 0x7027C3
    embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")

    return embed

def getOfficialArt(pokemonID : int):
    if pokemonID < 10:
        numStr = "0"+"0"+str(pokemonID)
    elif pokemonID < 100:
        numStr = "0"+str(pokemonID)
    else:
        numStr = str(pokemonID)

    return "https://assets.pokemon.com/assets/cms2/img/pokedex/full/%s.png" % numStr

def getArt(image_type : int, pokemonID : int, pokemonObject):
    artList = [
        getOfficialArt(pokemonID),
        pokemonObject.sprites.front_default,
        pokemonObject.sprites.back_default,
        pokemonObject.sprites.front_shiny,
        pokemonObject.sprites.back_shiny,
        ]
    return artList[image_type]

def incrementPokemonJson(pokeObject):
    with open(POKEMON_STATS_FILE, "r") as INFile:
        pokeDict = load(INFile)
    try:
        pokeDict[pokeObject.name] += 1
    except:
        pokeDict[pokeObject.name] = 1
    with open(POKEMON_STATS_FILE, "w") as OUTFile:
        dump(pokeDict, OUTFile, indent="  ")

def getPokemonObject(name_num : str) -> tuple:
    if (name_num.isdigit()):
        pokeID = int(name_num)
        if (pokeID < MIN_POKE_ID or pokeID > MAX_POKE_ID):
            return None
        pokeObject = pokebase.pokemon(int(name_num))
    else:
        pokeObject = pokebase.pokemon(name_num.lower())
        try:
            pokeID = pokeObject.id
        except:
            return None
    return (pokeObject, pokeID)

def mainPokemonCommand(name_num : str):
    descript_string = ""
    pokemon_embed = getBaseEmbed()

    pokeTuple = getPokemonObject(name_num)
    if (pokeTuple == None):
        return None
    pokeObject = pokeTuple[0]
    pokeID = pokeTuple[1]

    pokemon_embed.set_image(url=getOfficialArt(pokeID))
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

    incrementPokemonJson(pokeObject)

    return pokemon_embed

def pokemonImageCommand(name_num : str, image_type : int):
    pokeTuple = getPokemonObject(name_num)
    if (pokeTuple == None):
        return None
    pokeObject = pokeTuple[0]
    pokeID = pokeTuple[1]

    incrementPokemonJson(pokeObject)

    return getArt(image_type, pokeID, pokeObject)

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