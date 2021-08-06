import re
import discord
from discord.channel import DMChannel
import discord.ext.commands.context as C
import discord_slash.context as S
import asyncpraw
import json

from functions.general import getResponse
from urllib.request import urlopen
from bs4 import BeautifulSoup

cInfo = json.load(open("data/redditClient.json"))
redditClient = asyncpraw.Reddit(
    client_id = cInfo["client_id"], 
    client_secret = cInfo["client_secret"], 
    user_agent = cInfo["user_agent"]
    )

def getBaseEmbed(submission : asyncpraw.reddit.Submission):
    reddit_embed = discord.Embed()
    reddit_embed.url = f"https://www.reddit.com{submission.permalink}"
    reddit_embed.color = 0x7027C3
    reddit_embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")
    reddit_embed.add_field(name=f"{submission.title}\nfrom user {submission.author}"[:250], value=f"`💬 Comments: {submission.num_comments}`\n`⬆️ Upvotes: {submission.score}`")

    return reddit_embed

async def hmmmFunction(showEmbed : bool = False):
    #posts a random picture from the subreddit r/hmmm
    try:
        subreddit = await redditClient.subreddit("hmmm", fetch=True)
        submission = await subreddit.random()
        if submission.over_18:
            return "`This r/hmmm image is marked as nsfw`\n" \
                f"|| {submission.url} ||"
        if showEmbed == False:
            return submission.url
        reddit_embed = getBaseEmbed(submission)
        reddit_embed.title = f"Random hmmm post"
        reddit_embed.set_image(url=submission.url)
        return reddit_embed
    except Exception as e:
        print(e)
        return "`No post found`"

async def redditFunction(discordClient, ctx, sub : str, sortType: str):
    try:
        if sub[:2] == "r/": #command works with r/subreddit parameters
            sub = sub[2:] 
        subreddit: asyncpraw.reddit.Subreddit = await redditClient.subreddit(sub.lower(), fetch=True)
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
        if submission == None:
            return await ctx.send("`No post found`")

        if submission.over_18 and (type(ctx.channel) == DMChannel or ctx.channel.is_nsfw()) == False:
            if type(ctx) == S.SlashContext:
                return await ctx.send("`This post has been marked as NSFW use "
                    "'wah reddit [subreddit]' instead of the slash command`")
            else:
                await ctx.send("`This post has been marked as NSFW respond with 'yes' within 60 seconds to view`")
                response = await getResponse(discordClient, ctx)
                if response.content.lower() != 'yes':
                    return await ctx.send("`Post will not be shown.`")
            
        if submission.spoiler and type(ctx) == C.Context:
            await ctx.send("`This post has been marked as a spoiler respond with 'yes' within 60 seconds to view`")
            response = await getResponse(discordClient, ctx)
            if response.content.lower() != 'yes':
                return await ctx.send("`Post will not be shown.`")
        
        # Discord Embed Initialization
        reddit_embed = getBaseEmbed(submission)
        reddit_embed.title = f"{sortType} r/{sub} post"
        
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
        return await ctx.send(f"`Error: {e}`")