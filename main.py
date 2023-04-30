import discord
import asyncio
import os
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import aiohttp

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
TOKEN = 'MTEwMTY3NTkyODI4OTAzMDI0Ng.GcV4wC.5NWNTsk5vQrY9KEMQAS3OL4-eUHUSiFAP1e21M'
YOUR_YOUTUBE_CHANNEL_ID = 'UChDj6nNr9NgdJbEvocs1ZKQ'
YOUR_SERVER_ID = '1043819044966502411'
YOUR_API_KEY = 'AIzaSyCic3_ymSw1pZsOgAMCqLNDbICaHey5hHs'
API_KEY = os.getenv("YOUTUBE_API_KEY")
DISCORD_CHANNEL_ID = '1043819464992510022'

def get_nicolive_info():
    url = 'https://live.nicovideo.jp/'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
def get_video_title(video_id):
    # YouTube APIを使用して動画の情報を取得
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()

    # タイトルを返す
    items = response.get("items", [])
    if len(items) > 0:
        title = items[0]["snippet"]["title"]
        return title
    else:
        return "Error: Failed to retrieve the title"





async def get_youtube_info(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if "items" in data:
                vid_id = data["items"][0]["id"]["videoId"]
                vid_title = get_video_title(vid_id)
                return {"id": vid_id, "title": vid_title}
            else:
                return None

def get_video_title(vid_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.videos().list(
        part="snippet", id=vid_id)
    response = request.execute()
    title = response['items'][0]['snippet']['title']
    return title

async def check_loop():
    print("Checking for new videos...")
    youtube_info = await get_youtube_info(YOUR_YOUTUBE_CHANNEL_ID)
    if youtube_info is None:
        return

    last_youtube = youtube_info[0]
    if last_youtube != last_video_id:
        last_video_id = last_youtube
        message = f"New video: {youtube_info[1]}\nhttps://www.youtube.com/watch?v={last_video_id}"
        await send_message(DISCORD_CHANNEL_ID, message)
    else:
        print("No new videos found.")

    await check_loop()



# Botがログインした際に呼び出されるイベントハンドラ
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # check_loop()を非同期で実行
    client.loop.create_task(check_loop())

# Botのログイン処理
client.run(TOKEN)
