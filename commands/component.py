import discord
import asyncio

from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

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
                Button(style=ButtonStyle.blue, label="🤡"),
                Button(style=ButtonStyle.red, label="🤥"),
                Button(style=ButtonStyle.URL, label="url", url="https://lukeyreyno.github.io/lucas-website/index.html"),
            ],
        )

        res = await self.dComp.wait_for_interact("button_click")
        if res.channel == ctx.channel:
            await res.respond(
                type=InteractionType.ChannelMessageWithSource,
                content=f'{res.component.label} clicked'
            )

def setup(client):
    client.add_cog(component(client))