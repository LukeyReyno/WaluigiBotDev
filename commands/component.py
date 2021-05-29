import discord
import asyncio

from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import discord_components

class component(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dComp = DiscordComponents(client, change_discord_methods=False)

    @commands.command()
    async def component(self, ctx):
        await DiscordComponents.send_component_msg(
            self = self.dComp,
            channel=ctx.channel, 
            content="Waluigi Moment", 
            components=[
                Button(style=ButtonStyle.blue, label="Blue Button", emoji=discord.PartialEmoji(name="🤡")),
                Button(style=ButtonStyle.red, label="Red Button", emoji=discord.PartialEmoji(name="🤥")),
                Button(style=ButtonStyle.gray, label="Gray Button", emoji=discord.PartialEmoji(name="😂")),
                Button(style=ButtonStyle.green, label="Green Button", emoji=discord.PartialEmoji(name="🐬")),
                Button(style=ButtonStyle.blue, label="Quit", emoji=discord.PartialEmoji(name="🛑"))
            ],
        )

        res: discord_components.Context = await self.dComp.wait_for_interact("button_click")
        if res.channel == ctx.channel:
            await res.respond(
                type=InteractionType.ChannelMessageWithSource,
                content=f'{res.component.label} clicked'
            )

def setup(client):
    client.add_cog(component(client))