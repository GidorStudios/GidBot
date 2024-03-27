import datetime
from typing import Type
from discord.errors import ClientException
from discord.errors import DiscordException, HTTPException
from discord.ext import commands
from asyncio import run
import discord
from discord import channel, opus
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, when_mentioned_or
from bs4 import BeautifulSoup
import asyncio
from contextlib import redirect_stdout
import youtube_dl
import requests as rq
from asyncio.subprocess import PIPE
from io import BytesIO
from PIL import Image, ImageChops 
from discord.ext.commands import has_permissions, CheckFailure, MissingRequiredArgument, BadArgument, CommandOnCooldown, has_any_role

import pafy

queue_len = 0
from bot import fork_version as v

class Music(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.song_queue = {}
		self.setup()

	@commands.Cog.listener()
	async def on_ready(self):
		print("Music module loaded.")

	def setup(self):
		for guild in self.client.guilds:
			self.song_queue[guild.id] = []            

	async def check_queue(self, ctx):
		if len(self.song_queue[ctx.guild.id]) > 0:
			ctx.voice_client.stop()
			await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
			self.song_queue[ctx.guild.id].pop(0)



	async def search_song(self, amount, song, get_url=False):
		info = await self.client.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
		if len(info["entries"]) == 0: return None

		return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

	async def play_song(self, ctx, song):
		url = pafy.new(song).getbestaudio().url
		ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.client.loop.create_task(self.check_queue(ctx)))
		ctx.voice_client.source.volume = 0.5


	

	@commands.command(aliases=["connect"])
	async def join(self, ctx):
		if ctx.author.voice is None:
			embed = discord.Embed(description=':x: You are not conencted to a voice channel, please connect to the channel you want the bot to join!', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
			return await ctx.send(embed=embed)

		if ctx.voice_client is not None:
			await ctx.voice.client.disconnect()

		await ctx.author.voice.channel.connect()
		embed = discord.Embed(description=f'<a:check:677157258320150530> Connected to voice channel {ctx.author.voice.channel}!', color=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
		await ctx.send(embed=embed)

	@commands.command(aliases=["stop", "left"])
	async def leave(self, ctx):
		if ctx.voice_client is not None:
			await ctx.voice_client.disconnect()
			embed = discord.Embed(description='<a:check:677157258320150530> Disconnected from voice channel, and cleared the queue!', color=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
			return await ctx.send(embed=embed)
		embed = discord.Embed(description=':x: I am not connected to any voice channel!', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
		await ctx.send(embed=embed)

	@commands.command(aliases=["p"])
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def play(self, ctx, *, song=None):
		global queue_len
		if song is None:
			embed = discord.Embed(description=':x: You must include a something to play!', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
			return await ctx.send(embed=embed)

		c = self.client.get_channel(id=555057369931972632)
		#handle song where song isn't url
		if ctx.voice_client is None:
			await ctx.author.voice.channel.connect()

		if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
			embed = discord.Embed(description='<a:loading:853609809936515122> Searching for song, this may take a few seconds.', color=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
			play_msg = await ctx.send(embed=embed)

			play_id = play_msg.id

			play_msg = await ctx.channel.fetch_message(play_id)

			result = await self.search_song(1, song, get_url=True)

			if result is None:
				embed = discord.Embed(description=':x: Sorry, I could not find the given song, try using my search command.', color=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
				return await play_msg.edit(embed=embed)

			song = result[0]
			
		if ctx.voice_client.source is not None:
			
			queue_len = len(self.song_queue[ctx.guild.id])

			if queue_len < 10:
				self.song_queue[ctx.guild.id].append(song)
				await c.send("Music added to queue: **{}** in **{}**=**{}**".format(song, ctx.message.guild.id, ctx.message.guild.name))
				embed = discord.Embed(description=f"<a:check:677157258320150530> {song} has been added to the queue at position {queue_len+1}.", color=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
				return await ctx.send(embed=embed)
			else: 
				await c.send("Queue full in: **{}**=**{}**".format(ctx.message.guild.id, ctx.message.guild.name))
				embed = discord.Embed(description=f":x: Sorry, i can only queue up to 10 songs, please wait for the current song to finish.", color=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
				return await ctx.send(embed=embed)
			
	
				
		await c.send("Playing music: **{}** in **{}**=**{}**".format(song, ctx.message.guild.id, ctx.message.guild.name))
			
		await self.play_song(ctx, song)
		embed = discord.Embed(description=f"<a:check:677157258320150530> Playing song: {song}", color=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		await ctx.send(embed=embed)




	@play.error
	async def play_error(self, ctx, error):
		if isinstance(error, TypeError):
			embed=discord.Embed(description=":x: Unexpected error occured.", colour=discord.Colour.red())
			embed.set_footer(text='GidBot | {}'.format(v))
			await ctx.send(embed=embed)
			c = self.client.get_channel(id=555057369931972632)
			errorlog = self.client.get_channel(id=744973883890991264)
			await c.send("Play command used in **{}**=**{}** (TypeError occured.)".format(ctx.message.guild.id, ctx.message.guild.name))
			await errorlog.send(error) 		
		if isinstance(error, ClientException):
			return print(error)
		if isinstance(error, MissingRequiredArgument):
			embed=discord.Embed(description=":x: You forgot to give a song title to search for.", colour=discord.Colour.red())
			embed.set_footer(text='GidBot | {}'.format(v))
			await ctx.send(embed=embed)
			c = self.client.get_channel(id=555057369931972632)
			await c.send("Play command used in **{}**=**{}** (No argument)".format(ctx.message.guild.id, ctx.message.guild.name))
		if not isinstance(error, MissingRequiredArgument or CheckFailure or BadArgument or TypeError or ClientException or CommandOnCooldown):
			errorlog = self.client.get_channel(id=744973883890991264)
			await errorlog.send("Play command used in **{}**=**{}**".format(ctx.message.guild.id, ctx.message.guild.name))
			await errorlog.send(error)
		if isinstance(error, CommandOnCooldown):
			embed=discord.Embed(title="Slow down!", description=":x: Please wait {:.1f} seconds.".format(error.retry_after), colour=discord.Colour.red())
			embed.set_footer(text='GidBot | {}'.format(v))
			await ctx.send(embed=embed) 


	@commands.command(aliases=["findsong", "searchsong", "ytsearch"])
	async def search(self, ctx, *, song):

		embed = discord.Embed(description='<a:loading:853609809936515122> Searching for songs, this may take a few seconds.', color=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		msg = await ctx.send(embed=embed)
		msg_id = msg.id
		msg = await ctx.channel.fetch_message(msg_id)

		info = await self.search_song(5, song)

		embed1 = discord.Embed(title=f"Results for '{song}':", description="*You can use there URL's to play a song.*\n", color= discord.Colour.blue())

		amount = 0
		for entry in info["entries"]:
			embed1.description += f"[{entry['title']}]({entry['webpage_url']})\n"
			amount += 1

		embed1.set_footer(text=f"Displaying the first {amount} results.")
		await msg.edit(embed=embed1)

	@search.error
	async def search_error(self, ctx, error):
		if isinstance(error, MissingRequiredArgument):
			embed=discord.Embed(description=":x: You forgot to include a song to search for.", colour=discord.Colour.red())
			embed.set_footer(text='GidBot | {}'.format(v))
			await ctx.send(embed=embed)
			c = self.client.get_channel(id=555057369931972632)
			await c.send("Search ccommand used in **{}**=**{}** (No argument)".format(ctx.message.guild.id, ctx.message.guild.name))

		if not isinstance(error, MissingRequiredArgument or CheckFailure or BadArgument):
			errorlog = self.client.get_channel(id=744973883890991264)
			await errorlog.send("Search command used in **{}**=**{}** (But unexpected error occured.)".format(ctx.message.guild.id, ctx.message.guild.name))
			await errorlog.send(error) 

	@commands.command()
	async def queue(self, ctx):
		if len(self.song_queue[ctx.guild.id]) == 0:
			embed = discord.Embed(description='There are currently no songs in the queue.', color=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
			return await ctx.send(embed=embed)		
			
		embed = discord.Embed(title=f"Song Queue", description="", color=discord.Colour.blue())

		i = 1
		for url in self.song_queue[ctx.guild.id]:
			embed.description += f"**{i}**) - {url}\n"

			i += 1

		await ctx.send(embed=embed)

	@commands.command(aliases=["s"])
	async def skip(self, ctx):
		if ctx.voice_client is None:
			embed = discord.Embed(description=':x: I am not playing any song right now.', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
			return await ctx.send(embed=embed)	

		if ctx.author.voice is None:
			embed = discord.Embed(description=':x: You are not conencted to a voice channel.', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
			return await ctx.send(embed=embed)

		if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
			embed = discord.Embed(description=':x: I am not playing any songs in your channel.', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
			return await ctx.send(embed=embed)

		poll = discord.Embed(title=f"Vote to Skip Song by: {ctx.author.name}#{ctx.author.discriminator}", description="Skip - :white_check_mark: \n Stay - :no_entry_sign:", color=discord.Colour.blue())
		poll.set_author(name=ctx.author, url="https://gidorstudios.ga", icon_url=ctx.message.author.avatar_url)
		poll.set_footer(text=f"Vote ends in 20 seconds.")

		poll_msg = await ctx.send(embed=poll)


		poll_id = poll_msg.id
		await poll_msg.add_reaction(u"\u2705")
		await poll_msg.add_reaction(u"\U0001F6AB")
		await asyncio.sleep(15)

		poll_msg = await ctx.channel.fetch_message(poll_id)

		votes = {u"\u2705": 0, u"\U0001F6AB": 0}
		reacted = []
		
		for reaction in poll_msg.reactions:
			if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
				async for user in reaction.users():
					if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
						votes[reaction.emoji] += 1

						reacted.append(user.id)

		skip = False

		if votes[u"\u2705"] > 0:
			if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.59: # 80% or higher
				skip = True
				embed = discord.Embed(title="Skip Successful", description="***Voting to skip the current song was succesful, skipping now.***", colour=discord.Colour.green())

		if not skip:
			embed = discord.Embed(title="Skip Failed", description="*Voting to skip the current song has failed.*\n\n**The vote requires at least 60% of the members to skip.**", colour=discord.Colour.red())

		embed.set_footer(text="Voting has ended.")

		await poll_msg.clear_reactions()
		await poll_msg.edit(embed=embed)

		if skip:
			#ctx.voice_client.stop()
			await self.check_queue(ctx)

	@commands.command(aliases=["fs", "fskip", "forces"])
	@commands.has_any_role('DJ', 'dj', 'Dj', 'dJ')
	async def forceskip(self, ctx):
		if ctx.voice_client is None:
			embed = discord.Embed(description=':x: I am not playing any song right now.', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
			return await ctx.send(embed=embed)	

		if ctx.author.voice is None:
			embed = discord.Embed(description=':x: You are not conencted to a voice channel.', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
			return await ctx.send(embed=embed)

		if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
			embed = discord.Embed(description=':x: I am not playing any songs in your channel.', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
			return await ctx.send(embed=embed)

		embed = discord.Embed(description="Track skipped, playing next music in queue...", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		embed.set_author(name=ctx.author, url="https://gidorstudios.ga", icon_url=ctx.message.author.avatar_url)
		await ctx.send(embed=embed)

		#ctx.voice_client.stop()
		await self.check_queue(ctx)

	@forceskip.error
	async def purge_error(self, ctx, error):
		if isinstance(error, CheckFailure):
			embed=discord.Embed(description=":x: This command can only be used if you have a **DJ** role!", colour=discord.Colour.red())
			embed.set_footer(text='GidBot | {}'.format(v)) 
			await ctx.send(embed=embed)
			
	@commands.command(aliases=["vol", "setvolume"])
	async def volume(self, ctx, vol: int = 50):
		if vol < 101 and vol > 0:
			if ctx.voice_client is None:
				embed = discord.Embed(description=':x: I am not playing any song right now.', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
				return await ctx.send(embed=embed)	

			if ctx.author.voice is None:
				embed = discord.Embed(description=':x: You are not conencted to a voice channel.', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
				return await ctx.send(embed=embed)

			if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
				embed = discord.Embed(description=':x: I am not playing any songs in your channel.', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
				return await ctx.send(embed=embed)
				
			ctx.voice_client.source.volume = float(vol/100)
			embed = discord.Embed(description=f"<a:check:677157258320150530> Set the volume to **{vol}**%", color=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(description=':x: The Maximum volume is 100, and the Minimum volume is 1', color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
			return await ctx.send(embed=embed)

	@commands.command()
	async def pause(self, ctx):
        # Checks if music is playing and pauses it, otherwise sends the player a message that nothing is playing
		try:
			ctx.voice_client.pause()
			embed = discord.Embed(description=f"<a:check:677157258320150530> Paused the music-.", colour=discord.Colour.green())
			return await ctx.send(embed = embed)
		except:
			embed = discord.Embed(description=f":x: The music is already paused or im not playing anything at the moment!", colour = discord.Colour.red())
			return await ctx.send(embed=embed)

	@commands.command(aliases=["continue"])
	async def resume(self, ctx):
        # Checks if music is paused and resumes it, otherwise sends the player a message that nothing is playing
		try:
			ctx.voice_client.resume()
			embed = discord.Embed(description=f"<a:check:677157258320150530> Resumed the music!", colour=discord.Colour.green())
			return await ctx.send(embed = embed)
		except:
			embed = discord.Embed(description=f":x: The music is not paused, or im not playing anything at the moment!", colour=discord.Colour.red())
			return await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Music(client))
