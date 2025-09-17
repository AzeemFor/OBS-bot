# ============================
# Discord Owo-Style Bot
# GitHub & Replit Ready
# ============================

import discord
from discord.ext import commands
import random
import os
from flask import Flask
from threading import Thread
from datetime import datetime, timedelta

# ============================
# Bot Setup
# ============================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

# ============================
# Economy Data
# ============================
user_balances = {}
user_inventories = {}
user_pets = {}
work_cooldowns = {}
daily_cooldowns = {}
beg_cooldowns = {}

# Helper Functions
def get_balance(user):
    return user_balances.get(user.id, 1000)

def set_balance(user, amount):
    user_balances[user.id] = amount

def update_balance(user, amount):
    balance = get_balance(user) + amount
    set_balance(user, balance)
    return balance

# ============================
# Admin Commands
# Only c4rtt. can use these
# ============================
@bot.command()
async def addmoney(ctx, user: discord.Member, amount: int):
    if str(ctx.author) != "c4rtt.#0000":  # Replace #0000 with the full tag of c4rtt.
        await ctx.send("You do not have permission to use this command!")
        return
    update_balance(user, amount)
    await ctx.send(f"Added {amount} coins to {user.mention}. New balance: {get_balance(user)}")

@bot.command()
async def removemoney(ctx, user: discord.Member, amount: int):
    if str(ctx.author) != "c4rtt.#0000":  # Replace #0000 with the full tag of c4rtt.
        await ctx.send("You do not have permission to use this command!")
        return
    update_balance(user, -amount)
    await ctx.send(f"Removed {amount} coins from {user.mention}. New balance: {get_balance(user)}")

# ============================
# Economy & Game Commands with cooldowns
# ============================
@bot.command()
async def balance(ctx):
    await ctx.send(f"{ctx.author.mention}, your balance is {get_balance(ctx.author)} coins.")

@bot.command()
async def work(ctx):
    now = datetime.utcnow()
    last_work = work_cooldowns.get(ctx.author.id)
    if last_work and now - last_work < timedelta(hours=5):
        remaining = timedelta(hours=5) - (now - last_work)
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"You must wait {hours}h {minutes}m {seconds}s before working again.")
        return
    earn = random.randint(100, 300)
    update_balance(ctx.author, earn)
    work_cooldowns[ctx.author.id] = now
    await ctx.send(f"{ctx.author.mention}, you worked and earned {earn} coins! Balance: {get_balance(ctx.author)}")

@bot.command()
async def daily(ctx):
    now = datetime.utcnow()
    last_daily = daily_cooldowns.get(ctx.author.id)
    if last_daily and now - last_daily < timedelta(days=1):
        remaining = timedelta(days=1) - (now - last_daily)
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"You must wait {hours}h {minutes}m {seconds}s before claiming daily again.")
        return
    reward = 500
    update_balance(ctx.author, reward)
    daily_cooldowns[ctx.author.id] = now
    await ctx.send(f"{ctx.author.mention}, you claimed your daily {reward} coins! Balance: {get_balance(ctx.author)}")

@bot.command()
async def beg(ctx):
    now = datetime.utcnow()
    last_beg = beg_cooldowns.get(ctx.author.id)
    if last_beg and now - last_beg < timedelta(hours=2):
        remaining = timedelta(hours=2) - (now - last_beg)
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"You must wait {hours}h {minutes}m {seconds}s before begging again.")
        return
    earn = random.choice([0, 50, 100])
    update_balance(ctx.author, earn)
    beg_cooldowns[ctx.author.id] = now
    await ctx.send(f"{ctx.author.mention}, you begged and got {earn} coins! Balance: {get_balance(ctx.author)}")

# ============================
# Keep alive code for Replit
# ============================
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ============================
# Run Bot
# ============================
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("No DISCORD_TOKEN found. Please set it as an environment variable.")

keep_alive()
bot.run(TOKEN)
