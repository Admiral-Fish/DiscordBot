import discord

async def sendMessage(channel, title, message):
    embed = discord.Embed(title=title, description=message, color=0x3498db)
    await channel.send(embed=embed)