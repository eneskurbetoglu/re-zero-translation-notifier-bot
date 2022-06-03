import discord      
import aiofiles

from wand.image import Image
from discord import ui
from aiohttp.client import ClientSession
from discord.ext.commands import Bot
from typing import List
from typing_extensions import Self


class FilterView(ui.View):
    def __init__(self, i: discord.Interaction, embed: discord.Embed, bot: Bot):
        super().__init__(timeout=60)
        self.i = i
        self.embed = embed
        self.image = embed.image.url
        self.bot = bot
        self.filters: List[str] = []
        self.new_embed = discord.Embed(colour=discord.Colour.random())
        self.add_once: bool = True
        
        
    def disabled(self):
        for btn in self.children:  # type: ignore
            btn.disabled = True  # type: ignore
        return self
    
    
    async def on_timeout(self):
        self.stop()
        msg = await self.i.original_message()
        if msg:
            if self.add_once:
                await self.i.edit_original_message(embed=self.embed, view=self.disabled())
            else:
                await self.i.edit_original_message(embed=self.new_embed, view=self.disabled())  # type: ignore
            await msg.reply("This view just timed out, I suppose! You need to interact with it to keep it up, in fact!")  # type: ignore
        
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.i.user  # type: ignore
    
    
    async def apply_filter(self, choice: int):
        with Image(filename="original_user_avatar.png") as img:
            if choice == 0:
                img.blur(radius=0, sigma=3)
            elif choice == 1:
                img.shade(gray=True,
                          azimuth=286.0,
                          elevation=45.0
                            )
            elif choice == 2:
                img.sharpen(radius=8, sigma=4)
            elif choice == 3:
                img.spread(radius=8.0)
            elif choice == 4:
                img.transform_colorspace('gray')
                img.edge(radius=1)
            elif choice == 5:
                img.transform_colorspace('gray')
                img.emboss(radius=3.0, sigma=1.75)
            elif choice == 6:
                img.charcoal(radius=1.5, sigma=0.5)
            elif choice == 7:
                img.wave(amplitude=img.height / 32,
                        wave_length=img.width / 4)
            elif choice == 8:
                img.colorize(color="yellow", alpha="rgb(10%, 0%, 20%)")
            elif choice == 9:
                img.sepia_tone(threshold=0.8)
            elif choice == 10:
                img.transform_colorspace("gray")
                img.sketch(0.5, 0.0, 98.0)
            elif choice == 11:
                img.solarize(threshold=0.5 * img.quantum_range)
            elif choice == 12:
                img.swirl(degree=-90)
            elif choice == 13:
                img.tint(color="yellow", alpha="rgb(40%, 60%, 80%)")
            else:
                f = discord.File("./original_user_avatar.png", filename="original_user_avatar.png")
        
                if self.add_once:
                    self.new_embed.add_field(name=self.embed.fields[0].name, value=self.embed.fields[0].value)
                    self.add_once = False
                self.new_embed.set_image(url="attachment://original_user_avatar.png")
                
                await self.i.edit_original_message(attachments=[f], embed=self.new_embed)
            
            img.save(filename="user_avatar.png")
        
        f = discord.File("./user_avatar.png", filename="user_avatar.png")
        
        if self.add_once:
            self.new_embed.add_field(name=self.embed.fields[0].name, value=self.embed.fields[0].value)
            self.add_once = False
        self.new_embed.set_image(url="attachment://user_avatar.png")
        
        await self.i.edit_original_message(attachments=[f], embed=self.new_embed)

    
    async def update(self, choice: int):
        session: ClientSession = self.bot.session  # type: ignore
        url: str = self.image  # type: ignore
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open('./original_user_avatar.png', mode='wb') as f:
                    await f.write(await resp.read())
        
        await self.apply_filter(choice)
        
            
        
    @ui.button(label='Blur', style=discord.ButtonStyle.blurple)
    async def opt_one(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(0)
        
    @ui.button(label='Shade', style=discord.ButtonStyle.blurple)
    async def opt_two(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(1)
        
    @ui.button(label='Sharpen', style=discord.ButtonStyle.blurple)
    async def opt_three(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(2)
        
    @ui.button(label='Spread', style=discord.ButtonStyle.blurple)
    async def opt_four(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(3)
        
    @ui.button(label='Edge', style=discord.ButtonStyle.blurple)
    async def opt_five(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(4)
                
    @ui.button(label='Emboss', style=discord.ButtonStyle.blurple)
    async def opt_six(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(5)
        
    @ui.button(label='Charcoal', style=discord.ButtonStyle.blurple)
    async def opt_seven(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(6)
        
    @ui.button(label='Wave', style=discord.ButtonStyle.blurple)
    async def opt_eight(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(7)
        
    @ui.button(label='Colorize', style=discord.ButtonStyle.blurple)
    async def opt_nine(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(8)
        
    @ui.button(label='Sepia', style=discord.ButtonStyle.blurple)
    async def opt_ten(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(9)        
    @ui.button(label='Sketch', style=discord.ButtonStyle.blurple)
    async def opt_eleven(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(10)
        
    @ui.button(label='Solarize', style=discord.ButtonStyle.blurple)
    async def opt_twelve(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(11)
        
    @ui.button(label='Swirl', style=discord.ButtonStyle.blurple)
    async def opt_thirteen(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(12)
        
    @ui.button(label='Tint', style=discord.ButtonStyle.blurple)
    async def opt_fourteen(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(13)
        
    @ui.button(label='Reset', style=discord.ButtonStyle.red)
    async def opt_reset(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        await interaction.response.defer()
        await self.update(14)
        