import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_user=True)
    async def kick(self, ctx, user: discord.Member, *, reason):
        await user.kick(reason=reason)        
        await self.bot.log_channel.send(f"{ctx.author.mention} kicked {user.mention} for reason: {reason}")

    @commands.command()
    @commands.has_permissions(ban_user=True)
    async def ban(self, ctx, user: discord.Member, reason):
        await user.ban(reason=reason)        
        await self.bot.log_channel.send(f"{ctx.author.mention} banned {user.mention} for reason: {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

def setup(bot):
    bot.add_cog(Admin(bot))