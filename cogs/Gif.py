import discord
import random
import os
import aiohttp
import json

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


class Gif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tenor_api_key = os.getenv('TENOR_API_KEY')

    # pout uwu
    @commands.command()
    async def pout(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://g.tenor.com/v1/search?q=%s&key=%s" %
                                   ("anime pout", self.tenor_api_key)) as r:
                if r.status == 200:
                    response = await r.read()
                    pouts = json.loads(response)
                else:
                    print("Tenor down!")
                    return
        embed = discord.Embed(
            color=discord.Colour.random()
        )
        rand_index = random.randrange(len(pouts['results']))
        desc = '{} pouted, I suppose!'.format(ctx.author.mention)
        embed = discord.Embed(description=desc, color=discord.Colour.random())
        embed.set_image(url=(pouts['results'])[rand_index]
                        ['media'][0]['mediumgif']['url'])
        await ctx.send(embed=embed)

    # hug uwu
    @commands.command()
    async def hug(self, ctx, user: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://g.tenor.com/v1/search?q=%s&key=%s" %
                                   ("anime hug", self.tenor_api_key)) as r:
                if r.status == 200:
                    response = await r.read()
                    hugs = json.loads(response)
                else:
                    print("Tenor down!")
                    return
        if not user:
            user = ctx.author
        embed = discord.Embed(
            color=discord.Colour.random()
        )
        rand_index = random.randrange(len(hugs['results']))
        if ctx.author.id == user.id:
            desc = 'Hugging yourself? Pathetic, I suppose!'
        elif user.id == self.bot.user.id:
            desc = 'How dare you hug me, in fact?! *swoosh* Be gone, I suppose!'
        else:
            desc = '{} hugged {}, I suppose!'.format(
                ctx.author.mention, user.mention)
        embed = discord.Embed(description=desc, color=discord.Colour.random())
        embed.set_image(url=(hugs['results'])[rand_index]
                        ['media'][0]['mediumgif']['url'])
        await ctx.send(embed=embed)

    # smug uwu
    @commands.command()
    async def smug(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://g.tenor.com/v1/search?q=%s&key=%s" %
                                   ("anime smug", self.tenor_api_key)) as r:
                if r.status == 200:
                    response = await r.read()
                    smugs = json.loads(response)
                else:
                    print("Tenor down!")
                    return
        embed = discord.Embed(
            color=discord.Colour.random()
        )
        rand_index = random.randrange(len(smugs['results']))
        desc = '{} is being smug, I suppose!'.format(ctx.author.mention)
        embed = discord.Embed(description=desc, color=discord.Colour.random())
        embed.set_image(url=(smugs['results'])[rand_index]
                        ['media'][0]['mediumgif']['url'])
        await ctx.send(embed=embed)

    # pat uwu
    @commands.command()
    async def pat(self, ctx, user: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://g.tenor.com/v1/search?q=%s&key=%s" %
                                   ("anime pat", self.tenor_api_key)) as r:
                if r.status == 200:
                    response = await r.read()
                    pats = json.loads(response)
                else:
                    print("Tenor down!")
                    return
        embed = discord.Embed(
            color=discord.Colour.random()
        )
        rand_index = random.randrange(len(pats['results']))
        if ctx.author.id == user.id:
            desc = 'Why are you patting yourself, I suppose!'
        elif user.id == self.bot.user.id:
            desc = 'Don\'t get any funny ideas, Betty\'s trying to be nice so she\'ll allow it, in fact!'
        else:
            desc = '{} patted {}, I suppose!'.format(
                ctx.author.mention, user.mention)
        embed = discord.Embed(description=desc, color=discord.Colour.random())
        embed.set_image(url=(pats['results'])[rand_index]
                        ['media'][0]['mediumgif']['url'])
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Gif(bot))
