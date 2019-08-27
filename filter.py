import discord

import env

def filterMessage(message):
    if message.channel.id in env.FILTER_IGNORE_CHANNELS:
        return False

    content = message.content.split()
    if any(x in content for x in env.FILTER_WORDS):
        return True

    return False