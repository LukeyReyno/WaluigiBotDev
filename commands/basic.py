import discord
import random
import WaluigiBotDev

from discord.ext import commands, tasks
from json import *

class basic(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(color = 0x7027C3, title = "Help using 'wah' prefix", url="https://lukeyreyno.github.io/lukeyreyno-website/help.html")
        embed.add_field(name="Basic Commands", value="`help\nhmmm\nfight\nping\nplot\nconsume\ndaily\nclear\npokemon\nbotw`")
        embed.add_field(name="Argument Commands", value="`randomReact [emoji]\ne [custom_emoji]\nanime_search [title]\nstats [@member]\nstatus [@member]\navatar [@member]\ncolor [@member]\njoined [@member]\n8ball [question]?\nligma [reason] \necho [statement]\nreddit [subreddit]`")
        embed.add_field(name="Games", value="`hangman\nwordsearch`")
        embed.add_field(name="Click the link above for some examples", value="`Some commands require Manage Messages or Embed Links Permissions for both BOT and User`")
        embed.add_field(name="Info", value="`Waluigi Bot only stores user and textchannel IDs for game and daily music commands`")
        await ctx.send(embed=embed)

    @commands.command()
    async def plot(self, ctx):
        await ctx.send("`Everyone is plotting against me!!!`")

    @commands.command()
    async def add(self, ctx, a: int, b: int):
        await ctx.send('`{0}`'.format(a + b))

    class Ligma(commands.Converter):
        async def convert(self, ctx, arg):
            receiver = random.choice(ctx.guild.members)
            return '`{0.author.name} gave {1.name} Ligma because {2}`'.format(ctx, receiver, arg)

    @commands.command()
    async def ligma(self, ctx, *, reason: Ligma()):
        await ctx.send(reason)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'`Ping: {round(self.client.latency * 1000)}ms`')

    @commands.command()
    async def song(self, ctx):
        if len(WaluigiBotDev.songs_command) == 0:
            return await ctx.send("`Waluigi Bot has recently been updated wait until ~2PM Pacific to use this command`")
        else:
            return await ctx.send(random.choice(WaluigiBotDev.songs_command))

    @commands.command()
    async def joined(self, ctx, *, member: discord.Member):
        await ctx.send('`{0} joined on {0.joined_at}`'.format(member))

    @commands.command()
    async def pokemon(self, ctx, x = str(random.choice(range(1,899)))):
        if not x.isdigit():
            return await ctx.send("`Use a Pokémon's Dex Number instead`")
        elif not 0 < int(x) < 899:
            return await ctx.send("`Use a valid Dex Number [1, 898]`")

        if int(x) < 10:
            x = "0"+"0"+str(int(x))
        elif int(x) < 100:
            x = "0"+str(int(x))
        await ctx.send("`Number: %s`\nhttps://assets.pokemon.com/assets/cms2/img/pokedex/full/%s.png" % (x, x))

    @commands.command()
    async def consume(self, ctx):
        foods = '🍏 🍎 🍐 🍊 🍋 🍌 🍉 🍇 🍓 🍈 🍒 🍑 🥭 🍍 🥥 🥝 🍅 🍆 🥑 🥦 🥬 🥒 🌶 🌽 🥕 🧄 🧅 🥔 🍠 🥐 🥯 🍞 🥖 🥨 🧀 🥚 🍳 🧈 🥞 🧇 🥓 🥩 🍗 🍖 🦴 🌭 🍔 🍟 🍕 🥪 🥙 🧆 🌮 🌯 🥗 🥘 🥫 🍝 🍜 🍲 🍛 🍣 🍱 🥟 🦪 🍤 🍙 🍚 🍘 🍥 🥠 🥮 🍢 🍡 🍧 🍨 🍦 🥧 🧁 🍰 🎂 🍮 🍭 🍬 🍫 🍿 🍩 🍪 🌰 🥜 🍯 🥛 🍼 🍵 🧃 🥤 🍶 🍺 🍻 🥂 🍷 🥃 🍸 🍹 🧉 🍾 🧊 :poop:'
        food_list = foods.split()
        animals = '🐶 🐱 🐭 🐹 🐰 🦊 🐻 🐼 🐨 🐯 🦁 🐮 🐷 🐸 🐵 🐔 🐧 🐦 🐤 🦆 🦅 🦉 🦇 🐺 🐗 🐴 🦄 🐝 🐛 🦋 🐌 🐞 🐜 🦟 🦗 🕷 🦂 🐢 🐍 🦎 🦖 🦕 🐙 🦑 🦐 🦞 🦀 🐡 🐠 🐟 🐬 🐳 🐋 🦈 🐊 🐅 🐆 🦓 🦍 🦧 🐘 🦛 🦏 🐪 🐫 🦒 🦘 🐃 🐂 🐄 🐎 🐖 🐏 🐑 🦙 🐐 🦌 🐕 🐩 🦮 🐕‍🦺 🐈 🐓 🦃 🦚 🦜 🦢 🦩 🕊 🐇 🦝 🦨 🦡 🦦 🦥 🐁 🐀 🐿 🦔 🐉'
        animals_list = animals.split()
        await ctx.send(f'{random.choice(food_list)}{random.choice(animals_list)}')

    @commands.command(aliases=["8ball", "8-ball"])
    async def _8ball(self, ctx, *, question):
        ballarray = ["`Yes, definitely`", "`Why don't you figure that out for yourself.`", "`How 'bout no?`", "`Perhaps.`", ":regional_indicator_n::regional_indicator_o:", "`Yeet!`", "`Ask me later.`", "`Yes`",
                        "`No`", "`Well yes, but actually no`", ":regional_indicator_y::regional_indicator_e::regional_indicator_s:", "`Nah bruh`", "`Signs point to yes`", "`My sources say no`", "`I'm not going to tell you`",
                        "`Without a doubt`", "`Cannot predict now`", "`Outlook not so good`", "`I think it best not to tell you`", "`Is Waluigi in smash?`"]
        response = random.choice(ballarray)
        msg = ctx.message.content.split()
        msg = msg[2:]
        msg = ' '.join(msg)
        '''if msg == '':  # Returns if no question is asked
            return await ctx.send(content="`Please ask a question.`")'''
        if msg[-1] != '?' or len(msg) < 5:
            return await ctx.send(content="`Bruh that's a stupid question.`")
        await ctx.send('`{0.author.name} asked: {1}`\n\n `{2}`'.format(ctx, msg, response))

    @commands.command()
    async def clear(self, ctx, amount: int=2):
        if ctx.channel.permissions_for(ctx.author).manage_messages:
            return await ctx.channel.purge(limit=amount)
        elif not ctx.channel.permissions_for(ctx.guild.get_member(self.client.user.id)).manage_messages:
            return await ctx.send("`I don't have the manage messages permission in this channel`")
        return await ctx.send("`You don't have the manage messages permission in this channel`")

    @commands.command()
    async def question(self, ctx):
        auth = ctx.author
        await ctx.send("`Do you like to play Fall Guys?`")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            response = await self.client.wait_for('message', check=check, timeout=60)
        except:
            return await ctx.send("`TimeoutError: No changes have been made.`")
        if response.content.lower() == "yes":
            await ctx.send("`Cool, I like falling`")
        elif response.content.lower() == "no":
            await ctx.send("`Maybe it's because you're bad`")
        else:
            await ctx.send("`hmmmm`")

    @commands.command()
    async def embed(self, ctx):
        auth = ctx.author
        em = discord.Embed()
        em.description = "Waluigi Bot Embed"
        em.title = "Waluigi"
        em.color = 0x7027C3
        em.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")
        em.set_image(url="https://lukeyreyno.github.io/lukeyreyno/pictures/smg.jpeg")
        embmsg = await ctx.send(embed=em)
        e = embmsg.embeds[0]
        e.set_image(url="https://lukeyreyno.github.io/lukeyreyno/pictures/Hangman.6.png")
        e.add_field(name="Jeff", value="Zut Geaugh\nNow this is Epic!!!")
        await ctx.send("`Do you like to play Fall Guys?`")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            response = await self.client.wait_for('message', check=check, timeout=60)
        except:
            return await ctx.send("`TimeoutError: No changes have been made.`")
        if response.content.lower() == "yes":
            await embmsg.edit(embed=e)

    @commands.command()
    async def fight(self, ctx):
        results = ["after they land a critical hit.", "after they use a mori.", "with one HP remaining.", "after summoning zut geaugh.", "by yeeting them with a rock.", 
            "with the power within.", "because they used wall hacks.", "because of their determination.", "without breaking a sweat."]
        #await ctx.guild.fetch_members(limit=150).flatten()
        opponent =  random.choice(ctx.guild.members)
        while opponent == ctx.author:
            opponent = random.choice(ctx.guild.members)
        fighters = [ctx.author, opponent]
        winner = random.choice(fighters)
        loser = fighters[fighters.index(winner)-1]
        await ctx.send(f"`{winner.name} wins the 1v1 against {loser.name} {random.choice(results)}`")

    @commands.command()
    async def react(self, ctx):
        msg = await ctx.send("Ligma")
        await msg.add_reaction("🐸")

    @commands.command()
    async def echo(self, ctx, *, string):
        results = ""
        s = string.split()
        if s[0] == "-d":
            string = " ".join(s[1:])
            try:
                await ctx.message.delete()
            except:
                await ctx.send("`Missing Some Permissions`")
        for char in string:
            if char.isalpha():
                results += f":regional_indicator_{char.lower()}:"
                continue
            if char.isdigit():
                numList = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:",
                    ":six:", ":seven:", ":eight:", ":nine:"]
                results += numList[int(char)]
                continue
            elif char == " ":
                results += "  "
                continue
            elif char == ".":
                results += ":record_button:"
                continue
            elif char == "!":
                results += ":exclamation:"
                continue
            elif char == "?":
                results += ":question:"
                continue
            else:
                results += char
        await ctx.send(results)

    @commands.command()
    async def daily(self, ctx):
        sendPerms = ctx.channel.permissions_for(await ctx.guild.fetch_member(self.client.user.id)).send_messages
        if not sendPerms:
            return await ctx.author.send("`I cannot send messages in that text channel`")
        
        c = ctx.channel.id
        
        if c not in WaluigiBotDev.dailyChannelList:
            with open("data/WahNCounter.json", "r") as INFile:
                WahDict = load(INFile)
            WahDict["chanList"] += [c]
            WaluigiBotDev.dailyChannelList = WahDict["chanList"]
            with open("data/WahNCounter.json", "w") as OUTFile:
                dump(WahDict, OUTFile, indent="  ")
            return await ctx.send("`This Channel Will Now Receive Routine Messages`")

        await ctx.send("`This Channel Already Receives Routine Messages\nDo you want me to stop sending Messages? (yes/no)`")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            response = await self.client.wait_for('message', check=check, timeout=60)
        except:
            return await ctx.send("`TimeoutError: No changes have been made.`")
        if response.content.lower() == "yes":
            with open("data/WahNCounter.json", "r") as INFile:
                WahDict = load(INFile)
            WahDict["chanList"].remove(c)
            WaluigiBotDev.dailyChannelList = WahDict["chanList"]
            with open("data/WahNCounter.json", "w") as OUTFile:
                dump(WahDict, OUTFile, indent="  ")
            return await ctx.send("`This Channel Will No Longer Receive Routine Messages`")
        return await ctx.send("`No changes have been made.`")

    @commands.command()
    async def avatar(self, ctx, arg : str = None):
        p = ctx.message.mentions[0]
        if arg == "-d":
            return await ctx.send(p.default_avatar_url)
        return await ctx.send(p.avatar_url_as(static_format='png'))

    @commands.command(aliases=["colour"])
    async def color(self, ctx):
        p = ctx.message.mentions[0]
        return await ctx.send(f"{p.color}\nhttps://www.colorhexa.com/{str(p.color)[1:]}.png")

    @commands.command(aliases=["emoji"])
    async def e(self, ctx, emoji):
        emoji = f"\{emoji}"
        e = self.client.get_emoji(int(emoji[-19:-1]))
        return await ctx.send(e.url_as(static_format='png'))

    @commands.command(aliases=["rr", "rreact", "reaction"])
    async def randomReact(self, ctx, emoji : str = None):
        try:
            textChannel = ctx.channel
            await ctx.message.delete()
            messages = await textChannel.history(limit=5).flatten()
            if emoji == None:                   
                await random.choice(messages).add_reaction(random.choice(["🤓", "🤡", "👽", "🤔", "🤥", "😳"]))
            else:
                await random.choice(messages).add_reaction(emoji)
            return
        except Exception as e:
            await ctx.author.send(e)
            return await ctx.author.send("`I have failed to react - ><_><`")

    @commands.command()
    async def status(self, ctx):
        user = ctx.message.mentions[0]

        status_embed = discord.Embed()
        status_embed.title = f"{user.name} current status"
        status_embed.color = 0x7027C3
        status_embed.set_thumbnail(url=user.avatar_url)
        status_embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")

        status_embed.description = f"Role: {user.roles[len(user.roles)-1]}\n\nStatus: {user.status}\n\nActivity: {user.activity}"
        return await ctx.send(embed=status_embed)

    @commands.command()
    async def stats(self, ctx):
        if len(ctx.message.mentions) == 0:
            await ctx.send("`You must @mention someone`")
            return await ctx.send("Example: `wah stats @Waluigi Bot`")

        user = ctx.message.mentions[0]

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

    @commands.command()
    async def id(self, ctx):
        await ctx.send(self.client.user.id)

def setup(client):
    client.add_cog(basic(client))