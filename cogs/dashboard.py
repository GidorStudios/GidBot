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

from discord_slash import cog_ext, SlashContext
v = "v4.3"




class Dashboard(commands.Cog):

    def __init__(self, client):
        self.client = client


    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Dashboard module loaded.")
        
    
    @commands.command(pass_context=True, aliases=["setpref", "prefix", "setp"])
    @has_permissions(administrator=True)
    async def setprefix(self, ctx, pre):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = pre
        em = discord.Embed(description=f"Set server prefix to: **{pre}**! :smile:", color=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
        em.set_author(name=ctx.author, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)


    @setprefix.error
    async def preferror(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Administrator** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
     
        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: Please specify a new prefix. Example: `!`", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
          


    @commands.command(aliases=["welc", "setwelcome"])
    @has_permissions(manage_channels=True)
    async def welcome(self, ctx, function: str, channel: discord.TextChannel = None):
        if str(function) == "on":
            em = discord.Embed(description=f"<a:check:677157258320150530> Enabled welcome messages for: {channel.mention}", colour=discord.Colour.green())
            await ctx.send(embed=em)
            with open("welcome.json") as f:
                serverid = str(ctx.message.guild.id)
                wcmsg = json.load(f)
                wcmsg[serverid] = {}
                wcmsg[serverid]["state"] = function.lower()
                wcmsg[serverid]["channel"] = channel.id
            with open("welcome.json", "w") as f1:
                json.dump(wcmsg, f1)

        if str(function) == "off":
            if not channel:
                em = discord.Embed(description="<a:check:677157258320150530> Disabled welcome messages on the server!", colour=discord.Colour.green())
                await ctx.send(embed=em)
                with open("welcome.json") as f33:
                    serverid = str(ctx.message.guild.id)
                    wcmsg = json.load(f33)
                    wcmsg[serverid] = {}
                    wcmsg[serverid]["state"] = function.lower()
                    with open("welcome.json", "w") as f2:
                        json.dump(wcmsg, f2)
            else:
                with open("welcome.json") as f33:
                    serverid = str(ctx.message.guild.id)
                    wcmsg = json.load(f33)
                    wcmsg[serverid] = {}
                    wcmsg[serverid]["state"] = function.lower()
                    wcmsg[serverid]["channel"] = channel.id
                with open("welcome.json", "w") as f2:
                    json.dump(wcmsg, f2)

    @welcome.error
    async def werror(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Manage Channels** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
            
        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: The correct usage is: g.welcome [on/off] [#channel]", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
         
        if isinstance(error, BadArgument):
            embed=discord.Embed(description=":x: I can't find a channel named like that.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)


        
    @commands.command(aliases=["log", "setlog"])
    @has_permissions(manage_channels=True)
    async def logs(self, ctx, function: str, channel: discord.TextChannel = None):
        if str(function) == "on":     
            em = discord.Embed(description=f"<a:check:677157258320150530> Enabled audit log for: {channel.mention}", colour=discord.Colour.green())
            await ctx.send(embed=em)
            with open("logs.json") as f:
                serverid = str(ctx.message.guild.id)
                wcmsg = json.load(f)
                wcmsg[serverid] = {}
                wcmsg[serverid]["state"] = function.lower()
                wcmsg[serverid]["channel"] = channel.id
            with open("logs.json", "w") as f1:
                json.dump(wcmsg, f1)  

        if str(function) == "off":  
            if not channel:
                em = discord.Embed(description="<a:check:677157258320150530> Disabled audit log on this server!", colour=discord.Colour.green())
                await ctx.send(embed=em)
                        #-----------WRITE JSON SERVER DATA---------------
                with open("logs.json") as f33:
                    serverid = str(ctx.message.guild.id)
                    wcmsg = json.load(f33)
                    wcmsg[serverid] = {}
                    wcmsg[serverid]["state"] = function.lower()
                with open("logs.json", "w") as f2:
                    json.dump(wcmsg, f2)
            else:
                with open("logs.json") as f33:
                    serverid = str(ctx.message.guild.id)
                    wcmsg = json.load(f33)
                    wcmsg[serverid] = {}
                    wcmsg[serverid]["state"] = function.lower()
                    wcmsg[serverid]["channel"] = channel.id
                with open("logs.json", "w") as f2:
                    json.dump(wcmsg, f2)

    @logs.error
    async def logs_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Manage Channels** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
            
        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: The correct usage is: g.log [on/off] [#channel]!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
         
        if isinstance(error, BadArgument):
            embed=discord.Embed(description=":x: I can't find a channel named like that.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
         
    


    @commands.command(aliases=["arole","autor", "setautor", "setautorole"])
    @has_permissions(manage_roles=True)
    async def autorole(self, ctx, function: str, role: discord.Role = None):
        if str(function) == "on":     
            em = discord.Embed(description="<a:check:677157258320150530> Enabled autorole on the server!", colour=discord.Colour.green())
            await ctx.send(embed=em)
            with open("autorole.json") as f:
                serverid = str(ctx.guild.id)
                wcmsg = json.load(f)
                wcmsg[serverid] = {}
                wcmsg[serverid]["state"] = function.lower()
                wcmsg[serverid]["role"] = role.name
            with open("autorole.json", "w") as f1:
                json.dump(wcmsg, f1)

        if str(function) == "off":  
            if not role:
                em = discord.Embed(description=f"<a:check:677157258320150530> Disabled autorole on the server!", colour=discord.Colour.green())
                await ctx.send(embed=em)
                        #-----------WRITE JSON SERVER DATA---------------
                with open("autorole.json") as f33:
                    serverid = str(ctx.guild.id)
                    wcmsg = json.load(f33)
                    wcmsg[serverid] = {}
                    wcmsg[serverid]["state"] = function.lower()
                with open("autorole.json", "w") as f2:
                    json.dump(wcmsg, f2)

    @autorole.error
    async def aroleerror(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Manage Roles** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
 
        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: The correct usage is: g.autorole [on/off] [@role] !", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
           
        if isinstance(error, BadArgument):
            embed=discord.Embed(description=":x: I can't find a role named like that.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
           

     
    @cog_ext.cog_slash(name="dashboard", description="Overview of the server features.") 
    async def _dashboard(self, ctx: SlashContext):
        state = "off"
        state1 = "off"
        state2 = "off"
        state3 = False

        serverid = str(ctx.message.guild.id)

        with open("prefixes.json", "r") as pref:
            prefixes = json.load(pref)
        with open("autorole.json") as f:
            atrl = json.load(f)
        with open("welcome.json") as wel:    
            wcmsg = json.load(wel)
        with open("logs.json") as log:    
            l = json.load(log)
        with open("szinek.json") as rain:
            rb = json.load(rain)

        if str(ctx.message.guild.id) not in prefixes:
            pref = "g."
        else:
            prefix = prefixes[str(ctx.message.guild.id)]
            pref = prefix

        if serverid in wcmsg:
            state = str(wcmsg[serverid]["state"])
            if state == "on":
                c = self.client.get_channel(int(wcmsg[serverid]["channel"]))
                welcomesystem = "ON"
                channel = "{}".format(c.id)
            else:
                welcomesystem = "OFF"
                channel = ""
        else:
            welcomesystem = "OFF"
            channel = ""

        if serverid in atrl:
            state1 = str(atrl[serverid]["state"])
            if state1 == "on":
                ar = discord.utils.get(ctx.message.guild.roles, name=atrl[serverid]["role"])
                arolesystem = "ON"
                arole = "{}".format(ar.id)
            else:
                arolesystem = "OFF"
                arole = ""
        
        else:
            arolesystem = "OFF"
            arole = ""
        

        if serverid in l:
            state2 = str(l[serverid]["state"])
            if state2 == "on":
                logc = self.client.get_channel(int(l[serverid]["channel"]))
                logsystem = "ON"
                logchannel = "{}".format(logc.id)
            else:
                logsystem = "OFF"
                logchannel = ""
        else:
            logsystem = "OFF"
            logchannel = ""

        if serverid in rb:
            state3 = bool(rb[serverid]["fuss"])
            if state3 == True:
                roleid = int(rb[serverid]["id"])
                rsystem = "ON"
                rrole = "{}".format(roleid)
            else:
                rsystem = "OFF"
                rrole = ""
        else:
            rsystem = "OFF"
            rrole = ""
        if str(ctx.message.guild.id) in prefixes:
            embed = discord.Embed(title="Server Dashboard", description=f"Prefix on the server: **{pref}**", colour=discord.Colour.blue())
        else:
            embed = discord.Embed(title="Server Dashboard", description=f"Prefix on the server: **{pref}**", colour=discord.Colour.blue())
        if serverid in wcmsg:
            if state == "on":
                embed.add_field(name="Welcome System", value="Status: {} \n\n<#{}>".format(welcomesystem, channel), inline=False)
            else:
                embed.add_field(name="Welcome System", value="Status: {}".format(welcomesystem), inline=False)
        else:
            embed.add_field(name="Welcome System", value="Status: {}".format(welcomesystem), inline=False)
        if serverid in l:
            if state1 == "on":
                embed.add_field(name="Log System", value="Status: {} \n\n<#{}>".format(logsystem, logchannel), inline=False)
            else:
                embed.add_field(name="Log System", value="Status: {}".format(logsystem), inline=False)
        else:
            embed.add_field(name="Log System", value="Status: {}".format(logsystem), inline=False)
        if serverid in atrl:
            if state2 == "on":
                embed.add_field(name="Autorole System", value="Status: {} \n\n<@&{}>".format(arolesystem, arole), inline=False)
            else:
                embed.add_field(name="Autorole System", value="Status: {}".format(arolesystem), inline=False)
        else:
            embed.add_field(name="Autorole System", value="Status: {}".format(arolesystem), inline=False)
        if serverid in rb:
            if state3 == True:
                embed.add_field(name="Rainbow System", value="Status: {} \n\n<@&{}>".format(rsystem, rrole), inline=False)
            else:
                embed.add_field(name="Rainbow System", value="Status: {}".format(rsystem), inline=False)
        else:
            embed.add_field(name="Rainbow System", value="Status: {}".format(rsystem), inline=False)

        await ctx.send(embed=embed)	
    @commands.command(aliases=["db","dashb","dboard"])
    async def dashboard(self, ctx):

        state = "off"
        state1 = "off"
        state2 = "off"
        state3 = False

        serverid = str(ctx.message.guild.id)

        with open("prefixes.json", "r") as pref:
            prefixes = json.load(pref)
        with open("autorole.json") as f:
            atrl = json.load(f)
        with open("welcome.json") as wel:    
            wcmsg = json.load(wel)
        with open("logs.json") as log:    
            l = json.load(log)
        with open("szinek.json") as rain:
            rb = json.load(rain)

        if str(ctx.message.guild.id) not in prefixes:
            pref = "g."
        else:
            prefix = prefixes[str(ctx.message.guild.id)]
            pref = prefix

        if serverid in wcmsg:
            state = str(wcmsg[serverid]["state"])
            if state == "on":
                c = self.client.get_channel(int(wcmsg[serverid]["channel"]))
                welcomesystem = "ON"
                channel = "{}".format(c.id)
            else:
                welcomesystem = "OFF"
                channel = ""
        else:
            welcomesystem = "OFF"
            channel = ""

        if serverid in atrl:
            state1 = str(atrl[serverid]["state"])
            if state1 == "on":
                ar = discord.utils.get(ctx.message.guild.roles, name=atrl[serverid]["role"])
                arolesystem = "ON"
                arole = "{}".format(ar.id)
            else:
                arolesystem = "OFF"
                arole = ""
        
        else:
            arolesystem = "OFF"
            arole = ""
        

        if serverid in l:
            state2 = str(l[serverid]["state"])
            if state2 == "on":
                logc = self.client.get_channel(int(l[serverid]["channel"]))
                logsystem = "ON"
                logchannel = "{}".format(logc.id)
            else:
                logsystem = "OFF"
                logchannel = ""
        else:
            logsystem = "OFF"
            logchannel = ""

        if serverid in rb:
            state3 = bool(rb[serverid]["fuss"])
            if state3 == True:
                roleid = int(rb[serverid]["id"])
                rsystem = "ON"
                rrole = "{}".format(roleid)
            else:
                rsystem = "OFF"
                rrole = ""
        else:
            rsystem = "OFF"
            rrole = ""
        if str(ctx.message.guild.id) in prefixes:
            embed = discord.Embed(title="Server Dashboard", description=f"Prefix on the server: **{pref}**", colour=discord.Colour.blue())
        else:
            embed = discord.Embed(title="Server Dashboard", description=f"Prefix on the server: **{pref}**", colour=discord.Colour.blue())
        if serverid in wcmsg:
            if state == "on":
                embed.add_field(name="Welcome System", value="Status: {} \n\n<#{}>".format(welcomesystem, channel), inline=False)
            else:
                embed.add_field(name="Welcome System", value="Status: {}".format(welcomesystem), inline=False)
        else:
            embed.add_field(name="Welcome System", value="Status: {}".format(welcomesystem), inline=False)
        if serverid in l:
            if state1 == "on":
                embed.add_field(name="Log System", value="Status: {} \n\n<#{}>".format(logsystem, logchannel), inline=False)
            else:
                embed.add_field(name="Log System", value="Status: {}".format(logsystem), inline=False)
        else:
            embed.add_field(name="Log System", value="Status: {}".format(logsystem), inline=False)
        if serverid in atrl:
            if state2 == "on":
                embed.add_field(name="Autorole System", value="Status: {} \n\n<@&{}>".format(arolesystem, arole), inline=False)
            else:
                embed.add_field(name="Autorole System", value="Status: {}".format(arolesystem), inline=False)
        else:
            embed.add_field(name="Autorole System", value="Status: {}".format(arolesystem), inline=False)
        if serverid in rb:
            if state3 == True:
                embed.add_field(name="Rainbow System", value="Status: {} \n\n<@&{}>".format(rsystem, rrole), inline=False)
            else:
                embed.add_field(name="Rainbow System", value="Status: {}".format(rsystem), inline=False)
        else:
            embed.add_field(name="Rainbow System", value="Status: {}".format(rsystem), inline=False)

        await ctx.send(embed=embed)	





def setup(client):
    client.add_cog(Dashboard(client))