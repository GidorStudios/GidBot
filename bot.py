
"""
This bot is heavily outdated, and was written with zero documentation (little or no commenting).
The bot was just a hobby project made for fun in the early days of 2018 and until 2021 then it wasn't maintained.
It's also not designed to be used as a template for other bots. It doesn't follow best practices in terms of code organization, because I started working on it
when I was still a begineer in python. It's not recommended to use this code as it may be difficult to understand for someone new to .
It's meant to be a starting point, not an example of how to write discord bot.

The bot was abandoned for these reasons above, and because I wanted to make a better more organized bot. Which now runs under the name Pulsar. 
The new bot has been built from the ground up. It uses the py-cord library instead of kinda abandoned discord.py. 
I recommend trying out the new bot.
"""

v = "4.3"
token="YOUR TOKEN"
fork_owner_id = 0123456780123 #your user id
fork_version = "1.0"

from discord.ext import commands
from asyncio import run
import discord
from discord import channel, opus
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, when_mentioned_or
from bs4 import BeautifulSoup
import asyncio
from contextlib import redirect_stdout
import requests as rq
from asyncio.subprocess import PIPE
from io import BytesIO
from PIL import Image, ImageChops 
from discord.ext.commands import is_nsfw, is_owner, has_permissions, has_guild_permissions, CheckFailure, MissingRequiredArgument, BadArgument, CommandOnCooldown
intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.presence = True
from discord_slash import SlashCommand, SlashContext

client = commands.AutoShardedBot(command_prefix="g.", help_command=None, intents=intents)

def is_me():
    def predicate(ctx):
        return ctx.message.author.id == fork_owner_id
    return commands.check(predicate)

@client.event
async def on_ready():
	print ("Bot.py Loaded succesfully!")
	print ("A wild bot appeared!")
	counter = 0
	while not counter > 0:
		await client.change_presence(status=discord.Status.idle, activity=discord.Game(name='Used on {} servers'.format(len(client.guilds)), type=discord.ActivityType.watching)) 
		await asyncio.sleep(40)
		await client.change_presence(status=discord.Status.idle, activity=discord.Game(name='Type g.help | {}-Fork'.format(fork_version), type=0))
		await asyncio.sleep(40)


async def setup():
	client.load_extension(f'cogs.eventhandler')
	client.load_extension(f'cogs.economy')
	client.load_extension(f'cogs.dashboard')
	client.load_extension(f'cogs.general')
	client.load_extension(f'cogs.music')
	client.load_extension(f'cogs.moderation')
	client.load_extension(f'cogs.fun')
	client.load_extension(f'cogs.giveaway')

client.loop.create_task(setup())
client.run("TOKEN") 
