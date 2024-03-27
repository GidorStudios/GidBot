	
from random import choice
from datetime import datetime, timedelta
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
from discord.ext.commands import has_permissions, has_guild_permissions, CheckFailure, MissingRequiredArgument, BadArgument, CommandOnCooldown
from bot import fork_version as v

class Giveaway(commands.Cog):


	def __init__(self, client):
		self.client = client
		self.giveaways = []
	
	@commands.Cog.listener()
	async def on_ready(self):
		print("Giveaway module loaded.")

	@commands.command()
	@has_guild_permissions(administrator=True)
	async def giveaway(self, ctx, mins: int, *, description: str):
		embed = discord.Embed(title="Giveaway",
					  description=description + "\n\n React with ✅ to enter the giveaway!",
					  colour=discord.Colour.blue())

		#fields = [("End time", f"{datetime.utcnow()+timedelta(seconds=mins*60)} UTC", False)]

		#for name, value, inline in fields:
		#	embed.add_field(name=name, value=value, inline=inline)
		embed.set_footer(text=f"Ends at {(datetime.utcnow()+timedelta(seconds=mins*60)).__format__('%A, %Y. %m. %d. @ %H:%M:%S')} UTC")
		message = await ctx.send(embed=embed)
		await message.add_reaction(emoji="✅")

		self.giveaways.append((message.channel.id, message.id))

		#self.client.scheduler.add_job(self.complete_giveaway, "date", run_date=datetime.now()+timedelta(seconds=mins),
		#						   args=[message.channel.id, message.id])

		await asyncio.sleep(mins*60)

		await self.complete_giveaway(message.channel.id, message.id)


	async def complete_giveaway(self, channel_id, message_id):
		message = await self.client.get_channel(channel_id).fetch_message(message_id)

		if len((entrants := [u for u in await message.reactions[0].users().flatten() if not u.bot])) > 0:
			winner = choice(entrants)
			await message.channel.send(f"**Congratulations** {winner.mention} - you won the giveaway!")
			self.giveaways.remove((message.channel.id, message.id))

		else:
			await message.channel.send("Giveaway ended - __no one entered__!")
			self.giveaways.remove((message.channel.id, message.id))

	@giveaway.error
	async def giveaway_error(self, ctx, error):
		if isinstance(error, CheckFailure):
			embed=discord.Embed(description=":x: You need **Administrator** permission to use this command!", colour=discord.Colour.red())
			embed.set_footer(text='GidBot | {}'.format(v))
			await ctx.send(embed=embed)
		if isinstance(error, MissingRequiredArgument):
			embed=discord.Embed(description=":x: You forgot to include a reward, and the time.", colour=discord.Colour.red())
			embed.set_footer(text='GidBot | {}'.format(v))
			await ctx.send(embed=embed)
		if isinstance(error, BadArgument):
			embed=discord.Embed(description=":x: Invalid arguments! Usage: g.giveaway [Minute (number)] [Stuff (text)]", colour=discord.Colour.red())
			embed.set_footer(text='GidBot | {}'.format(v))
			await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Giveaway(client))
