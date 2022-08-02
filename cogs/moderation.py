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
from discord.ext.commands import has_permissions, has_guild_permissions, CheckFailure, MissingRequiredArgument, BadArgument, CommandOnCooldown
from datetime import timedelta


v = "v4.3"

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation module loaded.")


    @commands.command(pass_context = True)
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=0):
        
        

        if not ctx.message.guild == None:
            channel = ctx.message.channel
            messages = []
            async for message in channel.history(limit=int(amount) + 1):
                messages.append(message)
            await ctx.message.channel.delete_messages(messages)
            em = discord.Embed(title="Purged!", description="<a:check:677157258320150530> I Succesfully deleted **{}** messages. :hugging:".format(int(amount)), colour=discord.Colour.green())
            await ctx.send(embed=em)
        else:
            await ctx.send("❌ You cant use this command in private messages!")


    @commands.command(pass_context = True)
    @has_guild_permissions(mute_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason):
        try:
            role = discord.utils.get(member.guild.roles, name='Muted')
        except:
            embed = discord.Embed(title='Error!', description='Please create a role named `Muted` without `sending_messages` permission!', colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
            return
            
        await member.add_roles(role, reason="Gid Bot Moderation. Mutes")
        embed=discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name='User Muted!', value="User <@{}> was muted by <@{}> for **{}**.".format(member.id, ctx.message.author.id, reason), inline=True)
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)
        try:
            user = self.client.get_user(member.id)
            embed1 = discord.Embed(
                colour = discord.Colour.red()
            )
            embed1.add_field(name="Mute Notification", value='You have been Muted in **{}** for: **{}** by **{}**! :disappointed_relieved:'.format(ctx.message.guild.name, reason, ctx.message.author))
            embed1.set_footer(text='GidBot | {}'.format(v))
            await user.send(embed=embed1)


    @commands.command(aliases=['hban'])
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, usid:int):
        await ctx.guild.ban(discord.Object(id=usid))   
        embed = discord.Embed( description=f"<a:check:677157258320150530> User with ID: **{usid}** has been banned by: {ctx.message.author.mention}", color=discord.Color.blue())
        await ctx.send(embed=embed)
        
        
        
        

    @commands.command(aliases=['uban'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, usid:int):
        await ctx.guild.unban(discord.Object(id=usid))   
        embed = discord.Embed( description=f"<a:check:677157258320150530> User with ID: **{usid}** has been unbanned by: {ctx.message.author.mention}", color=discord.Color.blue())
        await ctx.send(embed=embed)
        
        
    @hackban.error
    async def hackban_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Ban Members** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: Please Specify the ID of the user you want to ban.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, BadArgument):
            embed=discord.Embed(description=":x: I can't find an User with an ID like that.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)



    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Ban Members** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: Please Specify the ID of the user you want to unban.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, BadArgument):
            embed=discord.Embed(description=":x: I can't find an User with an ID like that.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

    @commands.command(pass_context = True)
    @has_guild_permissions(mute_members=True)
    async def tempmute(self, ctx, time: int, member: discord.Member, *, reason):
        try:
            role = discord.utils.get(member.guild.roles, name='Muted')
        except:
            embed = discord.Embed(title='Error!', description='Please create a role named `Muted` without `sending_messages` permission!', colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
            return
            
        await member.add_roles(role, reason="Gid Bot Moderation. Tempmute")
        embed=discord.Embed( colour=discord.Colour.blue())
        embed.add_field(name='User Muted!', value="User <@{}> was muted by <@{}> for **{}** minute. Reason: **{}**".format(member.id, ctx.message.author.id, time, reason), inline=True)
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)
        try:
            user = self.client.get_user(member.id)
            embed1 = discord.Embed(
                colour = discord.Colour.red()
            )
            embed1.add_field(name="Mute Notification", value='You have been Temporarily Muted in **{}** for **{} minute** with reason **{}** by **{}**! :disappointed_relieved:'.format(ctx.message.guild.name, time, reason, ctx.message.author))
            embed1.set_footer(text='GidBot | {}'.format(v))
            await user.send(embed=embed1)

        await asyncio.sleep(time*60)
        await member.remove_roles(role, reason="Gid Bot Moderation. Auto Unmute from tempmute.")
        try:
            user = self.client.get_user(member.id)
            embed1 = discord.Embed(
                colour = discord.Colour.red()
            )
            embed1.add_field(name="Unmute Notification", value='You have been Unmuted in **{}**! :hugging:'.format(ctx.message.guild.name))
            embed1.set_footer(text='GidBot | {}'.format(v))
            await user.send(embed=embed1)
        except:
            return


    @tempmute.error
    async def tempmute_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Mute Members** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: Correct command usage is: g.tempmute [time in minutes] [user] [reason]!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, BadArgument):
            embed=discord.Embed(description=":x: I can't find a member named like that.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

    @commands.command(pass_context = True)
    @has_guild_permissions(mute_members=True)
    async def unmute(self, ctx, member: discord.Member):
        try:
            role = discord.utils.get(member.guild.roles, name='Muted')
        except:
            embed = discord.Embed(title='Error!', description='Please create a role named `Muted`!', colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
            return
        await member.remove_roles(role, reason="Gid Bot Moderation")
        
        embed=discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name='User Unmuted', value="User <@{}> was unmuted by <@{}> ".format(member.id, ctx.message.author.id), inline=True)
        embed.set_footer(text="GidBot | {}".format(v))
        await c.send("Mute command used in **{}**=**{}**".format(ctx.message.guild.id, ctx.message.guild.name))
        try:
            user = self.client.get_user(member.id)
            embed1 = discord.Embed(
                colour = discord.Colour.red()
            )
            embed1.add_field(name="Unmute Notification", value='You have been Unmuted in **{}** by **{}**! :hugging:'.format(ctx.message.guild.name, ctx.message.author))
            embed1.set_footer(text='GidBot | {}'.format(v))
            await user.send(embed=embed1)
        except:


    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Mute Members** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)


        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: Please Specify a member!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, BadArgument):
            embed=discord.Embed(description=":x: I can't find a member named like that.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)



    @commands.command(pass_context = True)
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason):
        
        try: 
            await member.ban(reason=reason)
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.add_field(name="Banned!", value='<a:check:677157258320150530> **{}** Was Banned by: <@{}> for: **{}**!<:DPESgun:478896794965770242>'.format(member.name, ctx.message.author.id, reason))
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
            await c.send("Ban command used in **{}**=**{}**".format(ctx.message.guild.id, ctx.message.guild.name))
            try:
                user = self.client.get_user(member.id)
                embed1 = discord.Embed(
                    colour = discord.Colour.red()
                )
                embed1.add_field(name="Ban Notification", value='You have been Banned from **{}** with the reason: **{}** by **{}**! <:DPESgun:478896794965770242>'.format(ctx.message.guild.name, reason, ctx.message.author))
                embed1.set_footer(text='GidBot | {}'.format(v))
                await user.send(embed=embed1)
            except:
                 await c.send("Ban command used in **{}**=**{}** (Banned but can't dm user.".format(ctx.message.guild.id, ctx.message.guild.name))	


        except:
            embed=discord.Embed(description=":x:  I can't ban users, they have higher roles than me.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Ban Members** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: Please Specify the user and the reason!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, BadArgument):
            embed=discord.Embed(description=":x: I can't find a member named like that.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)



    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason):
        
        try: 
            await member.kick(reason=reason)
            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.add_field(name="Kicked!", value='<a:check:677157258320150530> **{}** Was kicked by: <@{}> for: **{}**! <:DPESgun:478896794965770242>'.format(member.name, ctx.message.author.id, reason))
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
            await c.send("Kick command used in **{}**=**{}**".format(ctx.message.guild.id, ctx.message.guild.name))	
            try:
                user = self.client.get_user(member.id)
                embed1 = discord.Embed(
                    colour = discord.Colour.red()
                )
                embed1.add_field(name="Kick Notification", value='You have been Kicked from **{}** with the reason: **{}** by **{}**! <:DPESgun:478896794965770242>'.format(ctx.message.guild.name, reason, ctx.message.author))
                embed1.set_footer(text='GidBot | {}'.format(v))
                await user.send(embed=embed1)
    

        except:
            embed=discord.Embed(description=":x: I can't kick users, they have higher roles than me.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Kick Members** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: Please Specify the user and the reason!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, BadArgument):
            embed=discord.Embed(description=":x: I can't find a member named like that.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

            
    @commands.command()
    @has_permissions(administrator=True)
    async def poll(self, ctx, time: int, *, polldata): 
        await ctx.message.delete()
        options = {"✅": "Yes", ":x:": "No","🤷": "I don't know."} 
        vote = discord.Embed(title="Poll", description="{}".format(polldata), color=discord.Colour.blue(), timestamp=datetime.datetime.utcnow()) 
        value = "\n".join("- {} {}".format(*item) for item in options.items()) 
        vote.add_field(name="Vote now!", value=value, inline=True) 
        vote.set_footer(text="Time to vote: {} Minute.".format(time)) 
        message_1 = await ctx.send(embed=vote) # ❌✔️
        await message_1.add_reaction(emoji="✅") 
        await message_1.add_reaction(emoji="❌") 
        await message_1.add_reaction(emoji="🤷") 
        
        
        await asyncio.sleep(time*60)
        await ctx.send("<a:check:677157258320150530> Poll has ended!")

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed=discord.Embed(description=":x: You need **Administrator** permission to use this command!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: Please Specify the **time in seconds** and the **poll details**!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

        if isinstance(error, BadArgument):
            embed=discord.Embed(description=":x: The time you specified is not a number!.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

            

            

def setup(client):
    client.add_cog(Moderation(client))