import discord
from discord.ext import commands

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def member(self, ctx):
        if ctx.channel != self.bot.member_channel:
            return

        await ctx.message.delete()
        await ctx.author.add_roles(self.bot.member_role)
        await self.bot.log_channel.send(f"Added member role to {ctx.author.mention} | {ctx.author} | {ctx.author.id}")

def setup(bot):
    bot.add_cog(Member(bot))