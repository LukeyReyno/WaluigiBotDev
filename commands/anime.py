import discord
from discord.ext import commands, tasks
import datetime
import shutil
import requests
import secrets
import json

class anime(commands.Cog):
    def __init__(self, client):
        self.client = client
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

    @commands.command(aliases=["as", "animesearch", "asearch"])
    async def anime_search(self, ctx, *, query):
        response = requests.get(f'https://api.myanimelist.net/v2/anime?q={query}&limit=4', headers={"Authorization":f"Bearer {self.token}"})

        results = response.json()
        resultTitle = results["data"][0]["node"]["title"]

        anime_embed = discord.Embed()
        anime_embed.title = f'Anime Search First Result: {resultTitle}'
        url = f'https://myanimelist.net/anime/{results["data"][0]["node"]["id"]}/{resultTitle}?cat=anime'
        url = url.replace(' ', '_')

        anime_embed.url = url
        anime_embed.set_image(url=f'{results["data"][0]["node"]["main_picture"]["medium"]}')
        anime_embed.color = 0x7027C3
        anime_embed.set_thumbnail(url="https://www.otakutale.com/wp-content/uploads/2015/07/MyAnimeList-Logo.jpg")
        
        anime_embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")

        return await ctx.send(embed=anime_embed)

    @commands.command()
    async def animeTokenRefresh(self, ctx):
        self.reAuthorize()
        print("MAL Token Regenerated and set as current Access Token")

def setup(client):
    client.add_cog(anime(client))