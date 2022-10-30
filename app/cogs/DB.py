import random
import discord
import os
import json

from ast import literal_eval
from aiohttp import ClientSession
from discord import app_commands
from discord.ext import commands, tasks
from typing import List, Any, Dict, Union, Optional, Tuple, Mapping, cast, ClassVar
from pymongo.collection import Collection, ReturnDocument
from pymongo.database import Database
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from dotenv import load_dotenv  # type: ignore

from classes.Re_zero import Re_zero
from classes.Guya_moe import Guya_moe
from classes.Grand_Blue import Grand_Blue
from classes.MangaDex import MangaDex
from classes.Views.Pick import PickView
from classes.Views.Pagination import MangaReader, Source
from Bot import Bot

load_dotenv()


class DB(commands.Cog):

    _IMGUR: ClassVar[Optional[str]] = os.getenv("IMGUR_ID", None)

    def __init__(self, bot: Bot):
        self.bot = bot
        self.client = self.bot.client

        # channels db
        self.db_channels: Database[AsyncIOMotorClient] = self.client.channel_id
        # chapter db
        db_chapter: Database[AsyncIOMotorClient] = self.client.chapter  # type: ignore
        # chapters data
        self.data_rz: Collection[Mapping[str, Any]] = db_chapter.data  # type: ignore
        self.data_kaguya: Collection[Mapping[str, Any]] = db_chapter.data_kaguya  # type: ignore
        self.data_onk: Collection[Mapping[str, Any]] = db_chapter.data_onk  # type: ignore
        self.data_gb: Collection[Mapping[str, Any]] = db_chapter.data_gb  # type: ignore

        # flip image urls db
        db_flips: Database[AsyncIOMotorClient] = self.client.flips  # type: ignore
        # flip image urls data
        self.flips_col: Collection[Mapping[str, Any]] = db_flips.data  # type: ignore

        # avatars url db
        self.db_avatars: Database[AsyncIOMotorClient] = self.client.avatars.data
        # avatars path
        self.avatars = os.path.join(os.getcwd(), "avatars")

        # channels data
        self.channels_md: Collection[Mapping[str, Any]] = db_chapter.data_mangadex  # type: ignore
        self.channels_rz: Collection[Mapping[str, Any]] = self.db_channels.data  # type: ignore
        self.channels_kaguya: Collection[
            Mapping[str, Any]
        ] = self.db_channels.data_kaguya  # type: ignore
        self.channels_onk: Collection[Mapping[str, Any]] = self.db_channels.data_onk  # type: ignore
        self.channels_gb: Collection[Mapping[str, Any]] = self.db_channels.data_gb  # type: ignore

        self.collection_aliases: Dict[str, str] = {
            "data": "Re:Zero",
            "data_kaguya": "Kaguya-sama",
            "data_onk": "Oshi No Ko",
            "data_gb": "Grand Blue Dreaming",
        }

        # urls
        self.rz_url = "https://witchculttranslation.com/arc-7/"
        self.kaguya_url = "https://guya.moe/read/manga/Kaguya-Wants-To-Be-Confessed-To/"
        self.onk_url = "https://guya.moe/read/manga/Oshi-no-Ko/"
        self.gb_url = "https://mangareader.to/grand-blue-dreaming-8/"

        self.aliases = {
            "rezero": "rz",
            "re:zero": "rz",
            "guya": "kaguya",
            "kaguya-sama": "kaguya",
            "kaguya_sama": "kaguya",
            "oshi no ko": "onk",
            "oshi": "onk",
            "oshi_no_ko": "onk",
            "grand_blue": "gb",
            "grand blue": "gb",
            "grand-blue": "gb",
            "grand blue dreaming": "gb",
            "grand_blue_dreaming": "gb",
            "grand-blue-dreaming": "gb",
        }

        self.flips: List[Dict[str, str]] = []
        self.avatar_urls: List[str] = []
        self.mangas_list = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self.tasks_change_avatar.start()
        self.tasks_check_chapter.start()
        # self.tasks_filter_channels.start() NO

    # @commands.command()
    # @commands.is_owner()
    # async def toggle_task(self, ctx: commands.Context[Bot], task: Optional[str]=None):
    #     if task == "avatar":
    #         if self.bot.avatar_task_on:
    #             self.tasks_change_avatar.cancel()
    #         else:
    #             self.tasks_change_avatar.start()
    #         self.bot.avatar_task_on = not self.bot.avatar_task_on
    #     if task == "chapter":
    #         if self.bot.chapter_task_on:
    #             self.tasks_check_chapter.cancel()
    #         else:
    #             self.tasks_check_chapter.start()
    #         self.bot.chapter_task_on = not self.bot.chapter_task_on
    #     await ctx.send(f"Avatar task current state: {self.bot.avatar_task_on}\
    #                     \nChapter task current state: {self.bot.chapter_task_on}")

    async def cog_load(self) -> None:
        self.flips = [flip async for flip in self.flips_col.find()]  # type: ignore

    @commands.command()
    @commands.is_owner()
    async def changepfp(self, ctx: commands.Context[Bot], image: discord.Attachment):
        """Change avatar on command

        Args:
            ctx (commands.Context[Bot]): the context for this command
            image (discord.Attachment): the image
        """
        url: str = "https://api.imgur.com/3/image"

        payload: Dict[str, bytes] = {"image": await image.read()}
        headers: Dict[str, str] = {"Authorization": f"Client-ID {self._IMGUR}"}
        session: ClientSession = self.bot.session
        async with session.post(url, data=payload, headers=headers) as r:
            r = await r.read()
            r = json.loads(r)
            img_url: str = r["data"]["link"]
            await self.db_avatars.insert_one(  # type: ignore
                {
                    "url": img_url,
                }
            )
            self.avatar_urls.append(img_url)
        await self.bot.user.edit(avatar=await image.read())
        await ctx.send("Avatar changed, I suppose!")

    @app_commands.command(name="flip")
    async def commands_flip(self, i: discord.Interaction):
        """Flip your friends.

        Args:
            i (discord.Interaction): the interaction that invokes this coroutine
        """
        flip_dict: Dict[str, str] = random.choice(self.flips)
        flip_url: str = flip_dict.get("url", "")
        await i.response.send_message(flip_url)

    async def send_messages(
        self,
        channels: Collection[Mapping[str, Any]],
        title: str,
        data: Collection[Mapping[str, Any]],
        db_rec: Dict[str, str],
        anchor: str,
    ):
        """Sends the notification messages to all the relevant guild channels.

        Args:
            channels (motor.motor_asyncio.AsyncIOMotorCollection): relevant channels collection
            title (str): the scraped or response title to compare with the database
            data (motor.motor_asyncio.AsyncIOMotorCollection): chapter collection of the relevant series to update if necessary
            db_rec (dict): the latest document in the database of the relevant series
            anchor (str): link to the chapter
        """
        if db_rec["title"] != title:
            await data.find_one_and_update(  # type: ignore
                {"title": str(db_rec["title"])}, {"$set": {"title": title}}
            )
            async for channel in channels.find():  # type: ignore
                channel_if_exists = self.bot.get_guild(channel["guild_id"]).get_channel(  # type: ignore
                    (channel["id"])  # type: ignore
                )
                if channel_if_exists:
                    try:
                        await channel_if_exists.send(  # type: ignore
                            f"'{title}' has been translated.\n{anchor}, I suppose!"
                        )
                    except Exception as e:
                        print(
                            f"The channel with id {channel['id']} is private, I suppose!",
                            e,
                        )

    @tasks.loop(seconds=60 * 15)
    async def tasks_check_chapter(self):
        """Checks for the newest chapters every minute."""
        try:
            # for re zero
            rz = Re_zero(self.rz_url, self.bot)

            scrapes = await rz.scrape()
            most_recent_post_str = scrapes[0]
            latest_chapter_translated_link = scrapes[1]

            last_chapter: Dict[str, str] = await self.data_rz.find_one()  # type: ignore

            await self.send_messages(
                self.channels_rz,
                most_recent_post_str,
                self.data_rz,
                last_chapter,
                latest_chapter_translated_link,
            )

            # for kaguya-sama
            kaguya = Guya_moe(self.kaguya_url, self.bot)

            scrapes = await kaguya.scrape()
            most_recent_post_str = scrapes[0]
            latest_chapter_translated_link = scrapes[1]

            last_chapter = await self.data_kaguya.find_one()  # type: ignore

            await self.send_messages(
                self.channels_kaguya,
                most_recent_post_str,
                self.data_kaguya,
                last_chapter,
                latest_chapter_translated_link,
            )

            # for oshi no ko
            onk = Guya_moe(self.onk_url, self.bot)

            scrapes = await onk.scrape()
            most_recent_post_str = scrapes[0]
            latest_chapter_translated_link = scrapes[1]

            last_chapter = await self.data_onk.find_one()  # type: ignore

            await self.send_messages(
                self.channels_onk,
                most_recent_post_str,
                self.data_onk,
                last_chapter,
                latest_chapter_translated_link,
            )

            # for grand blue
            gb = Grand_Blue(self.gb_url, self.bot)

            scrapes = await gb.scrape()
            most_recent_post_str = scrapes[0]
            latest_chapter_translated_link = scrapes[1]

            last_chapter = await self.data_gb.find_one()  # type: ignore

            await self.send_messages(
                self.channels_gb,
                most_recent_post_str,
                self.data_gb,
                last_chapter,
                latest_chapter_translated_link,
            )

            # for mangadex
            md = MangaDex(self.bot)
            records_exist: List[
                Mapping[str, Any]
            ] = await self.channels_md.find().to_list(  # type: ignore
                None
            )
            if records_exist:
                for record in records_exist:
                    mangas_on_channel = (record)["mangas"]
                    ignore_no_groups = record.get("ignore_no_group", [])
                    mangas_dict = literal_eval(mangas_on_channel)
                    for manga_id in mangas_dict:
                        chapter = mangas_dict[manga_id]
                        chapter_response = await md.get_latest(manga_id)
                        volume = chapter_response.volume
                        chapter_num = chapter_response.num
                        title_response = chapter_response.get_title()
                        latest = title_response[0]
                        is_title = title_response[1]
                        chapter_link = chapter_response.get_link()
                        scanlation_group = None
                        if chapter_response.scanlation:
                            scanlation_group = await md.get_scanlation_group(
                                chapter_response.scanlation
                            )
                        if scanlation_group is None and manga_id in ignore_no_groups:
                            continue
                        if latest != chapter:
                            mangas_dict.update({f"{manga_id}": str(latest)})
                            await self.channels_md.find_one_and_update(  # type: ignore
                                {
                                    "channel_id": record["channel_id"],
                                    "guild_id": record["guild_id"],
                                },
                                {"$set": {"mangas": str(mangas_dict)}},
                            )
                            channel = record["channel_id"]
                            chp_title = await md.get_manga_title(manga_id)
                            embed = discord.Embed(
                                color=discord.Colour.random(),
                                title=str(latest),
                            )
                            if volume is None:
                                volume = "-"
                            num_of_pages = len(chapter_response.images)
                            if num_of_pages == 0:
                                if is_title:
                                    await self.bot.get_channel(channel).send(  # type: ignore
                                        f"'{chp_title} - {latest}' (Volume {volume}, Chapter {chapter_num}) has been translated, I suppose! \n{chapter_link}"
                                    )
                                else:
                                    await self.bot.get_channel(channel).send(  # type: ignore
                                        f"A new chapter of '{chp_title}' (Volume {volume}, Chapter {chapter_num}) has been translated, I suppose! \n{chapter_link}"
                                    )
                                continue
                            current_page = 0
                            group = "No group"
                            if scanlation_group:
                                group: str = scanlation_group["data"]["attributes"]["name"]  # type: ignore
                            embed.set_footer(
                                text=(
                                    f"Volume {volume}, Chapter {chapter_num} - "
                                    + f"Page {current_page+1}/{num_of_pages}. Translated by "
                                    + group
                                )
                            )
                            embed.set_image(url=chapter_response.images[current_page])

                            data = chapter_response.images
                            formatter = Source(data, per_page=1)
                            menu = MangaReader(formatter)
                            chnl: Union[
                                discord.abc.GuildChannel,
                                discord.Thread,
                                discord.abc.PrivateChannel,
                            ] = self.bot.get_channel(
                                channel
                            )  # type: ignore

                            if is_title:
                                text, embed = (
                                    f"'{chp_title} - {latest}' has been translated, I suppose \n{chapter_link}",
                                    embed,
                                )
                            else:
                                text, embed = (
                                    f"A new chapter of '{chp_title}' has been translated, I suppose \n{chapter_link}",
                                    embed,
                                )

                            await menu.start(
                                interaction=None,
                                channel=chnl,
                                text=text,
                                embed=embed,
                                group=group,
                                is_task=True,
                            )

        except Exception as e:
            print(e)

    async def last_chapter(self, series: str, i: discord.Interaction) -> None:
        """Sends the latest chapter info or the reader.

        Args:
            series (str): the series to check
            i (discord.Interaction): the interaction that invokes this coroutine
        """
        series = self.aliases[series] if series in self.aliases else series
        if series == "rz":
            await i.response.send_message(
                await Re_zero(self.rz_url, self.bot).latest_chapter()
            )
        elif series == "kaguya":
            await i.response.send_message(
                await Guya_moe(self.kaguya_url, self.bot).latest_chapter()
            )
        elif series == "onk":
            await i.response.send_message(
                await Guya_moe(self.onk_url, self.bot).latest_chapter()
            )
        elif series == "gb":
            await i.response.send_message(
                await Grand_Blue(self.gb_url, self.bot).latest_chapter()
            )
        else:
            md = MangaDex(self.bot)
            search: Optional[List[Any]] = await md.search(series, "1")
            search_query: str = ""
            if search:
                search_query = search[-1][0]
            chapter_response = await md.get_latest(search_query)
            volume = chapter_response.volume
            chapter_num = chapter_response.num
            chp_title = await md.get_manga_title(search_query)
            scanlation_group = None
            if chapter_response.scanlation is not None:
                scanlation_group = await md.get_scanlation_group(
                    chapter_response.scanlation
                )
            title_response = chapter_response.get_title()
            latest = title_response[0]
            is_title = title_response[1]
            chapter_link = chapter_response.get_link()
            embed = discord.Embed(
                color=discord.Colour.random(),
                title=str(latest),
            )
            if volume is None:
                volume = "-"
            num_of_pages = len(chapter_response.images)
            if num_of_pages == 0:
                if is_title:
                    await i.response.send_message(
                        f"'{chp_title} - {latest}' (Volume {volume}, Chapter {chapter_num}) has been translated, I suppose! \n{chapter_link}"
                    )
                else:
                    await i.response.send_message(
                        f"A new chapter of '{chp_title}' (Volume {volume}, Chapter {chapter_num}) has been translated, I suppose! \n{chapter_link}"
                    )
                return
            current_page = 0
            group: Optional[str] = None
            if scanlation_group is not None:
                group = scanlation_group["data"]["attributes"]["name"]  # type: ignore
            embed.set_footer(
                text=(
                    f"Volume {volume}, Chapter {chapter_num} - "
                    f"Page {current_page+1}/{num_of_pages}. Translated by "
                    + (group or "Unknown")
                )
            )
            embed.set_image(url=chapter_response.images[current_page])
            await i.response.send_message("Read away, I suppose!")

            data = chapter_response.images
            formatter = Source(data, per_page=1)
            menu = MangaReader(formatter)

            if is_title:
                text, embed = (
                    f"'{chp_title} - {latest}' has been translated, I suppose \n{chapter_link}",
                    embed,
                )
            else:
                text, embed = (
                    f"A new chapter of '{chp_title}' has been translated, I suppose \n{chapter_link}",
                    embed,
                )

            await menu.start(
                interaction=i, channel=i.channel, text=text, embed=embed, group=group
            )

    async def manga_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        """An autocomplete function

        Args:
            interaction (discord.Interaction): the interaction that invokes this coroutine
            current (str): whatever the user has typed as the input

        Returns:
            List[app_commands.Choice[str]]: The list of choices matching the input
        """
        await self.sync(current)
        return [
            app_commands.Choice(
                name=manga["attributes"]["title"]["en"][:100],  # type: ignore
                value=manga["attributes"]["title"]["en"][:100],  # type: ignore
            )
            for manga in self.mangas_list  # type: ignore
            if "en" in manga["attributes"]["title"].keys()  # type: ignore
            and current.lower() in manga["attributes"]["title"]["en"].lower()  # type: ignore
            or any("en" in list(x.keys()) for x in manga["attributes"]["altTitles"])  # type: ignore
            and any(current.lower() in list(x.values())[0].lower() for x in manga["attributes"]["altTitles"])  # type: ignore
        ][:25]

    @app_commands.command(name="last")
    @app_commands.autocomplete(series=manga_autocomplete)
    @app_commands.describe(
        series="The series you want to get the latest chapter of, in fact!"
    )
    async def commands_latest_chapter(self, i: discord.Interaction, series: str):
        """Get the latest chapter of a series.

        Args:
            i (discord.Interaction): the interaction that invokes this coroutine
            series (str, optional): the series to know about. Defaults to "".

        Returns:
            None: None
        """
        await self.last_chapter(series, i)

    # send manga info
    @app_commands.command(name="manga")
    @app_commands.autocomplete(series=manga_autocomplete)
    @app_commands.describe(
        series="The series you want to get information about, I suppose!"
    )
    async def commands_get_manga_info(self, i: discord.Interaction, series: str):
        """Get info on a manga.

        Args:
            i (discord.Interaction): the interaction that invokes this coroutine
            series (str): the series to know about
        """
        md = MangaDex(self.bot)
        embed = await md.get_info(series)
        if embed:
            await i.response.send_message(embed=embed)
        else:
            await i.response.send_message(
                "Couldn't find that, in fact! Make sure to select from the choices, if there are any matches they will show up there, I suppose!"
            )

    async def sync(self, query: str):
        """The function called everytime the input on mangadex related autocomplete argument changes.

        Args:
            query (str): query that will be sent to the api
        """
        session: ClientSession = self.bot.session
        async with session.get(
            f"https://api.mangadex.org/manga?limit=25&title={query}&availableTranslatedLanguage%5B%5D=en&order%5BlatestUploadedChapter%5D=desc&contentRating%5B%5D=safe&contentRating%5B%5D=suggestive&contentRating%5B%5D=erotica&contentRating%5B%5D=pornographic"
        ) as r:
            if r.status == 200:
                response = await r.read()
                self.mangas_list = json.loads(response)["data"]
            else:
                print("MangaDex down!")

    @app_commands.command(name="add")
    @app_commands.guild_only
    @app_commands.autocomplete(series=manga_autocomplete)
    @app_commands.describe(
        series="The series you want to track in this channel, in fact!"
    )
    @app_commands.choices(
        include_all=[
            app_commands.Choice(name="Ignore", value="0"),
            app_commands.Choice(name="Include", value="1"),
        ]
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def commands_add_channel(
        self,
        i: discord.Interaction,
        series: Optional[str] = None,
        id: Optional[str] = None,
        include_all: Optional[app_commands.Choice[str]] = None,
    ):
        """Add a series to track to this channel. You can either search for it with the 'series' argument or enter the id. You can also ignore individual (No Group) translations (default includes).

        Args:
            i (discord.Interaction): the interaction that invokes this coroutine
            series (str): the series to add this channel's tracking list
            id (str): the id of the series to add this channel's tracking list
            include_all (bool): whether to include individual translations
        """
        if series is not None:
            md = MangaDex(self.bot)
            channel_entry: Dict[str, int] = {
                "id": i.channel_id,  # type: ignore
                "guild_id": i.guild.id,
            }
            series = self.aliases[series] if series in self.aliases else series
            success_msg = "This text channel will receive notifications, I suppose!"
            failure_msg = "This text channel is already on the receiver list, in fact!"
            is_in_list = self.channels_rz.count_documents(channel_entry, limit=1) != 0  # type: ignore
            is_in_kaguya_list = (
                self.channels_kaguya.count_documents(channel_entry, limit=1) != 0  # type: ignore
            )
            is_in_onk_list = self.channels_onk.count_documents(channel_entry, limit=1) != 0  # type: ignore
            is_in_gb_list = self.channels_gb.count_documents(channel_entry, limit=1) != 0  # type: ignore
            if series == "rz":
                if not is_in_list:
                    await self.channels_rz.insert_one(channel_entry)  # type: ignore
                    msg = success_msg
                else:
                    msg = failure_msg
            elif series == "kaguya":
                if not is_in_kaguya_list:
                    await self.channels_kaguya.insert_one(channel_entry)  # type: ignore
                    msg = success_msg
                else:
                    msg = failure_msg
            elif series == "onk":
                if not is_in_onk_list:
                    await self.channels_onk.insert_one(channel_entry)  # type: ignore
                    msg = success_msg
                else:
                    msg = failure_msg
            elif series == "gb":
                if not is_in_gb_list:
                    await self.channels_gb.insert_one(channel_entry)  # type: ignore
                    msg = success_msg
                else:
                    msg = failure_msg
            elif series == "" or series == " ":
                msg = "To what list do you want to add this channel, in fact?!"
            else:
                md = MangaDex(self.bot)
                results = await md.search(series, "5")
                msg = results

            if isinstance(msg, list):
                titles = msg[2]
                manga_ids = msg[3]
                msg = msg[1]
                manga_infos = (titles, manga_ids)
                await i.response.send_message(
                    "Pick a series to follow, I suppose!",
                    embed=msg,
                    view=PickView(i, self.channels_md, manga_infos, self.bot, msg),
                )
            else:
                await i.response.send_message(msg)
        elif series is None:
            if id is None:
                return await i.response.send_message(
                    "Either the title or the exact ID of the series is required, in fact!"
                )

            md = MangaDex(self.bot)
            found = await md.find(id)

            if not found:
                return await i.response.send_message("I couldn't find that, I suppose!")

            channel_exist: Dict[str, Any] = await self.channels_md.find_one(  # type: ignore
                {
                    "channel_id": i.channel_id,
                    "guild_id": i.guild.id,
                }
            )
            if not channel_exist:
                channel_exist: Dict[str, Any] = await self.channels_md.insert_one(  # type: ignore
                    {
                        "channel_id": i.channel_id,
                        "guild_id": i.guild.id,
                        "mangas": "{}",
                        "ignore_no_group": [],
                    }
                )
                channel_exist: Dict[str, Any] = await self.channels_md.find_one(  # type: ignore
                    {
                        "channel_id": i.channel_id,
                        "guild_id": i.guild.id,
                    }
                )
            if not channel_exist.get("ignore_no_group", False):
                channel_exist = await self.channels_md.find_one_and_update(  # type: ignore
                    {
                        "channel_id": i.channel_id,
                        "guild_id": i.guild.id,
                    },
                    {
                        "$set": {
                            "ignore_no_group": [],
                        }
                    },
                    return_document=ReturnDocument.AFTER,
                )
            res = (
                literal_eval(channel_exist["mangas"]),
                channel_exist["ignore_no_group"],
            )

            if id not in res[0]:
                res[0].update({f"{id}": "null"})
                if include_all is not None:
                    if include_all.value == "0":
                        res[1].append(id)
                await self.channels_md.find_one_and_update(  # type: ignore
                    {
                        "channel_id": i.channel_id,
                        "guild_id": i.guild.id,
                    },
                    {
                        "$set": {
                            "mangas": str(res[0]),
                            "ignore_no_group": res[1],
                        }
                    },
                )
                await i.response.send_message(
                    f"This channel will receive notifications on new chapters of the manga with ID: {id}, I suppose!"
                )
            else:
                await i.response.send_message(
                    f"This channel is already following this series, I suppose!"
                )

    @app_commands.command(name="remove")
    @app_commands.guild_only
    @app_commands.describe(
        series="The series you want to stop tracking in this channel, I suppose!"
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def commands_remove_channel(
        self, i: discord.Interaction, series: Optional[str]
    ):
        """Remove a series this channel is tracking.

        Args:
            i (discord.Interaction): the interaction that invokes this coroutine
            series (str, optional): the series to remove from this channel's tracking list. Defaults to "".
        """
        md = MangaDex(self.bot)
        channel_entry: Dict[str, int] = {
            "id": i.channel_id,  # type: ignore
            "guild_id": i.guild.id,
        }
        series = self.aliases[series] if series in self.aliases else series
        success_msg = (
            "This text channel will no longer receive notifications, I suppose!"
        )
        failure_msg = "This text channel is not on the receiver list, in fact!"
        is_in_list = self.channels_rz.count_documents(channel_entry, limit=1) != 0  # type: ignore
        is_in_kaguya_list = (
            self.channels_kaguya.count_documents(channel_entry, limit=1) != 0  # type: ignore
        )
        is_in_onk_list = self.channels_onk.count_documents(channel_entry, limit=1) != 0  # type: ignore
        is_in_gb_list = self.channels_gb.count_documents(channel_entry, limit=1) != 0  # type: ignore
        if series == "rz":
            if is_in_list:
                await self.channels_rz.find_one_and_delete(channel_entry)  # type: ignore
                msg = success_msg
            else:
                msg = failure_msg
        elif series == "kaguya":
            if is_in_kaguya_list:
                await self.channels_kaguya.find_one_and_delete(channel_entry)  # type: ignore
                msg = success_msg
            else:
                msg = failure_msg
        elif series == "onk":
            if is_in_onk_list:
                await self.channels_onk.find_one_and_delete(channel_entry)  # type: ignore
                msg = success_msg
            else:
                msg = failure_msg
        elif series == "gb":
            if is_in_gb_list:
                await self.channels_gb.find_one_and_delete(channel_entry)  # type: ignore
                msg = success_msg
            else:
                msg = failure_msg
        else:
            channel_exists: Dict[str, Union[str, int]] = (
                True
                if await self.channels_md.find_one(  # type: ignore
                    {
                        "channel_id": i.channel_id,
                        "guild_id": i.guild.id,
                    }
                )
                else False
            )
            if not channel_exists:
                return await i.response.send_message(
                    "This channel is not on any receiver list, in fact!"
                )

            mangas_on_channel: str = (
                await self.channels_md.find_one(  # type: ignore
                    {
                        "channel_id": i.channel_id,
                        "guild_id": i.guild.id,
                    }
                )
            )["mangas"]
            mangas_dict: Dict[str, str] = literal_eval(mangas_on_channel)

            embed = discord.Embed(
                title=f"Pick one of the series you wish to unfollow, I suppose! Only 5 series are shown at a time, in fact!"
                if len(mangas_dict) > 0
                else "This channel is not following any series, in fact!\n Use `/add <manga_title>` to pick some series to start, I suppose!",
                color=discord.Colour.random(),
            )

            titles: List[str] = []
            manga_ids: List[str] = []
            emojis = md.emojis
            for j, rs in enumerate(mangas_dict):
                if j > 4:
                    break
                manga_ids.append(rs)
                title = await md.get_manga_title(rs)
                if title:
                    titles.append(title)
                    title += f" {emojis[j]}"
                embed.add_field(name=title, value="\u200b", inline=False)

            msg = [embed, manga_ids, titles, emojis]

        if isinstance(msg, list):
            emojis = msg[3]
            manga_ids = msg[1]  # type: ignore
            titles = msg[2]  # type: ignore
            msg = msg[0]
            manga_infos: Tuple[List[str], List[str]] = (titles, manga_ids)
            await i.response.send_message(
                "Pick a series to follow, I suppose!",
                embed=msg,  # type: ignore
                view=PickView(i, self.channels_md, manga_infos, self.bot, msg),  # type: ignore
            )
        else:
            await i.response.send_message(msg)

    @tasks.loop(hours=12)
    async def tasks_change_avatar(self):
        """Task that changes the bot's avatar twice a day."""
        async for image_record in self.db_avatars.find():  # type: ignore
            url: str = image_record["url"]
            if url not in self.avatar_urls:
                self.avatar_urls.append(url)

        url = random.choice(self.avatar_urls)
        session: ClientSession = self.bot.session
        async with session.get(url) as resp:
            if resp.status == 200:
                bytes_image = await resp.read()

        await self.bot.wait_until_ready()
        await self.bot.user.edit(avatar=bytes_image)
        print("Avatar changed successfully!")

    @tasks_change_avatar.before_loop
    async def wait_ready(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds=60)
    async def tasks_filter_channels(self):
        """Task that filters out deleted channels from the database every 60 seconds."""
        async for channel in self.channels_rz.find():  # type: ignore
            if (
                self.bot.get_guild(channel["guild_id"]) is None  # type: ignore
                or self.bot.get_guild(channel["guild_id"]).get_channel((channel["id"]))  # type: ignore
                is None
            ):
                channel_entry: Mapping[str, Any] = {
                    "id": channel["id"],
                }
                await self.channels_rz.find_one_and_delete(channel_entry)  # type: ignore
        async for channel in self.channels_kaguya.find():  # type: ignore
            if (
                self.bot.get_guild(channel["guild_id"]) is None  # type: ignore
                or self.bot.get_guild(channel["guild_id"]).get_channel((channel["id"]))  # type: ignore
                is None
            ):
                channel_entry = {
                    "id": channel["id"],
                }
                await self.channels_kaguya.find_one_and_delete(channel_entry)  # type: ignore
        async for channel in self.channels_onk.find():  # type: ignore
            if (
                self.bot.get_guild(channel["guild_id"]) is None  # type: ignore
                or self.bot.get_guild(channel["guild_id"]).get_channel((channel["id"]))  # type: ignore
                is None
            ):
                channel_entry = {
                    "id": channel["id"],
                }
                await self.channels_onk.find_one_and_delete(channel_entry)  # type: ignore
        async for channel in self.channels_gb.find():  # type: ignore
            if (
                self.bot.get_guild(channel["guild_id"]) is None  # type: ignore
                or self.bot.get_guild(channel["guild_id"]).get_channel((channel["id"]))  # type: ignore
                is None
            ):
                channel_entry = {
                    "id": channel["id"],
                }
                await self.channels_gb.find_one_and_delete(channel_entry)  # type: ignore
        async for channel in self.channels_md.find():  # type: ignore
            if (
                self.bot.get_guild(channel["guild_id"]) is None  # type: ignore
                or self.bot.get_guild(channel["guild_id"]).get_channel(  # type: ignore
                    (channel["channel_id"])  # type: ignore
                )
                is None
            ):
                channel_entry = {
                    "channel_id": channel["channel_id"],
                    "guild_id": channel["guild_id"],
                }
                await self.channels_md.find_one_and_delete(channel_entry)  # type: ignore

    @app_commands.command(name="following")
    @app_commands.guild_only
    async def commands_following(self, i: discord.Interaction):
        """Check what series this channel is tracking.

        Args:
            i (discord.Interaction): the interaction that invokes this coroutine
        """
        await i.response.defer()
        series: List[str] = []
        all_channels: List[str] = await self.db_channels.list_collection_names()  # type: ignore
        for channels in all_channels:
            async for channel in self.db_channels[channels].find():  # type: ignore
                if self.bot.get_channel(cast(int, channel["id"])) == i.channel:
                    series.append(self.collection_aliases[channels])

        channel_exists: Dict[
            str, Any
        ] = await self.channels_md.find_one(  # type: ignore
            {
                "channel_id": i.channel_id,
                "guild_id": i.guild.id,
            }
        )
        if channel_exists:
            md = MangaDex(self.bot)
            mangas_on_channel = (channel_exists)["mangas"]
            mangas_dict = literal_eval(mangas_on_channel)
            for manga_id in mangas_dict:
                manga_title = await md.get_manga_title(manga_id)
                if manga_title:
                    series.append(manga_title)

        frame = discord.Embed(
            color=discord.Colour.random(),
            title="This channel is following the series below, in fact!"
            if len(series) > 0
            else "This channel is not following any series, I suppose!",
            description=""
            if len(series) > 0
            else "Use `/add <series>` to start following a series on this channel, in fact!",
        )
        if len(series) > 0:
            counter = 1
            desc = ""
            for s in series:
                desc += f"**{counter}.** {s}\n"
                counter += 1
            frame.description = desc
        await i.followup.send(embed=frame)


async def setup(bot: Bot):
    await bot.add_cog(DB(bot))
