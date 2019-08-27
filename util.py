import discord

import env

async def modLog(client, message):
    channel = client.get_channel(env.LOGCHAN_ID)
    await channel.send(message)

async def sendMessage(channel, title, message):
    embed = discord.Embed(title=title, description=message, color=0x3498db)
    await channel.send(embed=embed)