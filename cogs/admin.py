import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason):
        await user.kick(reason=reason)

        fields = { "Author":ctx.author.mention, "User":user.mention, "Reason":reason }
        await self.bot.logAction("Kicked User", fields)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, reason):
        await user.ban(reason=reason)

        fields = { "Author":ctx.author.mention, "User":user.mention, "Reason":reason }
        await self.bot.logAction("Banned User", fields)

    @commands.command()
    @commands.has_role(285270611583041537)
    async def purge(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

        fields = { "Author":ctx.author.mention, "Channel":ctx.channel.mention, "Amount":str(amount) }
        await self.bot.logAction("Purged Messages", fields)


def setup(bot):
    bot.add_cog(Admin(bot))