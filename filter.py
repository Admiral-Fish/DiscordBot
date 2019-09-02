import discord
from env import EnvType, getVariable

def filterMessage(message):
    if message.channel.id in getVariable("FILTER_IGNORE_CHANNELS", EnvType.INT_LIST):
        return False

    content = message.content.split()
    if any(x in content for x in getVariable("FILTER_WORDS", EnvType.STRING_LIST)):
        return True

    return False