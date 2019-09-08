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

        embed = discord.Embed(title="New Member", color=0x3498db)
        embed.add_field(name="Mention", value=ctx.author.mention)
        embed.add_field(name="Name", value=ctx.author)
        embed.add_field(name="ID", value=ctx.author.id)
        await self.bot.log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Member(bot))