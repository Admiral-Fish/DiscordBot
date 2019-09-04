import discord

def getEmbed(title, message):
    embed = discord.Embed(title=title, description=message, color=0x3498db)
    return embed