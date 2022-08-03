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



mainshop = [{"name":"Verified Bot Developer Badge","price":1000000,"description":"Collectible item."},
			{"name":"Gold Coin","price":100,"description":"Collectible item."},
			{"name":"Gem","price":5000,"description":"Collectible item."}]

fishes = [{"name":"Pufferfish", "price":50, "description":"Quite venomous fish."},
        {"name":"Butterflyfish", "price":55, "description":"The butterflyfish are a group of conspicuous tropical marine fish of the family Chateodontidae."},
        {"name":"Goldfish", "price":50, "description":"The goldfish is a freshwater fish in the family Cyprinidae of order Cypriniformes. "},
        {"name":"Salmon", "price":60, "description":"Salmon is the common name for several species of ray-finned fish in the family Salmonidae. "},
        {"name":"Crystal Jellyfish", "price":500, "description":"This jellyfish species is actually completely colorless!"},
        {"name":"White Jellyfish", "price":500, "description":"These jellies have very mild venom and therefore any jellyfish stings from its stinging cells are harmless to us humans. "},
        {"name":"Chaca", "price":65, "description":"These fish are commonly known as squarehead catfishes, frogmouth catfishes, or angler catfishes. "},
        {"name":"Carp", "price":60, "description":" Carp are various species of oily freshwater fish from the family Cyprinidae, a very large group of fish native to Europe and Asia."},
        {"name":"Glassfish", "price":50, "description":"The species in the family are native to Asia, Oceania, the Indian Ocean, and the western Pacific Ocean. "},
        {"name":"Emerald Catfish", "price":60, "description":"The emerald catfish is a tropical freshwater fish of the family Callichthyidae native to the Amazon Basin in South America."},
        {"name":"Damselfish", "price":55, "description":"Damselfish are those within the family of Pomacentridae. "},
        {"name":"Devilfish", "price":70, "description":"The devil fish or giant devil ray is a species of ray in the family Mobulidae. "},
        {"name":"Siamese-fighting fish", "price":50, "description":"The Siamese fighting fish commonly known as the betta, is a freshwater fish native to Southeast Asia. "}]


from bot import fork_version as v


