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
from discord.ext.commands import has_permissions, CheckFailure, MissingRequiredArgument, BadArgument, CommandOnCooldown


regionals = {'a': '\N{REGIONAL INDICATOR SYMBOL LETTER A}', 'b': '\N{REGIONAL INDICATOR SYMBOL LETTER B}',
                        'c': '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
                        'd': '\N{REGIONAL INDICATOR SYMBOL LETTER D}', 'e': '\N{REGIONAL INDICATOR SYMBOL LETTER E}',
                        'f': '\N{REGIONAL INDICATOR SYMBOL LETTER F}',
						'é': '\N{REGIONAL INDICATOR SYMBOL LETTER E}',
						'á': '\N{REGIONAL INDICATOR SYMBOL LETTER A}',
                        'g': '\N{REGIONAL INDICATOR SYMBOL LETTER G}', 'h': '\N{REGIONAL INDICATOR SYMBOL LETTER H}',
                        'i': '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
						'í': '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
                        'j': '\N{REGIONAL INDICATOR SYMBOL LETTER J}', 'k': '\N{REGIONAL INDICATOR SYMBOL LETTER K}',
                        'l': '\N{REGIONAL INDICATOR SYMBOL LETTER L}',
                        'm': '\N{REGIONAL INDICATOR SYMBOL LETTER M}', 'n': '\N{REGIONAL INDICATOR SYMBOL LETTER N}',
                        'o': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
						'ó': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
						'ő': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
						'ö': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
                        'p': '\N{REGIONAL INDICATOR SYMBOL LETTER P}', 'q': '\N{REGIONAL INDICATOR SYMBOL LETTER Q}',
                        'r': '\N{REGIONAL INDICATOR SYMBOL LETTER R}',
                        's': '\N{REGIONAL INDICATOR SYMBOL LETTER S}', 't': '\N{REGIONAL INDICATOR SYMBOL LETTER T}',
                        'u': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
						'ű': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
						'ü': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
						'ú': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
                        'v': '\N{REGIONAL INDICATOR SYMBOL LETTER V}', 'w': '\N{REGIONAL INDICATOR SYMBOL LETTER W}',
                        'x': '\N{REGIONAL INDICATOR SYMBOL LETTER X}',
                        'y': '\N{REGIONAL INDICATOR SYMBOL LETTER Y}', 'z': '\N{REGIONAL INDICATOR SYMBOL LETTER Z}',
                        '0': '0⃣', '1': '1⃣', '2': '2⃣', '3': '3⃣',
                        '4': '4⃣', '5': '5⃣', '6': '6⃣', '7': '7⃣', '8': '8⃣', '9': '9⃣', '!': '\u2757',
                        '?': '\u2753'}



