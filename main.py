

import os

import discord
import youtube
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
YOUTUBE_TOKEN = os.getenv("YOUTUBE_API_KEY")


youtube = build("youtube", "V3", developerKey=YOUTUBE_TOKEN)

request = youtube.commentThreads().list(
    part="snippet",
    allThreadsRelatedToChannelId="UCX2YyFkVhwXGbyPw1euSDnw"
)

response = request.execute()

print(response)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name = GUILD)
    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send("löl")

client.run(TOKEN)