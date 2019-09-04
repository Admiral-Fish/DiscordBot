import discord
from discord.ext import commands
from dotenv import load_dotenv
from env import EnvType, getVariable
import extensions

class FishBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".")
        load_dotenv()      

    async def on_ready(self):
        # Bot should only be in one server anyways
        guild = self.guilds[0]
        self.mod_role = guild.get_role(getVariable("MODROLE_ID", EnvType.INT))
        self.log_channel = guild.get_channel(getVariable("LOGCHAN_ID", EnvType.INT))
        self.member_channel = guild.get_channel(getVariable("MEMBERCHAN_ID", EnvType.INT))
        self.member_role = guild.get_role(getVariable("MEMBERROLE_ID", EnvType.INT))
        self.build_list = getVariable("BUILDS", EnvType.STRING_LIST)
        self.build_channels = getVariable("BUILDCHAN_IDs", EnvType.INT_LIST)
        self.filter_words = getVariable("FILTER_WORDS", EnvType.STRING_LIST)
        self.filter_ignore_channels = getVariable("FILTER_IGNORE_CHANNELS", EnvType.INT_LIST)

        for cog in extensions.cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                await self.log_channel.send(f"Failed to load addon: {cog} due to `{type(e).__name__}: {e}`\n")
                print(f"Failed to load addon: {cog} due to `{type(e).__name__}: {e}`\n")

        await self.log_channel.send("Bot finished loading")

    async def on_member_join(self, member):
        await self.log_channel.send(f"Member joined {member}")

    async def on_member_remove(self, member):
        await self.log_channel.send(f"Member left {member}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if any(message.channel.id == channel for channel in self.filter_ignore_channels):
            return

        words = message.content.split(" ")
        if any(word in self.filter_words for word in words):
            await message.delete()
            await self.log_channel.send(f"{message.author.mention} was censored in {message.channel.mention} for saying {message.content}")
            return

        if message.channel == self.member_channel and message != ".member":
            await message.delete()

        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            pass
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You are missing required arguments.")
            await ctx.send_help(ctx.command)
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send("A bad argument was provided, please try again.")
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions) or isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send("You don't have permission to use this command.")

    def run(self):
        super().run(getVariable("DISCORD_TOKEN"), reconnect=True)