class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy module loaded.")


    #commands
    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        em = discord.Embed(title=f"{ctx.author.name}'s balance", description="", colour=discord.Colour.blue())
        em.description += f"Wallet Balance: **{wallet_amt}$** \n Bank Balance: **{bank_amt}$**" 
        em.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed = em)


    @commands.command(aliases=["koldul"])
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        earnings = random.randrange(550, 1351)


        workmessages = [f"You worked hard, and earned **{earnings}$**.",
                        f"You worked as a discord bot developer, and earned {earnings}**$.",
                        f"You found a wallet on the street with **{earnings}$ **in it.",
                        f"You dig trough the trash and found **{earnings}$**.",
                        f"You sold some lemonade and earned **{earnings}$**.",
                        f"You sold a CS:GO Skin and earned **{earnings}$**.",
                        f"You cleaned your room and found **{earnings}$**.",
                        f"You found **{earnings}$** under your bed.",
                        f"You worked as a beggar and got **{earnings}$.**",
                        f"You worked as a cashier and got **{earnings}$**.",
                        f"You worked as a pizza delivery guy and got **{earnings}$**",
                        f"You worked as an amazon delivery driver and got **{earnings}$**",
                        f"You found a bug on discord and got **{earnings}$** for reporting it.",
                        f"You did some paperwork and earned **{earnings}$**.",
                        f"You got **{earnings}$** for winning a bet.",
                        f"You sold your car and earned **{earnings}$**.",
                        f"You worked in a restaurant and earned **{earnings}$**.",
                        f"You sold a blue necklace for **{earnings}$**.",
                        f"Someone donated to you on Twitch, and you've got **{earnings}**$."]

        em = discord.Embed(description=random.choice(workmessages), colour=discord.Colour.blue())
        em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
        em.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=em)

        users[str(user.id)]["wallet"] += earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed=discord.Embed(title="Cooldown!", description=":x: You can use this command again in {:.2f} minutes.".format(error.retry_after/60), colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
            c = self.client.get_channel(id=555057369931972632)
            await c.send("Work command used in **{}**=**{}** (On Cooldown for user)".format(ctx.message.guild.id, ctx.message.guild.name))






    @commands.command(aliases=["crimee"])
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def crime(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        earnings = random.randint(1000, 2140)
        succesrate = random.randint(0, 2)

        crimemessages = [f"You robbed a bank, and earned **{earnings}$.**",
                        f"You killed a cop, and found **{earnings}$** in her pockets.",
                        f"You stole a man's phone and sold it for **{earnings}$.**",
                        f"You killed a Mafia member and earned **{earnings}$.**",
                        f"You worked as an assasin and earned **{earnings}$.**",
                        f"You hacked NASA and got **{earnings}$.**",
                        f"You stole your moms credit card and got **{earnings}$.**",
                        f"You stole from an old man and earned **{earnings}$**.",
                        f"You hacked into a bank and transfered **{earnings}$**.",
                        f"You sold a kidney for **{earnings}$**.",
                        f"You sold a lung for **{earnings}$**.",
                        f"You robbed a store and got **{earnings}$**.",
                        f"You stole from a beggar and got **{earnings}$.**",
                        f"You broke into a safe and found **{earnings}$.**",
                        f"You kidnapped a girl and she gave you **{earnings}$** to let her free."]



        if succesrate == 1:
            em = discord.Embed(description=random.choice(crimemessages), colour=discord.Colour.blue())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)

            users[str(user.id)]["wallet"] += earnings
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
        else:
            lost = random.randint(900, 2700)

            em = discord.Embed(description=f"You have been caught and lost {lost}$", colour=discord.Colour.red())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)

            users[str(user.id)]["wallet"] -= lost
            with open("mainbank.json", "w") as f:
                json.dump(users, f)



    @crime.error
    async def crime_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed=discord.Embed(title="Cooldown!", description=":x: You can use this command again in {:.2f} minutes.".format(error.retry_after/60), colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)


    @commands.command(aliases=["bolt"])
    async def shop(self, ctx):
        em = discord.Embed(title = "Shop", description="", colour=discord.Colour.blue())

        for item in mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.set_footer(text='GidBot | {}'.format(v))
            em.description += f"{name} | **{price}$** - {desc} \n\n"
        for fish in fishes:
            name = fish["name"]
            price = fish["price"]
            desc = fish["description"]
            em.set_footer(text='GidBot | {}'.format(v))
            em.description += f"{name} | **{price}$** - {desc} \n\n"
            
        await ctx.send(embed=em)


    @commands.command(aliases=["bui"])
    async def buy(self, ctx,amount=1, *, item):
        await open_account(ctx.author)

        res = await buy_this(ctx.author, item, amount)

        if not res[0]:
            if res[1]==1:
                em = discord.Embed(description="That product is not available here, or can't be bought.", colour=discord.Colour.red())
                em.set_footer(text='GidBot | {}'.format(v))
                await ctx.send(embed=em)
                return
            if res[1]==2:
                em = discord.Embed(description=f"You don't have enough money in your wallet to buy **{amount}** of **{item}**!", colour=discord.Colour.red())
                em.set_footer(text='GidBot | {}'.format(v))
                await ctx.send(embed=em)
                return

        em = discord.Embed(description=f"You just bought **{amount}** of **{item}**", colour=discord.Colour.blue())
        em.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=em)

    @commands.command(aliases=["with"])
    async def withdraw(self, ctx, amount = None):
        await open_account(ctx.author)

        if amount == None:
            em = discord.Embed(description=":x: Please specify the withdrawal amount!", colour=discord.Colour.red())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)
            return

        bal = await update_bank(ctx.author)

        if amount == "all":
            amount = bal[1]

        amount = int(amount)
        if amount>bal[1]:
            em = discord.Embed(description=":x: You don't have that much money!", colour=discord.Colour.red())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)
            return
        if amount<0:
            em = discord.Embed(description=":x: Amount must be a positive number!", colour=discord.Colour.red())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)
            return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1*amount, "bank")

        em = discord.Embed(description=f"You withdrew **{amount}**$!", colour=discord.Colour.blue())
        em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
        em.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=em)
        return

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, amount = None):
        await open_account(ctx.author)

        if amount == None:
            em = discord.Embed(description=":x: Please specify the amount to be deposited!", colour=discord.Colour.red())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)
            return

        bal = await update_bank(ctx.author)

        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount>bal[0]:
            em = discord.Embed(description=":x: You don't have that much money!", colour=discord.Colour.red())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)
            return
        if amount<0:
            em = discord.Embed(description=":x: Amount must be a positive number!", colour=discord.Colour.red())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)
            return

        await update_bank(ctx.author, -1*amount)
        await update_bank(ctx.author, amount, "bank")

        em = discord.Embed(description=f"You deposited **{amount}**$!", colour=discord.Colour.blue())
        em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
        em.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=em)
        return

    @commands.command(aliases=["send"])
    async def pay(self, ctx, member: discord.Member, amount = None):
        await open_account(ctx.author)
        await open_account(member)

        if amount == None:
            em = discord.Embed(description=":x: Please specify the amount to be given!", colour=discord.Colour.red())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)
            return

        bal = await update_bank(ctx.author)

        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount>bal[0]:
            em = discord.Embed(description=":x: You don't have that much money!", colour=discord.Colour.red())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)
            return
        if amount<0:
            em = discord.Embed(description=":x: Amount must be a positive number!", colour=discord.Colour.red())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)
            return

        await update_bank(ctx.author, -1*amount, "wallet")
        await update_bank(member, amount, "bank")

        em = discord.Embed(description=f"You gave **{amount}**$ to **{member.name}**!", colour=discord.Colour.blue())
        em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
        em.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=em)
        return


    @commands.command(aliases=["lop"])
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def rob(self, ctx, member:discord.Member):
        await open_account(ctx.author)
        await open_account(member)

        bal = await update_bank(member)

        succesrate = random.randint(0, 4)

        if bal[0]<1:
            em2 = discord.Embed(description="You can't rob him, because he has no money in his wallet.", colour=discord.Colour.red())
            em2.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em2.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em2)
            return

        if succesrate == 1:
            earnings = random.randint(round(bal[0]*0.1), round(bal[0]*0.7))


            await update_bank(ctx.author, earnings) 
            await update_bank(member, -1*earnings, "wallet")
            em = discord.Embed(description=f"You robbed **{earnings}$** from **{member.name}**!", colour=discord.Colour.blue())
            em.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em)
            return


        else:
            earnings = random.randint(1200, 2700)

            await update_bank(ctx.author, -1*earnings, "wallet") 
            em3 = discord.Embed(description=f"You have been caught and you recived a **{1*earnings}**$ fine!", colour=discord.Colour.blue())
            em3.set_author(name=ctx.author.name, icon_url=ctx.message.author.avatar_url)
            em3.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=em3)
            return


    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed=discord.Embed(title="Cooldown!", description=":x: You can use this command again in {:.2f} minutes.".format(error.retry_after/60), colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
          
        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(description=":x: Please Specify the user!", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)
          
        if isinstance(error, BadArgument):
            embed=discord.Embed(description=":x: I can't find an user named like that.", colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)



    @commands.command(aliases=["inv","inventory"])
    async def bag(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em = discord.Embed(title = "Inventory", description="" ,colour=discord.Colour.blue())
        for item in bag:
            name = item["item"]
            amount = item["amount"]

            em.description += f"**{name}** - {amount} \n"
            
        em.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed = em)

    @commands.command(aliases=["f"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fish(self, ctx):
        fish = random.choice(fishes)
        number = random.randint(2,6)
        name = fish["name"]
        if "Jellyfish" in fish["name"]:
            number = 1
            
            fishr = await add_item(ctx.author, fish["name"], number)
        else:
            fishr = await add_item(ctx.author, fish["name"], number)
            
        embed=discord.Embed(description=f"You caught **{number}** of **{name}**", colour=discord.Colour.blue())
        embed.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=embed)
        
    @fish.error
    async def fish_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed=discord.Embed(title="Cooldown!", description=":x: You can use this command again in {:.1f} seconds.".format(error.retry_after), colour=discord.Colour.red())
            embed.set_footer(text='GidBot | {}'.format(v))
            await ctx.send(embed=embed)

  
    @commands.command(aliases=["soll"])
    async def sell(self, ctx, amount = 1, *, item):
        await open_account(ctx.author)

        if "fish" in item:
            fishres = await sell_fish(ctx.author, item, amount)

            if not fishres[0]:
                if fishres[1]==1:
                    em = discord.Embed(description="That fish is not available in the shop.", colour=discord.Colour.red())
                    em.set_footer(text='GidBot | {}'.format(v))
                    await ctx.send(embed=em)
                    return
                if fishres[1]==2:
                    em = discord.Embed(description=f"You don't have **{amount}** **{item}**, in your bag.", colour=discord.Colour.red())
                    em.set_footer(text='GidBot | {}'.format(v))
                    await ctx.send(embed=em)
                    return
                if fishres[1]==3:
                    em = discord.Embed(description=f"You don't have **{item}** in your bag.", colour=discord.Colour.red())
                    em.set_footer(text='GidBot | {}'.format(v))
                    await ctx.send(embed=em)
                    return
        else:
            res = await sell_this(ctx.author, item, amount)
            if not res[0]:
                if res[1]==1:
                    em = discord.Embed(description="That product is not available in the shop.", colour=discord.Colour.red())
                    em.set_footer(text='GidBot | {}'.format(v))
                    await ctx.send(embed=em)
                    return
                if res[1]==2:
                    em = discord.Embed(description=f"You don't have **{amount}** **{item}**, in your bag.", colour=discord.Colour.red())
                    em.set_footer(text='GidBot | {}'.format(v))
                    await ctx.send(embed=em)
                    return
                if res[1]==3:
                    em = discord.Embed(description=f"You don't have **{item}** in your bag.", colour=discord.Colour.red())
                    em.set_footer(text='GidBot | {}'.format(v))
                    await ctx.send(embed=em)
                    return

        em = discord.Embed(title=f"You just sold **{amount}** **{item}**.", colour=discord.Colour.blue())
        em.set_footer(text='GidBot | {}'.format(v))
        await ctx.send(embed=em)
    
    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx, x = 10):
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total, reverse=True)
        em = discord.Embed(title = f"Top {x} Richest People (Global)", description="", color=discord.Colour.blue())
        em.set_footer(text='GidBot | {}'.format(v))
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            mem = await self.client.fetch_user(id_)
            name = mem.name
            em.description += f"**{index}**) **{name}** - *{amt}$* \n"
            if index == x:
                break
            else:
                index += 1

        await ctx.send(embed = em)


