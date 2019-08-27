import discord
import sys
import subprocess

from actions import fetchPCalc, installPCalc, grab3dsRNGTool, grabRNGReporter, grabPokeFinder, fixNTR, kickUser, banUser
from filter import filterMessage
from util import modLog

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_disconnect(self):
        print(f"{self.user} has disconnected")

    async def on_member_join(self, member):
        await modLog(self, f"Member joined {member}")

    async def on_member_remove(self, member):
        await modLog(self, f"Member left {member}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if filterMessage(message):
            await message.delete()
            await modLog(self, f"{message.author.mention} was censored in {message.channel.mention} for saying message.content")
            return

        await self.handleMessage(message)

    async def handleMessage(self, message):
        contents = message.content.split(" ", 2)

        command = contents[0]
        if command == ".ping":
            await message.channel.send("pong")
        elif command == ".pcalc":
            await fetchPCalc(message)
        elif command == ".grabbuild":
            await fetchPCalc(message)
        elif command == ".installpcalc":
            await installPCalc(message.channel)
        elif command == ".3dsrngtool":
            await grab3dsRNGTool(message.channel)
        elif command == ".rngreporter":
            await grabRNGReporter(message.channel)
        elif command == ".pokefinder":
            await grabPokeFinder(message.channel)
        elif command == ".fixntr":
            await fixNTR(message.channel)
        elif command == ".kick":
            if len(contents) == 3 and len(message.mentions) == 1:
                if await kickUser(message.author, message.mentions[0], contents[2]):
                    await modLog(self, f"{message.author.mention} kicked {message.mentions[0].mention} for reason: {contents[2]}")
                else:
                    await modLog(self, f"{message.author.mention} attempted to kick {message.mentions[0].mention} without privleges")
            return
        elif command == ".ban":
            if len(contents) == 3 and len(message.mentions) == 1:
                if await banUser(message.author, message.mentions[0], contents[2]):
                    await modLog(self, f"{message.author.mention} banned {message.mentions[0].mention} for reason: {contents[2]}")
                else:
                    await modLog(self, f"{message.author.mention} attempted to ban {message.mentions[0].mention} without privleges")
            return
        else:
            return

        await modLog(self, f"{message.author.mention} ran command {command} in {message.channel.mention}")