import discord
from discord.ext import commands
from env import EnvType, getVariable
import extensions


class FishBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix=".", intents=intents)

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
                await self.load_extension(cog)
            except Exception as e:
                await self.log_channel.send(f"Failed to load addon: {cog} due to `{type(e).__name__}: {e}`")

        await self.log_channel.send("Bot finished loading")

    async def on_member_join(self, member: discord.Member):
        fields = {"User": member}
        await self.logAction("Member Joined", fields)

    async def on_member_remove(self, member: discord.Member):
        fields = {"User": member}
        await self.logAction("Member Left", fields)

    async def on_message(self, message: discord.Message):
        # Ignore bot messages
        if message.author == self.user:
            return

        # Check if message is in DM
        if message.guild is None:
            fields = {"Author": message.author.mention, "Message": message.content}
            await self.logAction("Bot DM", fields)
            return

        # Remove random messages from welcome channel
        if message.channel == self.member_channel and message.content != ".member":
            await message.delete()
            return

        # Only attempt to filter if in channels that need to be filtered
        if not any(message.channel.id == channel for channel in self.filter_ignore_channels):
            content = message.content.lower()

            if any(filter_word in content for filter_word in self.filter_words):
                await message.channel.send(f"{message.author.mention}, your message has been filtered. Please review the rules before posting again")
                await message.delete()
                return

        # Got em
        if message.content == "got em":
            await message.channel.send("bois")
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def on_command_error(self, ctx: commands.Context, error: commands.errors.CommandError):
        if isinstance(error, commands.errors.CommandNotFound):
            pass
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You are missing required arguments.")
            await ctx.send_help(ctx.command)
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send("A bad argument was provided, please try again.")
        elif isinstance(error, commands.errors.MissingPermissions) or isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You don't have permission to use this command.")

    async def on_message_delete(self, message: discord.Message):
        fields = {"Author": message.author.mention, "Channel": message.channel.mention, "Message": message.content}
        await self.logAction("Deleted Message", fields)

    async def logAction(self, title: str, fields: dict[str, str]):
        embed = discord.Embed(title=title, color=0x3498db)
        for name, value in fields.items():
            embed.add_field(name=name, value=value)
        await self.log_channel.send(embed=embed)

    def run(self):
        super().run(getVariable("DISCORD_TOKEN"), reconnect=True)