async def sell_this(user,item_name,amount,price=None):
    itemname = item_name
    name_ = None
    for item in mainshop:
        name = item["name"]
        if name  == itemname:
            name_ = name
            if price==None:
                price = item["price"]
            break
    if name_ == None:
        return [False,1]

    cost = price*amount 

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == itemname:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            return [False,3]
    except:
        return [False,3]

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

async def sell_fish(user,item_name,amount):
    itemname = item_name
    name_ = None
    price = None
    for item in fishes:
        name = item["name"]
        if name  == itemname:
            name_ = name
            price = item["price"]
            break
    if name_ == None:
        return [False,1]

    cost = price*amount 

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == itemname:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            return [False,3]
    except:
        return [False,3]

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

async def del_this(user,item_name,amount,price=None):
    itemname = item_name
    name_ = None
    for item in mainshop:
        name = item["name"]
        if name  == itemname:
            name_ = name
            if price==None:
                price = item["price"]
            break
    if name_ == None:
        return [False,1]

    cost = price*amount 

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == itemname:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            return [False,3]
    except:
        return [False,3]

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    await update_bank(user)

    return [True,"Worked"]



async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users 

async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change
    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]

    return bal



async def add_item(user, item_name, amount):
    item_name = item_name
    name_ = None
    for item in fishes:
        name = item["name"]
        if name == item_name:
            name_ = name
            break

    if name_ == None:
        return [False,1]

    users = await get_bank_data()
    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            obj = {"item":item_name, "amount":amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name, "amount":amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    await update_bank(user,amount*0, "wallet")

    return [True, "Worked"]




async def buy_this(user, item_name, amount):
    item_name = item_name
    name_ = None
    for item in mainshop:
        name = item["name"]
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount
    users = await get_bank_data()
    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            obj = {"item":item_name, "amount":amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name, "amount":amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1, "wallet")

    return [True, "Worked"]

def setup(client):
    client.add_cog(Economy(client))
