import discord
from discord.ext import commands

class BotUtil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def reload(self, ctx, cog):
        if self.bot.mod_role in ctx.author.roles:
            try:
                self.bot.reload_extension(cog)
                await self.bot.log_channel.send(f"`{cog}` reloaded successfully")
            except Exception as e:
                await self.bot.log_channel.send(f"Failed to reload addon: {cog} due to `{type(e).__name__}: {e}`")

    @commands.command(hidden=True)
    async def load(self, ctx, cog):
        if self.bot.mod_role in ctx.author.roles:
            try:
                self.bot.load_extension(cog)
                await self.bot.log_channel.send(f"`{cog}` loaded successfully")
            except Exception as e:
                await self.bot.log_channel.send(f"Failed to load addon: {cog} due to `{type(e).__name__}: {e}`")

    @commands.command(hidden=True)
    async def unload(self, ctx, cog):
        if self.bot.mod_role in ctx.author.roles:
            try:
                self.bot.unload_extension(cog)
                await self.bot.log_channel.send(f"`{cog}` unloaded successfully")
            except Exception as e:
                await self.bot.log_channel.send(f"Failed to unload addon: {cog} due to `{type(e).__name__}: {e}`")

def setup(bot):
    bot.add_cog(BotUtil(bot))