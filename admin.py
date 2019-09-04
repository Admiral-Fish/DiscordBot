import discord
from discord.ext import commands
import extensions
from util import getEmbed

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_user=True)
    async def kick(self, ctx, user: discord.Member, *reason):
        await user.kick(reason=reason)        
        await self.bot.log_channel.send(f"{ctx.author.mention} kicked {user.mention} for reason: {reason}")

    @commands.command()
    @commands.has_permissions(ban_user=True)
    async def ban(self, ctx, user: discord.Member, *reason):
        await user.ban(reason=reason)        
        await self.bot.log_channel.send(f"{ctx.author.mention} banned {user.mention} for reason: {reason}")

    @commands.command()
    async def member(self, ctx):
        if ctx.channel != self.bot.member_channel:
            return

        await ctx.message.delete()
        await ctx.author.add_roles(self.bot.member_role)     
        await self.bot.log_channel.send(f"Added member tole to {ctx.author.mention} | {ctx.author} | {ctx.author.id}")

    @commands.command()
    async def reload(self, ctx):
        for cog in extensions.cogs:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except Exception as e:
                await self.bot.log_channel.send(f"Failed to load addon: {cog} due to `{type(e).__name__}: {e}`")
                print(f"Failed to load addon: {cog} due to `{type(e).__name__}: {e}`")

def setup(bot):
    bot.add_cog(Admin(bot))