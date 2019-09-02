import discord

from env import getVariable

def filterMessage(message):
    channels = getVariable("FILTER_IGNORE_CHANNELS")
    if message.channel.id in [ int(channel) for channel in channels.split(",") ]:
        return False

    content = message.content.split()
    if any(x in content for x in getVariable("FILTER_WORDS").split(",")):
        return True

    return False