import discord
from discord.ext import commands
import extensions

class BotUtil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(285270611583041537)
    async def reload(self, ctx, cog):
        if cog == "all":
            for cog in extensions.cogs:
                try:
                    self.bot.reload_extension(cog)
                    await ctx.send(f"`{cog}` loaded successfully", delete_after=5)
                except Exception as e:
                    await ctx.send(f"Failed to load addon: {cog} due to `{type(e).__name__}: {e}`", delete_after=5)
        else:
            try:
                self.bot.reload_extension(f"cogs.{cog}")
                await ctx.send(f"`cogs.{cog}` loaded successfully", delete_after=5)
            except Exception as e:
                await ctx.send(f"Failed to load addon: cogs.{cog} due to `{type(e).__name__}: {e}`", delete_after=5)

        fields = { "Command":".reload", "Argument":cog, "User":ctx.author.mention, "Channel":ctx.channel.mention }
        await self.bot.logAction("Command Used", fields)
        await ctx.message.delete(delay=5)


    @commands.command()
    @commands.has_role(285270611583041537)
    async def load(self, ctx, cog):
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await self.bot.log_channel.send(f"`cogs.{cog}` loaded successfully", delete_after=5)
        except Exception as e:
            await self.bot.log_channel.send(f"Failed to load addon: `cogs.{cog}` due to `{type(e).__name__}: {e}`", delete_after=5)

        fields = { "Command":".load", "Argument":cog, "User":ctx.author.mention, "Channel":ctx.channel.mention }
        await self.bot.logAction("Command Used", fields)
        await ctx.message.delete(delay=5)

    @commands.command()
    @commands.has_role(285270611583041537)
    async def unload(self, ctx, cog):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await self.bot.log_channel.send(f"`cogs.{cog}` unloaded successfully", delete_after=5)
        except Exception as e:
            await self.bot.log_channel.send(f"Failed to unload addon: `cogs.{cog}` due to `{type(e).__name__}: {e}`", delete_after=5)

        fields = { "Command":".unload", "Argument":cog, "User":ctx.author.mention, "Channel":ctx.channel.mention }
        await self.bot.logAction("Command Used", fields)
        await ctx.message.delete(delay=5)

    @commands.command()
    @commands.has_role(285270611583041537)
    async def ping(self, ctx):
        await ctx.send("pong")

def setup(bot):
    bot.add_cog(BotUtil(bot))
