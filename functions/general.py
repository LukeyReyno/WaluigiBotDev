import discord.ext.commands.context as C

async def getResponse(discordClient, ctx: C.Context): #method for getting guesses and deleting author message
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        guess = await discordClient.wait_for('message', check=check, timeout=60)
    except:
        return await ctx.send("`TimeoutError`")

    return guess