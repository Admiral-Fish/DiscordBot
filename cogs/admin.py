import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.has_permissions(kick_user=True)
    async def kick(self, ctx, user: discord.Member, *, reason):
        await user.kick(reason=reason)

        embed = discord.Embed(title="Kicked user", color=0x3498db)
        embed.add_field(name="Author", value=ctx.author.mention)
        embed.add_field(name="User", value=user.mention)
        embed.add_field(name="Reason", value=reason)
        await self.bot.log_channel.send(embed=embed)

    @commands.command(hidden=True)
    @commands.has_permissions(ban_user=True)
    async def ban(self, ctx, user: discord.Member, reason):
        await user.ban(reason=reason)

        embed = discord.Embed(title="Banned user", color=0x3498db)
        embed.add_field(name="Author", value=ctx.author.mention)
        embed.add_field(name="User", value=user.mention)
        embed.add_field(name="Reason", value=reason)
        await self.bot.log_channel.send(embed=embed)

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        
        embed = discord.Embed(title="Purged messages", color=0x3498db)
        embed.add_field(name="Author", value=ctx.author.mention)
        embed.add_field(name="Channel", value=ctx.channel.mention)
        embed.add_field(name="Amount", value=str(amount))
        await self.bot.log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))