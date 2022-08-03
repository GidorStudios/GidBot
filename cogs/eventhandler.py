
import random
import hashlib
import time
import datetime
from discord.enums import AuditLogAction
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
import aiofiles

from bot import fork_version as v

class EventHandler(commands.Cog):
   
    def __init__(self, client):
        self.client = client
       


    @commands.Cog.listener()
    async def on_ready(self):
        print("eventhandler is ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("welcome.json") as wel:    
            wcmsg = json.load(wel)
        serverid = str(member.guild.id)
        if not serverid in wcmsg:
            with open("autorole.json") as l5:
                ar1 = json.load(l5)
            serverid = str(member.guild.id)
            if not serverid in ar1:
                return
            state = str(ar1[serverid]["state"])
            role = discord.utils.get(member.guild.roles, name=ar1[serverid]["role"])
            if state == "on":
                await member.add_roles(role, reason="Autorole, No Welcome System")
                return
        state = str(wcmsg[serverid]["state"])
        channel = self.client.get_channel(int(wcmsg[serverid]["channel"]))
        if state == "on":
            avatar = member.avatar_url
            embed = discord.Embed(colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Welcome!", value='**{}** Welcome to the server! :smile: Have a nice day!'.format(member))
            embed.set_footer(text='GidBot | {}'.format(v))
            embed.set_thumbnail(url=avatar)
            await channel.send(embed=embed)
        with open("autorole.json") as l: 
            ar = json.load(l)
        serverid = str(member.guild.id)
        if not serverid in ar:
            return
        state = str(ar[serverid]["state"])
        role = discord.utils.get(member.guild.roles, name=ar[serverid]["role"])
        if state == "on":
            await member.add_roles(role, reason="Autorole")





    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open("welcome.json") as f33:    
            wcmsg = json.load(f33)
        serverid = str(member.guild.id)
        if not serverid in wcmsg:
            return
        state = str(wcmsg[serverid]["state"])
        channel = self.client.get_channel(int(wcmsg[serverid]["channel"]))
        if state == "on":
            embed = discord.Embed(colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Goodbye!", value='**{}** left the server!'.format(member))
            embed.set_footer(text='GidBot | {}'.format(v))
            await channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_message_delete(self, message):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(message.guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            embed = discord.Embed(colour=discord.Colour.blue(), description="**Message Author**: {}\n**Message Content**: {}\n**Channel**: {}".format(message.author, message.content, message.channel.mention), timestamp=datetime.datetime.utcnow())
            embed.set_author(name="({}) - Message Deleted".format(message.id), icon_url=self.client.user.avatar_url)
            #embed.add_field(name="Message Author", value="{}".format(message.author.mention))
            #embed.add_field(name="Message Content", value="**{}**".format(message.conent))
            #embed.add_field(name="In Channel", value="<#{}>".format(message.channel.id)))
            embed.set_footer(text="GidBot | {}".format(v))
            if message.content == "":
                return
            await channel.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(role.guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            async for entry in role.guild.audit_logs(limit=1): 
                if entry.action == AuditLogAction.role_create:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="**Role**: {}\n**Created by**: {}".format(role.mention, entry.user.mention), timestamp=datetime.datetime.utcnow())
                    embed.set_author(name="{0.user} - Role Created".format(entry), icon_url=entry.user.avatar_url)
                    #embed.add_field(name="Role Name", value="<@{}>".format(role.id))
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="**Role**: {}".format(role.mention), timestamp=datetime.datetime.utcnow())
                    embed.set_author(name="Role Created", icon_url=self.client.user.avatar_url)
                    #embed.add_field(name="Role Name", value="<@{}>".format(role.id))
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel.send(embed=embed)  

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(role.guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            async for entry in role.guild.audit_logs(limit=1): 
                if entry.action == AuditLogAction.role_delete:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="**Role**: {}\n**Deleted by**: {}".format(role.name, entry.user.mention), timestamp=datetime.datetime.utcnow())
                    embed.set_author(name="{0.user} - Role Deleted".format(entry), icon_url=entry.user.avatar_url)
                    #embed.add_field(name="Role Name", value="<@{}>".format(role.id))
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="**Role**: {}".format(role.name), timestamp=datetime.datetime.utcnow())
                    embed.set_author(name="Role Deleted", icon_url=self.client.user.avatar_url)
                    #embed.add_field(name="Role Name", value="<@{}>".format(role.id))
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel.send(embed=embed) 
            
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(messages[0].guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            async for entry in messages[0].guild.audit_logs(limit=1):
                if entry.action == AuditLogAction.message_bulk_delete:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="**Channel**: {}\n**Messages deleted**: {}".format(messages[0].channel.mention, len(messages)), timestamp=datetime.datetime.utcnow())
                    embed.set_author(name="{} - Bulk Delete".format(entry.user), icon_url=self.client.user.avatar_url)
                    #embed.add_field(name="Messages Deleted", value="**{}**".format(len(messages)))
                    #embed.add_field(name="In:", value="#{}".format(messages[0].channel))
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            async for entry in guild.audit_logs(limit=1): 
                if entry.action == AuditLogAction.ban:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="**Member Name**: {}\n**Banned by**: {}".format(user, entry.user.mention), timestamp=datetime.datetime.utcnow())
                    #embed.add_field(name="Member Name", value="**{}**".format(user))
                    embed.set_author(name="{} - User Banned".format(entry.user), icon_url=entry.user.avatar_url)
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="**Member Name**: {}".format(user), timestamp=datetime.datetime.utcnow())
                    #embed.add_field(name="Member Name", value="**{}**".format(user))
                    embed.set_author(name="User Banned", icon_url=self.client.user.avatar_url)
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel.send(embed=embed) 
            
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            async for entry in guild.audit_logs(limit=1): 
                if entry.action == AuditLogAction.unban:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="**Member Name**: {}\n**Unbanned by**: {}".format(user, entry.user.mention),timestamp=datetime.datetime.utcnow())
                    #embed.add_field(name="Member Name", value="**{}**".format(user))
                    embed.set_author(name="{} - User Unbanned".format(entry.user), icon_url=entry.user.avatar_url)
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="**Member Name**: {}".format(user),timestamp=datetime.datetime.utcnow())
                    #embed.add_field(name="Member Name", value="**{}**".format(user))
                    embed.set_author(name="User Unbanned", icon_url=self.client.user.avatar_url)
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(before.guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            if before.content == after.content:
                return
            else:
                embed = discord.Embed(colour=discord.Colour.blue(), description="**Before**: {}\n **After**: {}\n**Channel**: {}".format(before.content, after.content, after.channel.mention), timestamp=datetime.datetime.utcnow())
                embed.set_author(name="{} - Message Edited".format(after.author), icon_url=after.author.avatar_url)
                #embed.add_field(name="Before:", value="**{}**".format(before.content))
                #embed.add_field(name="After", value="**{}**".format(after.content))
                embed.set_footer(text="GidBot | {}".format(v))
                return await channel.send(embed=embed)
            
            

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(channel.guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel1 = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            async for entry in channel.guild.audit_logs(limit=1): 
                if entry.action == AuditLogAction.channel_delete:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="**Channel Name**: {}\n**Channel Type**: {}\n**Deleted by**: {}".format(channel.name, channel.type, entry.user.mention), timestamp=datetime.datetime.utcnow())
                #embed.add_field(name="Channel Name", value="**#{}**".format(channel))
                #embed.add_field(name="Channel Type", value="**{}**".format(channel.type))
                    embed.set_author(name="{} - Channel Deleted".format(entry.user), icon_url=entry.user.avatar_url)
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel1.send(embed=embed)
                else:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="**Channel Name**: {}\n**Channel Type**: {}\n".format(channel.name, channel.type), timestamp=datetime.datetime.utcnow())
                #embed.add_field(name="Channel Name", value="**#{}**".format(channel))
                #embed.add_field(name="Channel Type", value="**{}**".format(channel.type))
                    embed.set_author(name="Channel Deleted", icon_url=self.client.user.avatar_url)
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel1.send(embed=embed)



    @commands.Cog.listener()
    async def on_guild_channel_create(self,channel):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(channel.guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel1 = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            async for entry in channel.guild.audit_logs(limit=1): 
                if entry.action == AuditLogAction.channel_create:
                    embed = discord.Embed(colour=discord.Colour.blue(),description="**Channel Name**: {}\n**Channel Type**: {}\n**Created by**: {}".format(channel.name, channel.type, entry.user.mention), timestamp=datetime.datetime.utcnow())

                    embed.set_author(name="{} - Channel Created".format(entry.user), icon_url=entry.user.avatar_url)
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel1.send(embed=embed)
                else:
                    embed = discord.Embed(colour=discord.Colour.blue(),description="**Channel Name**: {}\n**Channel Type**: {}".format(channel.name, channel.type), timestamp=datetime.datetime.utcnow())

                    embed.set_author(name="Channel Created", icon_url=self.client.user.avatar_url)
                    embed.set_footer(text="GidBot | {}".format(v))
                    await channel1.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(reaction.message.guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel1 = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            if reaction.message.content == "":
                embed = discord.Embed(colour=discord.Colour.blue(), description="**Channel**: <#{}> \n**On Message**: (Attachment) \n**Reaction**: '{}'".format(reaction.message.channel.id, reaction), timestamp=datetime.datetime.utcnow())
                embed.set_author(name="{} - Reaction Added".format(user), icon_url=user.avatar_url)
                embed.set_footer(text="GidBot | {}".format(v))
                await channel1.send(embed=embed)         
            else:
                embed = discord.Embed(colour=discord.Colour.blue(), description="**Channel**: <#{}> \n**On Message**: {} \n**Reaction**: '{}'".format(reaction.message.channel.id, reaction.message.content, reaction), timestamp=datetime.datetime.utcnow())
                embed.set_author(name="{} - Reaction Added".format(user), icon_url=user.avatar_url)
                embed.set_footer(text="GidBot | {}".format(v))
                await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(before.guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            if before.nick == after.nick:
                return
            else:
                embed = discord.Embed(colour=discord.Colour.blue(), description="**Nickname Before**: *{}* \n**Nickname After**: *{}*".format(before.nick, after.nick), timestamp=datetime.datetime.utcnow())
                embed.set_author(name="{} - Changed Nickname".format(after), icon_url=after.avatar_url)
                embed.set_footer(text="GidBot | {}".format(v))   
                await channel.send(embed=embed)  

                
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        with open("logs.json") as l:
            log = json.load(l)
        serverid = str(reaction.message.guild.id)
        if not serverid in log:
            return
        state = str(log[serverid]["state"])
        channel1 = self.client.get_channel(int(log[serverid]["channel"]))
        if state == "on":
            if reaction.message.content == "":
                embed = discord.Embed(colour=discord.Colour.blue(), description="**Channel**: {} \n**On Message**: (Attachment) \n**Reaction**: '{}'".format(reaction.message.channel.id, reaction), timestamp=datetime.datetime.utcnow())
                #embed.add_field(name="", value="Channel: {} \nOn Message: {} \n'{}'".format(reaction))
                embed.set_author(name="{} - Reaction Removed".format(user), icon_url=user.avatar_url)
                embed.set_footer(text="GidBot | {}".format(v))
                return await channel1.send(embed=embed)
            else:
                embed = discord.Embed(colour=discord.Colour.blue(), description="**Channel**: {} \n**On Message**: {} \n**Reaction**: '{}'".format(reaction.message.channel.id, reaction.message.content, reaction), timestamp=datetime.datetime.utcnow())
                #embed.add_field(name="", value="Channel: {} \nOn Message: {} \n'{}'".format(reaction))
                embed.set_author(name="{} - Reaction Removed".format(user), icon_url=user.avatar_url)
                embed.set_footer(text="GidBot | {}".format(v))
                return await channel1.send(embed=embed)
            

            
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:                                        
                em=discord.Embed(title="Thanks for inviting me!", description=f"Hello **{guild.name}** 👋,  I'm **Your bot name** forked from Gid, a multipurpse bot made by **Gidor#7092™**and **FightMan01**#????!\n\nType **g.help** to view the list of my commands! :smile:\nIf you need any help, or struggling setting up the bot, don't hesitate to join the [__`Support Server`__](https://discordapp.com/invite/YourInvite) :wink:", color=discord.Colour.blue())
                await channel.send(embed=em)
            break



def setup(client):
    client.add_cog(EventHandler(client))

