import discord
from discord.ext import commands
from asyncio import sleep, timeout
import asyncio
import logging
from steam import game_servers as gs
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
PORT_SERVER = os.getenv("PORT_SERVER")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="/", intents=intents)

async def GetInfoServer():
    try:
        global SERVER_ADDRESS
        global PORT_SERVER
        data = gs.a2s_info((SERVER_ADDRESS, PORT_SERVER), timeout=4)
    except:
        return None
    if data is None:
        return data
    return None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    asyncio.create_task(BotStatus())
    global SavedServerInfo
    SavedServerInfo = await GetInfoServer()

async def BotStatus():
    global SavedServerInfo
    while True:
        try:
            response = await GetInfoServer()
            SavedServerInfo = response
            if response:
                players = response.get("players")
                maxplayers = response.get("max_players")
                map_name = response.get("map")
                ping = response.get("_ping")
                await bot.change_presence(
                    activity=discord.Activity(
                        name="Map:" + str(map_name) + "| Spieler:" + str(players) + "/" + str(maxplayers),
                        type=discord.ActivityType.playing,
                        state="Ping:" + str(ping) + "ms",
                        application_id=1349029817122553886,
                        large_image_url="https://raw.githubusercontent.com/ich777/docker-templates/master/ich777/images/dayz.png"
                    )
                )
            else:
                await bot.change_presence(
                    activity=discord.Game(name="Server: Offline")
                )
        except Exception as e:
            print(e)
        await sleep(60)

bot.run(token,log_handler=handler, log_level=logging.DEBUG)