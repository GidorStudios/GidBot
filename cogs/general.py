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
from contextlib import redirect_stdout
import requests as rq
from asyncio.subprocess import PIPE
from io import BytesIO
from PIL import Image, ImageChops 
from discord.ext.commands import has_permissions, CheckFailure, MissingRequiredArgument, BadArgument, CommandOnCooldown

start_time = time.time()

from bot import v
from bot import fork_version
from bot import fork_owner_id


page1 = discord.Embed(title="Normal", description="**g.ping** | Pong\n**g.userinfo @user** | Information about the user\n**g.news** | Shows the information about the latest update\n**g.botinfo** | Information about the bot.\n**g.invite** | Bot invite, Support server and website.\n**g.uptime** | Current bot uptime.\n**g.serverinfo** | Information about the current server.\n **g.upvote** | Upvote the bot on discordbots.org to get it to more people.\n**g.channelinfo** | Information about the current channel.", color=discord.Colour.blue())
page2 = discord.Embed(title="Fun", description="󠀠**g.say [text]** | Says the provided text.\n**g.snipe** | Snipes a deleted message. \n **g.esay [text]** | Says the provided text in a box.\n**g.dice** | Rolls a dice. \n**g.8ball [Question]** | Answers to your question.\n**g.randnumber** | Generataes a random number bettwenn 1-99999\n**g.gennumber [min] [max]** | Generates a number bettwen the provided numbers\n**g.coinflip** | Head or Tails?\n**g.slap [@user]** | :punch: \n**g.spinner** | Spins the fidget spinner.\n**g.avatar [@user]** | Shows a user avatar.\n**g.cat** | Shows a random cat image.\n**g.dog** | Shows a random dog image.\n**g.suicide** | Rest in Peace\n**g.poke [@user]** | Pokes the provided user.\n**g.gay [@user]** | Shows the percentage of someones GaeRate\n**g.regional [text]** | Converts text to regional indicator emojies.", color=discord.Colour.blue())
page3 = discord.Embed(title="Music", description="󠀠**g.play** | Adds songs to the queue. \n**g.queue** | Shows the current queue. \n**g.volume [1-100]** | Sets the Music player volume. \n**g.join** | The bot joins to your voice channel.  \n**g.forceskip** | Skips a song without vote. \n**g.search** | Searches for music. \n**g.stop** | Stops the music player.\n**g.skip** | Votes to skip the song.\n**g.pause** | Pauses the current music. \n**g.resume** | Resumes the paused music.", color=discord.Colour.blue())
page4 = discord.Embed(title="Economy", description="󠀠**g.fish** | Catches some fish. \n**g.work** | Goes to work and earns money.\n**g.deposit <value>** | Deposits your money to your bank profile, it can't be robbed.\n**g.withdraw <value>** | Withdraws your money from your bank profile.\n**g.balance** | Shows your wallet balance & bank balance.\n**g.pay @user <value>** | Sends money from your wallet to an other person.\n**g.rob @user** | Robs from an user.\n**g.shop** | Shows the shop items and prices.\n**g.buy [item name]** | Buys an item.\n**g.crime** | Do some illegal work, and get some money.\n**g.bag** | Shows your inventory.", color=discord.Colour.blue())
page5 = discord.Embed(title="Moderation", description="󠀠**g.purge [Number]** | Deletes messages from the channel.\n**g.ban [@user]** | Bans users from the server.\n**g.kick [@user]** | Kicks users from the server.\n**g.mute [user] [reason]** | Mutes the user, so he can't write messages on the server.\n**g.tempmute [time in minutes] [user] [reason]** | Temporarily mutes an user. \n**g.unmute [user]** | Unmutes the user. \n **g.warn [user] [reason]** | Warns the user about something.", color=discord.Colour.blue())
page6 = discord.Embed(title="Utility", description="**g.giveaway [Minutes] [Stuff]** | Sets up a giveaway. \n**g.setticket [Message ID] [Category ID]** |󠀠 Sets up the support Ticket system. \n**g.dashboard** | Overview of the bot features in the current server.\n**g.welcome [on/off] [channel]** | Enables or disables the welcome system.\n**g.log [on/off] [channel]** | Enables the log feature on the server.\n**g.rainbow [on/off] [role]** | Enables the rainbowrole feature on the server.\n**g.autorole [on/off] [role]** | Enables the autorole feature on the server. \n**g.poll [time in mintues] [poll]** | Creates a poll. \n **g.reactionrole [Role] [Message ID] [Emoji]** | Sets up a reaction role based on a message, and the provided emoji.", color=discord.Colour.blue())



