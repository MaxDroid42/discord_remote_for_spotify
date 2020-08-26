import discord
import re
import requests

class discordClient(discord.Client):
    async def on_ready(self):
        print("Connected")

    async def on_message(self, message):
        msg_content=message.content
        if msg_content == "skip" or msg_content == "!skip":
            r=requests.post(url="http://127.0.0.1/nexttrack")
        elif msg_content == "pause" or msg_content == "!pause":
            r=requests.post(url="http://127.0.0.1/pause")
        elif msg_content == "play" or msg_content == "!play":
            r=requests.post(url="http://127.0.0.1/play")
        else:
            spotify_link=re.search("track(:|/){1}\w+", msg_content)
            if spotify_link != None:
                spotify_link=spotify_link.group()
                print(spotify_link)
                r=requests.post(url="http://127.0.0.1/addtoqueue", params={"track":spotify_link[6::]})

client=discordClient()
client.run("DISCORD_BOT_TOKEN")