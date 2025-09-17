# ============================
# Discord Owo-Style Bot (40+ commands)
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
# Economy & Game Data
# ============================
user_balances = {}
work_cooldowns = {}
daily_cooldowns = {}
beg_cooldowns = {}
coinflip_cooldowns = {}
blackjack_games = {}
inventory = {}

# ============================
# Helper Functions
# ============================
def get_balance(user):
    return user_balances.get(user.id, 1000)

def update_balance(user, amount):
    balance = get_balance(user) + amount
    user_balances[user.id] = balance
    return balance

def can_use_command(cooldown_dict, user_id, delta):
    now = datetime.utcnow()
    last = cooldown_dict.get(user_id)
    if last and now - last < delta:
        return False, delta - (now - last)
    cooldown_dict[user_id] = now
    return True, None

# ============================
# Admin Commands
# Only c4rtt. can use
# ============================
@bot.command()
async def addmoney(ctx, user: discord.Member, amount: int):
    if str(ctx.author) != "c4rtt.#0000":  # replace with full tag
        await ctx.send("You do not have permission!")
        return
    update_balance(user, amount)
    await ctx.send(f"Added {amount} coins to {user.mention}. New balance: {get_balance(user)}")

@bot.command()
async def removemoney(ctx, user: discord.Member, amount: int):
    if str(ctx.author) != "c4rtt.#0000":
        await ctx.send("You do not have permission!")
        return
    update_balance(user, -amount)
    await ctx.send(f"Removed {amount} coins from {user.mention}. New balance: {get_balance(user)}")

# ============================
# Economy Commands
# ============================
@bot.command()
async def balance(ctx):
    await ctx.send(f"{ctx.author.mention}, your balance is {get_balance(ctx.author)} coins.")

@bot.command()
async def work(ctx):
    ok, remaining = can_use_command(work_cooldowns, ctx.author.id, timedelta(hours=5))
    if not ok:
        hours, rem = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        await ctx.send(f"Wait {hours}h {minutes}m {seconds}s to work again.")
        return
    earned = random.randint(100, 300)
    update_balance(ctx.author, earned)
    await ctx.send(f"{ctx.author.mention} worked and earned {earned} coins! Balance: {get_balance(ctx.author)}")

@bot.command()
async def daily(ctx):
    ok, remaining = can_use_command(daily_cooldowns, ctx.author.id, timedelta(days=1))
    if not ok:
        hours, rem = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        await ctx.send(f"Wait {hours}h {minutes}m {seconds}s to claim daily again.")
        return
    reward = 500
    update_balance(ctx.author, reward)
    await ctx.send(f"{ctx.author.mention} claimed daily {reward} coins! Balance: {get_balance(ctx.author)}")

@bot.command()
async def beg(ctx):
    ok, remaining = can_use_command(beg_cooldowns, ctx.author.id, timedelta(hours=2))
    if not ok:
        hours, rem = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        await ctx.send(f"Wait {hours}h {minutes}m {seconds}s to beg again.")
        return
    reward = random.choice([0, 50, 100])
    update_balance(ctx.author, reward)
    await ctx.send(f"{ctx.author.mention} begged and got {reward} coins! Balance: {get_balance(ctx.author)}")

# ============================
# Coinflip Command
# ============================
@bot.command()
async def coinflip(ctx, amount: int, choice: str):
    choice = choice.lower()
    if choice not in ["heads", "tails"]:
        await ctx.send("Please say heads or tails!")
        return
    bal = get_balance(ctx.author)
    if amount > bal:
        await ctx.send("You don't have enough coins!")
        return
    flip = random.choice(["heads", "tails"])
    if choice == flip:
        update_balance(ctx.author, amount)
        await ctx.send(f"It's {flip}! You won {amount} coins! Balance: {get_balance(ctx.author)}")
    else:
        update_balance(ctx.author, -amount)
        await ctx.send(f"It's {flip}! You lost {amount} coins! Balance: {get_balance(ctx.author)}")

# ============================
# Blackjack Command (simplified)
# ============================
@bot.command()
async def blackjack(ctx, bet: int):
    bal = get_balance(ctx.author)
    if bet > bal:
        await ctx.send("You don't have enough coins!")
        return
    # Simplified: win 50% chance
    if random.random() < 0.5:
        update_balance(ctx.author, bet)
        await ctx.send(f"You won {bet} coins! Balance: {get_balance(ctx.author)}")
    else:
        update_balance(ctx.author, -bet)
        await ctx.send(f"You lost {bet} coins! Balance: {get_balance(ctx.author)}")

# ============================
# Fun Commands (example subset)
# ============================
@bot.command()
async def hug(ctx, user: discord.Member):
    await ctx.send(f"{ctx.author.mention} hugged {user.mention}! 🤗")

@bot.command()
async def slap(ctx, user: discord.Member):
    await ctx.send(f"{ctx.author.mention} slapped {user.mention}! 😡")

@bot.command()
async def kiss(ctx, user: discord.Member):
    await ctx.send(f"{ctx.author.mention} kissed {user.mention}! 😘")

# ============================
# Keep-alive server for Replit
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
    raise ValueError("No DISCORD_TOKEN found. Set it as an environment variable.")

keep_alive()
bot.run(TOKEN)
