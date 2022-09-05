import discord
from bot import FishBot
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot: FishBot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason: str):
        await user.kick(reason=reason)

        fields = {"Author": ctx.author.mention, "User": user.mention, "Reason": reason}
        await self.bot.logAction("Kicked User", fields)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason: str):
        await user.ban(reason=reason)

        fields = {"Author": ctx.author.mention, "User": user.mention, "Reason": reason}
        await self.bot.logAction("Banned User", fields)

    @commands.command()
    @commands.has_role(285270611583041537)
    async def purge(self, ctx: commands.Context, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

        fields = {"Author": ctx.author.mention, "Channel": ctx.channel.mention, "Amount": str(amount)}
        await self.bot.logAction("Purged Messages", fields)


async def setup(bot: FishBot):
    await bot.add_cog(Admin(bot))
