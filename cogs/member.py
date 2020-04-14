import discord
from discord.ext import commands

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def member(self, ctx):
        if ctx.channel != self.bot.member_channel:
            return

        await ctx.message.delete()
        await ctx.author.add_roles(self.bot.member_role)

        fields = { "Mention":ctx.author.mention, "Name":ctx.author, "ID":ctx.author.id }
        await self.bot.logAction("New Member", fields)

def setup(bot):
    bot.add_cog(Member(bot))