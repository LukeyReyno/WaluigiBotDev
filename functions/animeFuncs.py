import discord
import pokebase
import json
import requests

from functions.constants import ANIME_STATS_FILE

class AnimeCredentials():

    def __init__(self):
        cred = json.load(open("data/MALCred.json"))
        self.client_id = cred["CLIENT_ID"]
        self.client_secret = cred["CLIENT_SECRET"]

        tokenJson = json.load(open("data/token.json"))
        self.refresh_token = tokenJson["refresh_token"]
        self.token = tokenJson["access_token"]
        self.reAuthorize()

    def reAuthorize(self):
    
        params = {
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token
        }

        authorization_url = "https://myanimelist.net/v1/oauth2/token"

        r = requests.post(authorization_url, data=params)

        if r.ok:
                with open("data/token.json", 'w') as tokenFile:
                    json.dump(r.json(), tokenFile, indent=4)
                self.token = r.json()['access_token']
                return None
        else:
                print("Error Rehreshing Token for MAL")
                return None

ANIME_CREDENTIAL = AnimeCredentials()

def getBaseEmbed():
    embed = discord.Embed()
    embed.color = 0x7027C3
    embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")
    embed.set_thumbnail(url="http://d3ieicw58ybon5.cloudfront.net/ex/610.191/u/c2ea270de7764fb1a92f60080d27b0da.jpg")

    return embed

def searchAnime(animeCreds, query):
    response = requests.get(f'https://api.myanimelist.net/v2/anime?q={query}&limit=4', headers={"Authorization":f"Bearer {animeCreds.token}"})
    print(response)
    results = response.json()
    try:
        resultTitle = results["data"][0]["node"]["title"]
    except:
        return None
    
    incrementAnimeJson(resultTitle)

    anime_embed = getBaseEmbed()
    anime_embed.title = f'Anime Search First Result: {resultTitle}'
    url = f'https://myanimelist.net/anime/{results["data"][0]["node"]["id"]}/{resultTitle}?cat=anime'
    url = url.replace(' ', '_')

    anime_embed.url = url
    anime_embed.set_image(url=f'{results["data"][0]["node"]["main_picture"]["medium"]}')

    return anime_embed

def incrementAnimeJson(resultTitle):
    with open(ANIME_STATS_FILE, "r") as INFile:
        animeDict = json.load(INFile)
    try:
        animeDict[resultTitle.lower()] += 1
    except:
        animeDict[resultTitle.lower()] = 1
    with open(ANIME_STATS_FILE, "w") as OUTFile:
        json.dump(animeDict, OUTFile, indent="  ")


def animeStats():
    descript_string = ""
    stats_embed = getBaseEmbed()
    
    with open(ANIME_STATS_FILE, "r") as INFile:
        WahDict = json.load(INFile)

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
    with open(ANIME_STATS_FILE, "w") as OUTFile:
        json.dump(WahDict, OUTFile, indent="  ")
    descript_string += "```"

    stats_embed.description = descript_string
    stats_embed.title = "Top Ten Anime Searched"

    return stats_embed