class General(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.client.help_pages = [page1, page2, page3, page4, page5, page6]

    @commands.Cog.listener()
    async def on_ready(self):
        print("General module loaded.")

    @commands.command(pass_context = True)		
    async def uptime(self, ctx):
            current_time = time.time()
            difference = int(round(current_time - start_time))
            text = str(datetime.timedelta(seconds=difference)) 
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.add_field(name="Uptime", value='Current Bot Uptime: **{}**'.format(text))
            embed.set_footer(text='GidBot | {}'.format(v))
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException:
                await ctx.send("Current uptime: " + text)

    @commands.command(pass_context = True, aliases=["social", "upvote", "website", "supportserver", "sus", "serverinvite"])
    async def invite(self, ctx):
        inve = discord.Embed(colour=discord.Colour.blue())
        inve.add_field(name='Social Links:', value='󠀠\n**Bot Invite:**  \n**Upvote the Bot:**\n**Original Server: **https://discordapp.com/invite/Fjm8wfd', inline=False)
        inve.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=inve)

    # @commands.command(pass_context = True)
    # async def auditlog(self, ctx):    
    #     async for entry in ctx.message.guild.audit_logs(limit=1): 
    #         await ctx.send('{0.user} did {0.action} to {0.target}'.format(entry))

    @commands.command()
    async def help(self, ctx):
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
        current = 0
        msg = await ctx.send(embed=self.client.help_pages[current])
    
        for button in buttons:
           await msg.add_reaction(button)
        
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                return print(f"Help command timed out for {ctx.author}")

            else:
                previous_page = current
                if reaction.emoji == u"\u23EA":
                    current = 0
                
                elif reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1
                       
                elif reaction.emoji == u"\u27A1":
                    if current < len(self.client.help_pages)-1:
                        current += 1
    
                elif reaction.emoji == u"\u23E9":
                    current = len(self.client.help_pages)-1
        
                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(embed=self.client.help_pages[current])
        



    @commands.command()	
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            timestamp=datetime.datetime.utcnow()
            
        )
        s = ctx.message.guild
        img = ctx.message.guild.icon_url
        embed.set_thumbnail(url=img)
        embed.add_field(name='Server Information', value=f"\n**Server Name:** {ctx.message.guild.name}\n**Server Owner:** <@{ctx.message.guild.owner_id}>\n**Server ID:** {ctx.message.guild.id}\n**Afk Channel:** {ctx.message.guild.afk_channel}\n**Afk Timeout** {ctx.message.guild.afk_timeout} seconds.\n**Filesize Limit:** {round(ctx.message.guild.filesize_limit/1000000)} mb\n**Emoji Limit:** {ctx.message.guild.emoji_limit}\n**Max Audio Quality:** {round(ctx.message.guild.bitrate_limit/1000)} bit.\n**Animated Icon:** {ctx.message.guild.is_icon_animated()}\n**Boost Tier:** {ctx.message.guild.premium_tier}\n**Boosters:** {s.premium_subscription_count}\n**Location:** {s.region}\n**Members:** {s.member_count}\n**Verification Level:** {s.verification_level}")
        await ctx.send(embed=embed)

    @commands.command()	
    async def botinfo(self, ctx):
        embed = discord.Embed(
            colour = discord.Colour.blue(),
            timestamp=datetime.datetime.utcnow()
        )
        owner = await self.client.fetch_user(fork_owner_id)
        embed.add_field(name="Fork Owner",value=f"{owner.name}#{owner.discriminator}", inline=True)
        embed.add_field(name='Bot Information', value=f"""󠀠\n\n**Forked from Gid Bot on Github**\n**Originnaly made by:** __Gidor#7092__\n**\n**Version:** {fork_version}\n**Watching:** *{len(self.client.guilds)}* Servers & *{self.client.shard_count}* Shard\n**Members:** {len(self.client.users)}\n**Libraries:** Python 3.8.3, Discord.py v1.7.3\n**CPU:** Your system\n**Running On:** Your OS""", inline=False)
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)

    @commands.command(aliases=["uinfo"])	
    async def userinfo(self, ctx, user: discord.User):
        mem = await ctx.message.guild.fetch_member(user.id)
        if str(mem.status) == 'online':
            allapot = "Online"
        if str(mem.status) == 'idle':
            allapot = "Idling"
        if str(mem.status) == 'dnd':
            allapot = "Do Not Disturb" #these needs presence intent
        if str(mem.status) == 'offline':
            allapot = "Offline"
        try:
            avatar = user.avatar_url
            embed = discord.Embed(colour = discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="User Information", value=f"󠀠\n**Name:** {mem.name}\n**ID:** {mem.id}\n**Top Role:** {mem.top_role.mention}\n**Status:** {allapot}\n**Joined at:** {mem.joined_at.__format__('%A, %Y. %m. %d. @ %H:%M:%S')}\n**Registered at:** {mem.created_at.__format__('%A, %Y. %m. %d. @ %H:%M:%S')}")
            embed.set_author(name=user, icon_url=user.avatar_url)
            embed.set_footer(text='GidBot | {}'.format(v))  
            embed.set_thumbnail(url=avatar)
            await ctx.send(embed=embed)
        except:
            pass

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        embed = discord.Embed(title='Error!', description=':x: You forgot to menion a user.', colour=discord.Colour.red())
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)	


    @commands.command()	
    async def channelinfo(self, ctx):
        embed = discord.Embed(
            colour = discord.Colour.blue(),
            timestamp=datetime.datetime.utcnow()
        )
        if str(ctx.message.channel.type) == 'text':
            topic = "None"
        else:
            topic = ctx.message.channel.type

        embed.add_field(name='Channel Information', value=f"󠀠󠀠󠀠󠀠󠀠\n**Name:** {ctx.message.channel.mention}\n**ID:** {ctx.message.channel.id}\n**Topic:** {topic}\n**Created at:** {ctx.message.channel.created_at.__format__('%A, %Y. %m. %d. @ %H:%M:%S')}".format(ctx.message.channel.mention))
        embed.set_footer(text='GidBot | {}'.format(v))  
        
        await ctx.send(embed=embed)


    @commands.command()	
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send("Pinging...")
        ping = (time.monotonic() - before) * 100
        await message.edit(content="<a:check:677157258320150530> Pong! Response time: **{}ms**".format(int(ping)))



def setup(client):
    client.add_cog(General(client))
