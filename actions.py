import discord

import env
from util import sendMessage

async def fetchPCalc(message):
    await message.channel.send("pcalc")

async def installPCalc(channel):
    await sendMessage(channel, "Guide to Installing PCalc", "https://pokemonrng.com/guides/tools/en/How%20to%20Install%20PCalc.md")

async def grab3dsRNGTool(channel):
    await sendMessage(channel, "3DSRNGTool Releases", "https://github.com/wwwwwwzx/3DSRNGTool/releases")

async def grabRNGReporter(channel):
    await sendMessage(channel, "RNG Reporter Releases", "https://github.com/Admiral-Fish/RNGReporter/releases")

async def grabPokeFinder(channel):
    await sendMessage(channel, "PokeFinder Releases", "https://github.com/Admiral-Fish/PokeFinder/releases")

async def fixNTR(channel):
    message = "\n".join([
       "Delete the following files from the SD card to do a clean install:",
       "\t /ntr.o3ds/bin",
       "\t /ntr.n3ds.bin",
       "\t /3ds/bootntr",
       "\t /3ds/ntr",
       "\t /Nintendo 3DS/EBNTR",
       "\n Reinstall [BootNTR Selector](https://github.com/Nanquitas/BootNTR/releases)." 
    ])

    await sendMessage(channel, "Fixing NTR", message)

async def kickUser(author, user, reason):
    if not any(role.id == env.MODROLE_ID for role in author.roles):
        return False

    if any(role.id == env.MODROLE_ID for role in user.roles):
        return False

    await user.kick(reason=reason)
    
    return True
    
async def banUser(author, user, reason):
    if not any(role.id == env.MODROLE_ID for role in author.roles):
        return False

    if any(role.id == env.MODROLE_ID for role in user.roles):
        return False

    await user.ban(reason=reason)
    
    return True