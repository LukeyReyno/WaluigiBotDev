import discord

from discord.ext import commands

TEST_CHANNEL=880634647527161867 #temp discord channel

class basic_tests():

    def __init__(self, client: commands.Bot):
        self.client = client
        self.testChannel: discord.TextChannel = self.client.get_channel(TEST_CHANNEL)

    async def testCTXSend(self):
        await self.testChannel.send("`This is an example message.`")

    async def runTests(self):
        await self.testCTXSend()
