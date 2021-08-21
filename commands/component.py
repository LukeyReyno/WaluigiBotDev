import discord
import WaluigiBot

from discord.ext import commands
from discord.ext.commands import bot, context
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import *
from discord_slash.model import ButtonStyle, ComponentType

class component(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.__createExitActionRow()

    def __createExitActionRow(self):
        exitButton = [create_button(
                style=ButtonStyle.red, 
                label="Exit", 
                custom_id="exit")]
    
        self.exitActionRow = create_actionrow(*exitButton)

    @commands.command()
    async def button(self, ctx):
        buttons = [
            create_button(style=ButtonStyle.green, label="A green button", custom_id="Green"),
            create_button(style=ButtonStyle.blue, label="A blue button", custom_id="Blue")
        ]
    
        action_row = create_actionrow(*buttons)

        await ctx.send("`Waluigi Time`", components=[action_row, self.exitActionRow])

    @commands.command()
    async def button2(self, ctx):
        buttons = [
            create_button(style=ButtonStyle.red, label="🤡", custom_id="Clown"),
            create_button(style=ButtonStyle.gray, label="🐬", custom_id="Dolphin")
        ]
        buttons2 = [
            create_button(style=ButtonStyle.green, label="A green button", custom_id="Green"),
            create_button(style=ButtonStyle.blue, label="A blue button", custom_id="Blue")
        ]
    
        action_row = create_actionrow(*buttons)
        action_row2 = create_actionrow(*buttons2)

        await ctx.send("`Waluigi Time`", components=[action_row, action_row2, self.exitActionRow])

    @commands.command()
    async def select(self, ctx):
        select = create_select(
            options=[# the options in your dropdown
                create_select_option("Lab Coat", value="coat", emoji="🥼"),
                create_select_option("Test Tube", value="tube", emoji="🧪"),
                create_select_option("Petri Dish", value="dish", emoji="🧫"),
            ],
            placeholder="Choose your option",  # the placeholder text to show when no options have been chosen
            min_values=1,  # the minimum number of options a user must select
            max_values=2,  # the maximum number of options a user can select
        )

        await ctx.send("test", components=[create_actionrow(select)])  # like action row with buttons but without * in front of the variable

@WaluigiBot.bot.event
async def on_component(ctx: ComponentContext):
    # you may want to filter or change behaviour based on custom_id or message
    # print(ctx.custom_id)
    # print(ctx.data)

    if ctx.component_type == ComponentType.button:
        await ctx.defer(edit_origin=True)
        #await ctx.defer(edit_origin=False)
        if ctx.custom_id == "exit":
            await ctx.edit_origin(content="`Bye`")
        else:
            await ctx.edit_origin(content=f"`You pressed a {ctx.custom_id} button!`")

    """
    elif ctx.component_type == ComponentType.select:
        # ctx.selected_options is a list of all the values the user selected
        await ctx.edit_origin(content=f"You selected {ctx.selected_options}")"""

def setup(client):
    client.add_cog(component(client))
