import aiohttp
import discord
from discord.ext import commands
import io

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def grabtool(self, ctx, tool):
        if tool == "3dsrngtool":
            title = "3DSRNGTool Releases"
            message = "https://github.com/wwwwwwzx/3DSRNGTool/releases"
        elif tool == "pokefinder":
            title = "PokeFinder Releases"
            message = "https://github.com/Admiral-Fish/PokeFinder/releases"
        elif tool == "rngreporter":
            title = "RNG Reporter Releases"
            message = "https://github.com/Admiral-Fish/RNGReporter/releases"
        else:
            await ctx.send("Invalid tool. Valid tools are `3dsrngtool`, `pokefinder`, `rngeporter`")
            return

        embed = discord.Embed(title=title, description=message, color=0x3498db)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Command used", color=0x3498db)
        embed.add_field(name="Command", value=".grabtool")
        embed.add_field(name="Argument", value=tool)
        embed.add_field(name="User", value=ctx.author.mention)
        embed.add_field(name="Channel", value=ctx.channel.mention)
        await self.bot.log_channel.send(embed=embed)

    @commands.command()
    async def installpcalc(self, ctx):
        embed = discord.Embed(title="Guide to Installing PCalc", description="https://pokemonrng.com/guides/tools/en/How%20to%20Install%20PCalc/", color=0x3498db)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Command used", color=0x3498db)
        embed.add_field(name="Command", value=".installpcalc")
        embed.add_field(name="User", value=ctx.author.mention)
        embed.add_field(name="Channel", value=ctx.channel.mention)
        await self.bot.log_channel.send(embed=embed)
        
    @commands.command()
    async def lua(self, ctx, gen: int):
        if gen == 3:
            message = "Gen 3: https://pokerng.forumcommunity.net/?t=56443955&p=396434940"
        elif gen == 4:
            message = "Gen 4: https://pokerng.forumcommunity.net/?t=56443955&p=396434991"
        elif gen == 5:
            message = "Gen 5: https://pokerng.forumcommunity.net/?t=56443955&p=396435011"
        else:
            await ctx.send("Invalid gen. Valid gens are `3`, `4`, or `5`.")

        message += "\n\nPassword is `allyouneedisnoob`"
        
        embed = discord.Embed(title=f"Gen {gen} Lua Scripts", description=message, color=0x3498db)
        await ctx.send(embed=embed)
        
        embed = discord.Embed(title="Command used", color=0x3498db)
        embed.add_field(name="Command", value=".lua")
        embed.add_field(name="Argument", value=str(gen))
        embed.add_field(name="User", value=ctx.author.mention)
        embed.add_field(name="Channel", value=ctx.channel.mention)
        await self.bot.log_channel.send(embed=embed)

    @commands.command()
    async def pcalc(self, ctx, build):
        if ctx.channel.id not in self.bot.build_channels:
            embed = discord.Embed(title="Uh oh!", description="Please do not ask for PCalc in this channel.", color=0x3498db)
            await ctx.send(embed=embed)
            return

        if build not in self.bot.build_list:
            embed = discord.Embed(title="Uh oh!", description="Build not found! Please try: `usum`, `sm`, `oras`, `xy`, `tport`", color=0x3498db)
            await ctx.send(embed=embed)
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pokemonrng.com/downloads/pcalc/pcalc-{build}.zip") as resp:
                if resp.status != 200:
                    return await ctx.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await ctx.send(content=f"Here's the latest PCalc-{build}", file=discord.File(data, f"pcalc-{build}.zip"))
                           
                embed = discord.Embed(title="Command used", color=0x3498db)
                embed.add_field(name="Command", value=".pcalc")
                embed.add_field(name="Argument", value=build)
                embed.add_field(name="User", value=ctx.author.mention)
                embed.add_field(name="Channel", value=ctx.channel.mention)
                await self.bot.log_channel.send(embed=embed)

    @commands.command()
    async def fixntr(self, ctx):
        message = "\n".join([
        "Delete the following files from the SD card to do a clean install:",
        "\t /ntr.o3ds/bin",
        "\t /ntr.n3ds.bin",
        "\t /3ds/bootntr",
        "\t /3ds/ntr",
        "\t /Nintendo 3DS/EBNTR",
        "\n Reinstall [BootNTR Selector](https://github.com/Nanquitas/BootNTR/releases)." 
        ])

        embed = discord.Embed(title="Fixing NTR", description=message, color=0x3498db)
        await ctx.send(embed=embed)
        
        embed = discord.Embed(title="Command used", color=0x3498db)
        embed.add_field(name="Command", value=".fixntr")
        embed.add_field(name="User", value=ctx.author.mention)
        embed.add_field(name="Channel", value=ctx.channel.mention)
        await self.bot.log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Tools(bot))