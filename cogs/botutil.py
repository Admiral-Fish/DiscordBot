import discord
from discord.ext import commands

class BotUtil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.has_role("Mods")
    async def reload(self, ctx, cog):
        try:
            self.bot.reload_extension(cog)
            await self.bot.log_channel.send(f"`{cog}` reloaded successfully", delete_after=5)
        except Exception as e:
            await self.bot.log_channel.send(f"Failed to reload addon: {cog} due to `{type(e).__name__}: {e}`", delete_after=5)

        fields = { "Command":".reload", "Argument":cog, "User":ctx.author.mention, "Channel":ctx.channel.mention }
        await self.bot.logAction("Command Used", fields)


    @commands.command(hidden=True)
    @commands.has_role("Mods")
    async def load(self, ctx, cog):
        try:
            self.bot.load_extension(cog)
            await self.bot.log_channel.send(f"`{cog}` loaded successfully", delete_after=5)
        except Exception as e:
            await self.bot.log_channel.send(f"Failed to load addon: {cog} due to `{type(e).__name__}: {e}`", delete_after=5)

        fields = { "Command":".load", "Argument":cog, "User":ctx.author.mention, "Channel":ctx.channel.mention }
        await self.bot.logAction("Command Used", fields)

    @commands.command(hidden=True)
    @commands.has_role("Mods")
    async def unload(self, ctx, cog):
        try:
            self.bot.unload_extension(cog)
            await self.bot.log_channel.send(f"`{cog}` unloaded successfully", delete_after=5)
        except Exception as e:
            await self.bot.log_channel.send(f"Failed to unload addon: {cog} due to `{type(e).__name__}: {e}`", delete_after=5)

        fields = { "Command":".unload", "Argument":cog, "User":ctx.author.mention, "Channel":ctx.channel.mention }
        await self.bot.logAction("Command Used", fields)

def setup(bot):
    bot.add_cog(BotUtil(bot))