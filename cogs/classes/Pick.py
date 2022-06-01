import discord
from discord.ui.item import Item

from pymongo.collection import Collection
from ast import literal_eval
from discord import ui
from commands.db.classes.MangaDex import MangaDex
from discord.ext.commands import Bot
from typing import Tuple, Dict, Any, List, Optional
from commands.db.classes.MangaDex import Chapter

class PickView(ui.View):
    
    def __init__(self, i: discord.Interaction, channels: Collection[Any], info: Tuple[List[str], List[str]], bot: Bot):
        super().__init__(timeout=60)
        self.i = i
        self.channels = channels
        self.mangas: Dict[str, str] = {}
        self.bot = bot
        self.md: MangaDex = MangaDex(self.bot)
        self.info = info
        self.num_of_results: int = len(self.info[0])
        self.__children: List[Item[Any]]
        if self.num_of_results != len(self.__children):
            for j in range(len(self.__children)-1, self.num_of_results-1, -1):
                self.remove_item(self.__children[j])
        
        
    async def on_timeout(self):
        self.stop()
        await self.msg.edit(content=self.text, embed=self.embed, view=self.disabled())  # type: ignore
        await self.msg.reply("This view just timed out, I suppose! You need to interact with it to keep it up, in fact!")  # type: ignore
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.i.user  # type: ignore
    
    async def find_one(self):
        channel_exist: Dict[str, str] = await self.channels.find_one(  # type: ignore
                        {
                        "channel_id": self.i.channel_id,  # type: ignore
                        "guild_id": self.i.guild.id,  # type: ignore
                        }
                    )
        if not channel_exist:
            channel_exist: Dict[str, str] = await self.channels.insert_one({  # type: ignore
                'channel_id': self.i.channel_id,  # type: ignore
                "guild_id": self.i.guild.id,  # type: ignore
                'mangas': '{}',
            })
            channel_exist: Dict[str, str] = await self.channels.find_one(  # type: ignore
                        {
                        "channel_id": self.i.channel_id,  # type: ignore
                        "guild_id": self.i.guild.id,  # type: ignore
                        }
                    )
        return literal_eval(channel_exist['mangas'])
    
    async def update(self, choice: int):
        res = await self.find_one()
        titles = self.info[0]
        manga_ids = self.info[1]
        if self.i.command.name == "add":  # type: ignore
            if manga_ids[choice] not in res:
                chapter_response: Optional[Chapter] = await self.md.get_latest(manga_ids[choice])
                title_response = chapter_response.get_title()  # type: ignore
                latest = title_response[0]
                res.update({f"{manga_ids[choice]}": str(latest)})
                await self.channels.find_one_and_update(  # type: ignore
                    {
                        'channel_id': self.i.channel_id,  # type: ignore
                        "guild_id": self.i.guild.id,  # type: ignore
                        },
                    {
                        '$set': {
                            'mangas': str(res)
                        }
                    }
                )
                await self.i.channel.send(f"This channel will receive notifications on new chapters of {titles[choice]}, I suppose!")  # type: ignore
        else:
            if manga_ids[choice] in res:
                res.pop(manga_ids[choice])
                await self.channels.find_one_and_update(  # type: ignore
                    {
                        'channel_id': self.i.channel_id,  # type: ignore
                        "guild_id": self.i.guild.id,  # type: ignore
                        },
                    {
                        '$set': {
                            'mangas': str(res)
                        }
                    }
                )
                title = titles[choice]
                await self.i.channel.send(f"This channel will no longer receive notifications on new chapters of {title}, I suppose!")  # type: ignore
            
        
    @ui.button(emoji='1️⃣', style=discord.ButtonStyle.blurple)
    async def opt_one(self, interaction: discord.Interaction, button: discord.ui.Button[Any]):
        await interaction.response.defer()
        await self.update(0)
        
    @ui.button(emoji='2️⃣', style=discord.ButtonStyle.blurple)
    async def opt_two(self, interaction: discord.Interaction, button: discord.ui.Button[Any]):
        await interaction.response.defer()
        await self.update(1)
        
    @ui.button(emoji='3️⃣', style=discord.ButtonStyle.blurple)
    async def opt_three(self, interaction: discord.Interaction, button: discord.ui.Button[Any]):
        await interaction.response.defer()
        await self.update(2)
        
    @ui.button(emoji='4️⃣', style=discord.ButtonStyle.blurple)
    async def opt_four(self, interaction: discord.Interaction, button: discord.ui.Button[Any]):
        await interaction.response.defer()
        await self.update(3)
        
    @ui.button(emoji='5️⃣', style=discord.ButtonStyle.blurple)
    async def opt_five(self, interaction: discord.Interaction, button: discord.ui.Button[Any]):
        await interaction.response.defer()
        await self.update(4)
        
        