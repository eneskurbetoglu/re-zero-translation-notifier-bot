import discord
import random
import os
import aiohttp
import json

from discord.ext import commands
from discord import app_commands


class WarframeMarket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.base_url = "https://api.warframe.market/v1"
        self.items_list = {}
        self.is_synced = False
        self.image_url = "https://warframe.market/static/assets"
        
    async def sync(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url+"/items") as r:
                if r.status == 200:
                    response = await r.read()
                    self.items_list = json.loads(response)['payload']['items']
                    self.is_synced = True
                else:
                    print("WarframeMarket down!")

    @commands.command()
    @commands.is_owner()
    async def sync_items(self, ctx):
        try:
            self.sync()
            await ctx.send("Items synced, I suppose!")
        except Exception as e:
            print(e)
            await ctx.send("Something went wrong, I suppose!")
    
    @app_commands.command(name="item")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Sell", value="sell"),
        app_commands.Choice(name="Buy", value="buy"),
        ])
    async def get_item(self, interaction: discord.Interaction, choices: app_commands.Choice[str], *, item_name: str):
        order_type = choices.value
        item_name = " ".join([p.capitalize() for p in item_name.split(' ')])
        if not self.is_synced:
            await self.sync()
        for item in self.items_list:
            if item['item_name'] == item_name:
                item_info = item
        url_name = item_info['url_name']
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url+"/items/"+url_name) as r:
                if r.status == 200:
                    response = await r.read()
                    item_detail = json.loads(response)['payload']['item']['items_in_set'][0]
                else:
                    print("WarframeMarket down!")
        trading_tax = item_detail['trading_tax']
        ducats = item_detail['ducats']
        mastery_level = item_detail['mastery_level']
        item_description = item_detail['en']['description']
        wikilink = item_detail['en']['wiki_link']
        drop_list = item_detail['en']['drop']
        desc = f"Requires mastery rank {mastery_level}\n"
        desc += f"Trading tax: {trading_tax}, Ducats value: {ducats}\n"
        desc += f"```{item_description}```\n"
        desc += f"Drops from "
        for i in range(len(drop_list)):
            desc += drop_list[i]['name']+', ' if i < len(drop_list)-1 else drop_list[i]['name']
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url+"/items/"+url_name+"/orders") as r:
                if r.status == 200:
                    response = await r.read()
                    orders = json.loads(response)['payload']['orders']
                    online_orders = [o for o in orders if o['user']['status'] != 'offline']
                    filtered_types = [o for o in online_orders if o['order_type'] == order_type]
                    orders_sorted = sorted(filtered_types, key = lambda ele: ele['platinum'])
                else:
                    print("WarframeMarket down!")
        for i in range(len(orders_sorted)):
            if i>4:
                break
            desc += f"\n\nPrice: {orders_sorted[i]['platinum']} plat, Quantity: {orders_sorted[i]['quantity']}, Order type: {orders_sorted[i]['order_type']}\n"
            desc += f"by {orders_sorted[i]['user']['ingame_name']}\n"
            desc += f"```/w {orders_sorted[i]['user']['ingame_name']} Hi! I want to {orders_sorted[i]['order_type']}: {item_name} for {orders_sorted[i]['platinum']} platinum. (warframe.market)```\n"
        embed = discord.Embed(
            color=discord.Colour.random(),
            title=item_info['item_name'],
            url=wikilink,
            description=desc,
        )
        embed.set_thumbnail(url=self.image_url+"/"+item_info['thumb'])
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(WarframeMarket(bot))