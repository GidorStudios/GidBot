
v = "4.3"
token="YOUR TOKEN"
fork_owner_id = 0123456780123 #your user id
fork_version = "1.0"

import random
import hashlib
import time
import datetime
from discord.ext import commands
from asyncio import run
import discord
from discord import channel, opus
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, when_mentioned_or
from bs4 import BeautifulSoup
import asyncio
import os, json
import threading
import logger
import psutil
import urllib
import subprocess
import ast
import aiofiles
import string
import inspect
import io
import textwrap
import traceback
import PIL
from contextlib import redirect_stdout
import re
import nacl
import youtube_dl
import aiohttp
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



def get_prefix(bot, message):
	if not message.guild:
		return commands.when_mentioned_or("g.")(bot, message)
	
	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)

	if str(message.guild.id) not in prefixes:
		return commands.when_mentioned_or("g.")(bot, message)

	prefix = prefixes[str(message.guild.id)]
	return commands.when_mentioned_or(prefix)(bot, message)



client = commands.AutoShardedBot(command_prefix="g." help_command=None, intents=intents)


import logging
import dbl

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
	client.load_extension(f'cogs.moderation')
	client.load_extension(f'cogs.fun')
	client.load_extension(f'cogs.giveaway')

client.loop.create_task(setup())
client.run("TOKEN") 
