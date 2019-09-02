import aiohttp
import discord
import io
import sys
import subprocess

from env import EnvType, getVariable
from filter import filterMessage

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_disconnect(self):
        print(f"{self.user} has disconnected")

    async def on_member_join(self, member):
        await self.logMessage(f"Member joined {member}")

    async def on_member_remove(self, member):
        await self.logMessage(f"Member left {member}")

    async def logMessage(self, message):        
        channel = self.get_channel(getVariable("LOGCHAN_ID", EnvType.INT))
        await channel.send(message)

    async def sendMessage(self, channel, title, message):
        embed = discord.Embed(title=title, description=message, color=0x3498db)
        await channel.send(embed=embed)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if filterMessage(message):
            await message.delete()
            await self.logMessage(f"{message.author.mention} was censored in {message.channel.mention} for saying {message.content}")
            return

        await self.handleMessage(message)

    async def handleMessage(self, message):
        contents = message.content.split(" ", 2)

        command = contents[0]
        if command == ".pcalc":
            if len(contents) == 2:
                await self.fetchPCalc(message.channel, contents[1])
        elif command == ".installpcalc":
            await self.installPCalc(message.channel)
        elif command == ".3dsrngtool":
            await self.grab3dsRNGTool(message.channel)
        elif command == ".rngreporter":
            await self.grabRNGReporter(message.channel)
        elif command == ".pokefinder":
            await self.grabPokeFinder(message.channel)
        elif command == ".fixntr":
            await self.fixNTR(message.channel)
        elif command == ".kick":
            if len(contents) == 3 and len(message.mentions) == 1:
                await self.kickUser(message.author, message.mentions[0], contents[2])
            return
        elif command == ".ban":
            if len(contents) == 3 and len(message.mentions) == 1:
                await self.banUser(message.author, message.mentions[0], contents[2])
            return
        elif command == ".member":
            await self.addMember(message, message.guild.get_role(getVariable("MEMBERROLE_ID", EnvType.INT)))
        else:
            return

        await self.logMessage(f"{message.author.mention} ran command {command} in {message.channel.mention}")

    async def fetchPCalc(self, channel, version):
        if channel.id not in getVariable("BUILDCHAN_IDs", EnvType.INT_LIST):
            await self.sendMessage(channel, "Uh oh!", "Please do not ask for PCalc in this channel.")
            return

        if version not in getVariable("BUILDS", EnvType.STRING_LIST):
            await self.sendMessage(channel, "Uh oh!", "Build not found! Please try: usum, sm, oras, xy, tport")
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pokemonrng.com/downloads/pcalc/pcalc-{version}.zip") as resp:
                if resp.status != 200:
                    return await channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await channel.send(content=f"Here's the latest PCalc-usum", file=discord.File(data, f"pcalc-{version}.zip"))

    async def installPCalc(self, channel):
        await self.sendMessage(channel, "Guide to Installing PCalc", "https://pokemonrng.com/guides/tools/en/How%20to%20Install%20PCalc.md")

    async def grab3dsRNGTool(self, channel):
        await self.sendMessage(channel, "3DSRNGTool Releases", "https://github.com/wwwwwwzx/3DSRNGTool/releases")

    async def grabRNGReporter(self, channel):
        await self.sendMessage(channel, "RNG Reporter Releases", "https://github.com/Admiral-Fish/RNGReporter/releases")

    async def grabPokeFinder(self, channel):
        await self.sendMessage(channel, "PokeFinder Releases", "https://github.com/Admiral-Fish/PokeFinder/releases")

    async def fixNTR(self, channel):
        message = "\n".join([
        "Delete the following files from the SD card to do a clean install:",
        "\t /ntr.o3ds/bin",
        "\t /ntr.n3ds.bin",
        "\t /3ds/bootntr",
        "\t /3ds/ntr",
        "\t /Nintendo 3DS/EBNTR",
        "\n Reinstall [BootNTR Selector](https://github.com/Nanquitas/BootNTR/releases)." 
        ])

        await self.sendMessage(channel, "Fixing NTR", message)

    async def kickUser(self, author, user, reason):
        modrole = getVariable("MODROLE_ID", EnvType.INT)
        if not any(role.id == modrole for role in author.roles) or any(role.id == modrole for role in user.roles):
            await self.logMessage(f"{author.mention} attempted to kick {user.mention} without privleges")
            return

        await user.kick(reason=reason)        
        await self.logMessage(f"{author.mention} kicked {user.mention} for reason: {reason}")
        
    async def banUser(self, author, user, reason):
        modrole = getVariable("MODROLE_ID", EnvType.INT)
        if not any(role.id == modrole for role in author.roles) or any(role.id == modrole for role in user.roles):
            await self.logMessage(f"{author.mention} attempted to ban {user.mention} without privleges")
            return

        await user.ban(reason=reason)        
        await self.logMessage(f"{author.mention} banned {user.mention} for reason: {reason}")

    async def addMember(self, message, role):
        if message.channel.id != getVariable("MEMBERCHAN_ID", EnvType.INT):
            return

        if role in message.author.roles:
            return

        await message.author.add_roles(role)        
        await self.logMessage(f"Added member tole to {message.author.mention} | {message.author} | {message.author.id}")