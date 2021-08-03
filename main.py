

import os
import time

import discord
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
CHANNEL = os.getenv("DISCORD_CHANNEL")
YOUTUBE_TOKEN = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
YOUTUBE_VIDEO_ID = os.getenv("YOUTUBE_VIDEO_ID")


youtube = build("youtube", "V3", developerKey=YOUTUBE_TOKEN)

request = {}
request = youtube.commentThreads().list(
    part="snippet",
    videoId=YOUTUBE_VIDEO_ID
)

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    channel = client.get_channel(284033672292597761)

    scanForComments = True
    oldCommentThreads = []

    async def get_and_send_replies(commentId, videoTitle, commentThreadAuthorDisplayName):
        repliesRequest = youtube.commentThreads().list(
            part="replies",
            id=commentId
        )
        repliesResponse = repliesRequest.execute()

        repliesMetaData = repliesResponse["items"][0]["replies"]["comments"]
        for replyMetaData in reversed(repliesMetaData):
            replyData = replyMetaData["snippet"]
            embedVar = discord.Embed(title=f"{videoTitle}", description=f"Replied to **{commentThreadAuthorDisplayName}**\nhttps://www.youtube.com/watch?v={replyData['videoId']}&lc={replyMetaData['id']}", color=0x00ff00)
            embedVar.set_image(url=replyData['authorProfileImageUrl'])
            embedVar.add_field(name=f"{replyData['authorDisplayName']}", value=f"{replyData['textOriginal']}", inline=False)
            await channel.send(embed=embedVar)

    while scanForComments:
        response = request.execute()
        commentThreads = response["items"]
        for commentThread in reversed(commentThreads):
            if commentThread not in oldCommentThreads:
                videoId = commentThread["snippet"]["videoId"]
                videoRequest = youtube.videos().list(
                    part="snippet",
                    id=videoId
                )
                videoResponse = videoRequest.execute()
                videoTitle = videoResponse["items"][0]["snippet"]["title"]

                commentThreadData = commentThread["snippet"]
                commentMetaData = commentThreadData["topLevelComment"]
                commentData = commentMetaData["snippet"]
                embedVar = discord.Embed(title=f"{videoTitle}", description=f"Comment\nhttps://www.youtube.com/watch?v={commentData['videoId']}&lc={commentMetaData['id']}", color=0x00ff00)
                embedVar.set_image(url=commentData['authorProfileImageUrl'])
                embedVar.add_field(name=f"{commentData['authorDisplayName']}", value=f"{commentData['textOriginal']}", inline=False)
                await channel.send(embed=embedVar)

                if commentThreadData["totalReplyCount"] > 0:
                    await get_and_send_replies(commentMetaData["id"], videoTitle, commentData['authorDisplayName'])
                
                oldCommentThreads.append(commentThread)

        print(response)
        time.sleep(60)
        print("\n--GO--\n")



client.run(TOKEN)
