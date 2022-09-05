from bot import FishBot
from discord.ext import commands


class Member(commands.Cog):
    def __init__(self, bot: FishBot):
        self.bot = bot

    @commands.command()
    async def member(self, ctx: commands.Context):
        if ctx.channel != self.bot.member_channel:
            return

        await ctx.message.delete()
        await ctx.author.add_roles(self.bot.member_role)

        fields = {"Mention": ctx.author.mention, "Name": ctx.author, "ID": ctx.author.id}
        await self.bot.logAction("New Member", fields)


async def setup(bot: FishBot):
    await bot.add_cog(Member(bot))
