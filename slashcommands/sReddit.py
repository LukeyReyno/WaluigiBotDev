import re
import asyncpraw
import discord
import json

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from WaluigiBotDev import GUILDS
from urllib.request import urlopen
from bs4 import BeautifulSoup

cInfo = json.load(open("data/redditClient.json"))
redditClient = asyncpraw.Reddit(
    client_id = cInfo["client_id"], 
    client_secret = cInfo["client_secret"], 
    user_agent = cInfo["user_agent"]
    )

class sReddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="hmmm", description="grabs a random image from r/hmmm", guild_ids=GUILDS)
    async def hmmm(self, ctx):
        #posts a random picture from the subreddit r/hmmm
        try:
            subreddit = await redditClient.subreddit("hmmm", fetch=True)
            submission = await subreddit.random()
        
            return await ctx.send(submission.url)
        except Exception as e:
            print(e)
            return await ctx.send(f"`Error: No post found. Try again Later.`")
    
    @cog_ext.cog_slash(name="reddit", 
        description="grabs top post from chosen subreddit", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="Subreddit",
                description="Non-Private Valid Subreddit",
                option_type=str,
                required=True,
            ),
            create_option(
                name="Sort_Type",
                description="'random', 'controversial', 'hot', 'new', or 'top'",
                option_type=str,
                required=False,
            )
        ])
    async def reddit(self, ctx, sub : str="all", sortType : str="top"):
        try:
            if sub[:2] == "r/": #command works with r/subreddit parameters
               sub = sub[2:] 
            subreddit = await redditClient.subreddit(sub.lower(), fetch=True)
            if sortType == "random":
                submission = await subreddit.random()
            else:
                if sortType == "controversial":
                    submissions = subreddit.controversial(limit=5, time_filter="day")
                elif sortType == "hot":
                    submissions = subreddit.hot(limit=5)
                elif sortType == "new":
                    submissions = subreddit.new(limit=5)
                elif sortType == "top":
                    submissions = subreddit.top(limit=5, time_filter="day")
                else:
                    await ctx.send("`Invalid Sort Type, using Top of today`")
                    sortType = "top"
                    submissions = subreddit.top(limit=5, time_filter="day")
                submission = None
                async for submission in submissions:
                    if not submission.stickied:
                        break

            if submission.over_18 and ctx.channel.is_nsfw() == False:
                return await ctx.send("`This post has been marked as NSFW use "
                    "'wah reddit [subreddit]' instead of the slash command`")
            
            # Discord Embed Initialization
            reddit_embed = discord.Embed()
            reddit_embed.title = f"{sortType} r/{sub} post"
            reddit_embed.url = f"https://www.reddit.com{submission.permalink}"
            reddit_embed.color = 0x7027C3
            reddit_embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")
            reddit_embed.add_field(name=f"{submission.title}\nfrom user {submission.author}"[:250], value=f"`💬 Comments: {submission.num_comments}`\n`⬆️ Upvotes: {submission.score}`")
            
            # Discord Embed Body Setup
            if submission.url[8:11] == 'i.r':
                reddit_embed.set_image(url=submission.url)
            elif submission.url[23:30] == "gallery": #grabs first image in a gallery
                page = BeautifulSoup(urlopen(submission.url), features="html.parser")
                image = BeautifulSoup(str(page.findAll('img', alt=re.compile("r/"))[0]), "html.parser")
                reddit_embed.set_image(url=image.img["src"])
                await ctx.send(submission.url)
            else:
                if len(submission.selftext) < 1500:
                    reddit_embed.description = f"{submission.url}\n\n{submission.selftext}"
                else:
                    reddit_embed.description = f"{submission.url}"
                    
                if reddit_embed.url != submission.url: #sends link if link isn't the post
                    await ctx.send(submission.url)

            # Discord Embed Thumbnail setup
            if subreddit.community_icon != "":
                reddit_embed.set_thumbnail(url = subreddit.community_icon)
            elif subreddit.icon_img != None:
                reddit_embed.set_thumbnail(url = subreddit.icon_img)
            else:#occurs when subreddit has no icon or is unretrievable
                reddit_embed.set_thumbnail(url = "https://www.redditstatic.com/avatars/avatar_default_04_FF4500.png")

            return await ctx.send(embed=reddit_embed)
        except Exception as e:
            print(e)
            await ctx.send(f"`Error: {e}`")
            return await ctx.send(f"`No post found.\nTry a different subreddit and make sure the bot has permissions to embed links`")

def setup(client):
    client.add_cog(sReddit(client))