from bot import fork_version as v

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun Module Loaded")

    @commands.command()
    async def regional(self, ctx, *, msg):
        if ctx.message.author.guild_permissions.manage_messages or ctx.message.author.id == 338748699129937930:
            try:
                await ctx.message.delete()
                msg = list(msg)
                regional_list = [regionals[x.lower()] if x.isalnum() or x in ["!", "?"] else x for x in msg]
                regional_output = '\u200b'.join(regional_list)
                await ctx.send(regional_output)
            except:
                msg = list(msg)
                regional_list = [regionals[x.lower()] if x.isalnum() or x in ["!", "?"] else x for x in msg]
                regional_output = '\u200b'.join(regional_list)
                await ctx.send(regional_output)
        else:          
            embed = discord.Embed(title='Error!', description=':x: You need Manage Messages permission to use this!', colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)	




    @commands.command()
    async def gay(self, ctx, user: discord.Member = None):
        if user == None:
            gayrate1 = random.randint(0, 101)
            gayembed1 = discord.Embed(
                colour = discord.Colour.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            gayembed1.add_field(name="Gae Rate", value='{} You are **{}%** gay!'.format(ctx.message.author.mention, gayrate1), inline=False)
            await ctx.send(embed=gayembed1)
        else:
            gayrate = random.randint(0, 101)
            gayembed = discord.Embed(
                colour = discord.Colour.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            gayembed.add_field(name="Gae Rate", value='{} is **{}%** gay!'.format(user.mention, gayrate), inline=False)
            await ctx.send(embed=gayembed)
            


    #-----------------------Fun------------------------
    @commands.command()
    async def avatar(self, ctx, member: discord.Member):
            u = member.avatar_url
            embed = discord.Embed(description="<@{}>'s avatar..".format(member.id), colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
            embed.set_image(url=u)
            await ctx.send(embed=embed)


    @avatar.error
    async def avatar_error(self, ctx, error):
        embed = discord.Embed(title='Error!', description=':x: Please specify a user!', colour=discord.Colour.red())
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)	
        
    @commands.command()
    async def cat(self, ctx):
        response = rq.get('https://aws.random.cat/meow')
        data = response.json()
        
        embed = discord.Embed(	
            colour=discord.Colour.blue()
        )
        embed.add_field(name="Cat", value='Look at that, Awww.', inline=False)
        embed.set_image(url=data['file'])
        await ctx.send(embed=embed)


        
    @commands.command()
    async def dog(self, ctx):
        r = rq.get("https://random.dog/woof")
        r = str(r.content)
        r = r.replace("b'","")
        r = r.replace("'","")
        embed = discord.Embed(	
        colour=discord.Colour.blue()
        )
        embed.add_field(name="Dog", value='So Cute....', inline=False)
        embed.set_image(url="https://random.dog/" + r)
        await ctx.send(embed=embed)


        
    @commands.command()
    @has_permissions(manage_messages=True)
    async def esay(self, ctx, *, args):
        try:
            await ctx.message.delete()
            esay = discord.Embed(
            description="{}".format(args),
            colour=discord.Colour.blue(),
            timestamp=datetime.datetime.utcnow()
            )
            return await ctx.send(embed=esay)
        except:
            esay = discord.Embed(
            description="{}".format(args),
            colour=discord.Colour.blue(),
            timestamp=datetime.datetime.utcnow()
            )
            return await ctx.send(embed=esay)

    @esay.error
    async def esay_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Manage Messages** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description=":x: Please specify something to say!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
    
    @commands.command()
    @has_permissions(manage_messages=True)
    async def say(self, ctx, *, args):
        try:
            await ctx.message.delete()
            return await ctx.send(args)
        except:
            return await ctx.send(args)

    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Manage Messages** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        else:
            embed=discord.Embed(description=":x: Please specify something to say!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)   

    @commands.command(aliases=["8ball"])
    async def magicball(self, ctx, *, question):
        embed = discord.Embed(
            colour = discord.Colour.blue(),
            timestamp=datetime.datetime.utcnow()
            )
            
        embed.add_field(name=':8ball:', value='**Question: **' + question + ' **Answer:**' + random.choice([" It is certain",
            " Without a doubt",
            " Yes, definitely",
            " Do you know da wae?",
            " You may rely on it",
            " As I see it, yes",
            " Most likely.",
            " Yes.",
            " Signs point to yes",
            " Ask again later",
            " No god please no.",
            " Cannot predict now",
            " Concentrate and ask again",
            " Don't count on it",
            " My reply is no",
            " No U.",
            ' My sources say no']))
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)
        c = self.client.get_channel(id=555057369931972632)
        await c.send("Magicball command used in **{}**=**{}**".format(ctx.message.guild.id, ctx.message.guild.name))

    @magicball.error
    async def merror(self, ctx, error):
        embed = discord.Embed(title='Error!', description=':x: Please ask a question! :smile:', colour=discord.Colour.red())
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)	
        
    @commands.command()
    async def dice(self, ctx, * number):
        embed = discord.Embed(
        colour = discord.Colour.blue()
        )
        number = random.randint(1, 6)
        embed.add_field(name='Dice', value='<a:check:677157258320150530> You rolled the dice and you rolled: ' + '**{}**'.format(number))
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)
        
    @commands.command()
    async def randnumber(self, ctx, * number):
        embed = discord.Embed(
        colour = discord.Colour.blue()
        )
        number = random.randint(1, 99999)
        embed.add_field(name='Random Number', value='<a:check:677157258320150530> Your Random Number is: ' + '**{}**'.format(number), inline=False)
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)
    
        
    @commands.command(pass_context=True)
    async def gennumber(self, ctx, one: int, two: int):
        embed = discord.Embed(
        colour = discord.Colour.blue()
        )
        number = random.randint(one, two)
        embed.add_field(name='Number Generator', value='<a:check:677157258320150530> Your Random Generated Number is: ' + '**{}**'.format(number), inline=True)		
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)
        
    @gennumber.error
    async def gennumber_error(self, ctx, error):
        embed = discord.Embed(title='Error!', description=':x: Please specify the **Minimum** and **Maximum** values.', colour=discord.Colour.red())
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)	
        
    @commands.command(pass_context=True)
    async def coinflip(self, ctx):
        embed = discord.Embed(
        colour = discord.Colour.blue()
        )
        embed.add_field(name='Coinflip', value='Result: ' + random.choice(["**Head**",
            "**Tails**"]))
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)
        
    @commands.command(pass_context=True)
    async def slap(self, ctx, user: discord.Member):
        c = self.client.get_channel(id=555057369931972632)
        await c.send("Slap command used in **{}**=**{}**".format(ctx.message.guild.id, ctx.message.guild.name))

        embed = discord.Embed(
        colour = discord.Colour.blue()
        )
        embed.add_field(name='Slap',  value=':punch: <@{}> Was slapped by **<@{}>**! K.O'.format(ctx.message.author.id, user.id), inline=False)
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)
    
    @slap.error
    async def slerror(self, ctx, error):
        embed = discord.Embed(title='Error!', description=':x: Please specify an user to slap.', colour=discord.Colour.red())
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)	

    @commands.command(pass_context=True)
    async def poke(self, ctx, user: discord.Member):
        c = self.client.get_channel(id=555057369931972632)
        await c.send("Poke command used in **{}**=**{}**".format(ctx.message.guild.id, ctx.message.guild.name))

        embed = discord.Embed(
        colour = discord.Colour.blue()
        )
        embed.add_field(name='Poke',  value='**<@{}>** has been poked by: <@{}>!'.format(user.id, ctx.message.author.id), inline=False)
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)

    @poke.error
    async def pokeerror(self, ctx, error):
        embed = discord.Embed(title='Error!', description=':x: Please specify an user to poke.', colour=discord.Colour.red())
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)	
    

    @commands.command(pass_context = True)
    async def suicide(self, ctx):
            embed = discord.Embed(description='**<@{}>** took his own life.'.format(ctx.message.author.id), colour=discord.Colour.blue())
            embed.set_image(url="https://cdn.discordapp.com/attachments/552199641077121035/559348488324907027/suicide.gif")
            await asyncio.sleep(1)
            await ctx.send(embed=embed)


    @commands.command()		
    async def spinner(self, ctx, skip):
        number = random.randint(15, 145)
        if skip == "speed":       
            await ctx.send(f'<:fidgetspinner:541938644169261056> <@{ctx.message.author.id}> Your fidget spinner is spinning...<:fidgetspinner:541938644169261056>')
            await asyncio.sleep(int(number))
            await ctx.send(f'<:fidgetspinner:541938644169261056> <@{ctx.message.author.id}> Your fidget spinner was spinning for {number} seconds. <:fidgetspinner:541938644169261056>')
        if skip == "skip":
            await ctx.send(f'<:fidgetspinner:541938644169261056> <@{ctx.message.author.id}> Your fidget spinner was spinning for {number} seconds. <:fidgetspinner:541938644169261056>')

    @spinner.error
    async def spinner_no_skip(self, error, ctx):
        number = random.randint(7, 145)  
        await error.send(f'<:fidgetspinner:541938644169261056> <@{error.message.author.id}> Your fidget spinner is spinning...<:fidgetspinner:541938644169261056>')
        await asyncio.sleep(int(number))
        await error.send(f'<:fidgetspinner:541938644169261056> <@{error.message.author.id}> Your fidget spinner was spinning for {number} seconds. <:fidgetspinner:541938644169261056>')
        


def setup(client):
    client.add_cog(Fun(client))

