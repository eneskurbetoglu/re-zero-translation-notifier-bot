import discord
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import tasks
import threading

load_dotenv()
client = discord.Client()

@tasks.loop(minutes=10)
async def check_chapter():
    page = requests.get('https://witchculttranslation.com/arc-7/')

    soup = BeautifulSoup(page.content, 'html.parser')

    most_recent_post = soup.find_all('h3', 'rpwe-title')[0]

    post_link = most_recent_post.find('a')

    most_recent_post = most_recent_post.text
    most_recent_post_array = most_recent_post.split()

    most_recent_post_str = ""

    for i in range(0, 4):
        most_recent_post_str += most_recent_post_array[i] + " "

    most_recent_post_str = most_recent_post_str.strip()

    li_element = soup.find_all('li', 'rpwe-li rpwe-clearfix')[0]

    try:
        if 'href' in post_link.attrs:
            latest_chapter_translated_link = post_link.get('href')
    except:
        pass

    time_posted = li_element.find('time').text

    text_channel = client.get_channel(int(os.getenv('CHANNEL_ID')))

    last_message = (await text_channel.history(limit=1).flatten())[0].content
    last_message_array = last_message.split()
    last_chapter = ""

    if (len(last_message_array)>3):
        for i in range(0, 4):
            last_chapter += last_message_array[i] + " "

    last_chapter = last_chapter.strip()
    if last_chapter != most_recent_post_str:
        await text_channel.send(
            f'{most_recent_post} has been translated {time_posted}.\n{latest_chapter_translated_link}'
        )

@client.event
async def on_ready():
    check_chapter.start()

client.run(os.getenv('TOKEN'))