# ============================
# Discord Owo-Style Bot (Full 40+ commands)
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
inventory = {}
pets = {}
shop_items = {"Sword": 500, "Shield": 400, "Potion": 50}
leaderboard_limit = 10

# ============================
# Helper Functions
# ============================
def get_balance(user):
    return user_balances.get(user.id, 1000)

def update_balance(user, amount):
    balance = get_balance(user) + amount
    user_balances[user.id] = balance
    return balance

def can_use(user_id, cooldown_dict, delta):
    now = datetime.utcnow()
    last = cooldown_dict.get(user_id)
    if last and now - last < delta:
        return False, delta - (now - last)
    cooldown_dict[user_id] = now
    return True, None

# ============================
# Admin Commands (c4rtt. only)
# ============================
ADMIN_ID = 1001809123249238096  # your Discord ID

@bot.command()
async def addmoney(ctx, user: discord.Member, amount: int):
    if ctx.author.id != ADMIN_ID:
        await ctx.send("You do not have permission!")
        return
    update_balance(user, amount)
    await ctx.send(f"{amount} has been added to {user.display_name}'s balance. New balance: {get_balance(user)}")

@bot.command()
async def removemoney(ctx, user: discord.Member, amount: int):
    if ctx.author.id != ADMIN_ID:
        await ctx.send("You do not have permission!")
        return
    update_balance(user, -amount)
    await ctx.send(f"{amount} has been removed from {user.display_name}'s balance. New balance: {get_balance(user)}")
# ============================
# Economy Commands
# ============================
@bot.command()
async def balance(ctx):
    await ctx.send(f"{ctx.author.mention}, your balance is {get_balance(ctx.author)} coins.")

@bot.command()
async def work(ctx):
    ok, rem = can_use(ctx.author.id, work_cooldowns, timedelta(hours=5))
    if not ok:
        h, r = divmod(rem.seconds, 3600)
        m, s = divmod(r, 60)
        await ctx.send(f"Wait {h}h {m}m {s}s before working again.")
        return
    earn = random.randint(100, 300)
    update_balance(ctx.author, earn)
    await ctx.send(f"{ctx.author.mention} worked and earned {earn} coins! Balance: {get_balance(ctx.author)}")

@bot.command()
async def daily(ctx):
    ok, rem = can_use(ctx.author.id, daily_cooldowns, timedelta(days=1))
    if not ok:
        h, r = divmod(rem.seconds, 3600)
        m, s = divmod(r, 60)
        await ctx.send(f"Wait {h}h {m}m {s}s before claiming daily again.")
        return
    reward = 500
    update_balance(ctx.author, reward)
    await ctx.send(f"{ctx.author.mention} claimed daily {reward} coins! Balance: {get_balance(ctx.author)}")

@bot.command()
async def beg(ctx):
    ok, rem = can_use(ctx.author.id, beg_cooldowns, timedelta(hours=2))
    if not ok:
        h, r = divmod(rem.seconds, 3600)
        m, s = divmod(r, 60)
        await ctx.send(f"Wait {h}h {m}m {s}s before begging again.")
        return
    earn = random.choice([0, 50, 100])
    update_balance(ctx.author, earn)
    await ctx.send(f"{ctx.author.mention} begged and got {earn} coins! Balance: {get_balance(ctx.author)}")

# ============================
# Mini-Games
# ============================
@bot.command()
async def coinflip(ctx, amount: int, choice: str):
    choice = choice.lower()
    if choice not in ["heads", "tails"]:
        await ctx.send("Please say heads or tails!")
        return
    if amount > get_balance(ctx.author):
        await ctx.send("Not enough coins!")
        return
    result = random.choice(["heads", "tails"])
    if choice == result:
        update_balance(ctx.author, amount)
        await ctx.send(f"It's {result}! You won {amount} coins! Balance: {get_balance(ctx.author)}")
    else:
        update_balance(ctx.author, -amount)
        await ctx.send(f"It's {result}! You lost {amount} coins! Balance: {get_balance(ctx.author)}")

@bot.command()
async def blackjack(ctx, bet: int):
    if bet > get_balance(ctx.author):
        await ctx.send("Not enough coins!")
        return
    if random.random() < 0.5:
        update_balance(ctx.author, bet)
        await ctx.send(f"You won {bet} coins! Balance: {get_balance(ctx.author)}")
    else:
        update_balance(ctx.author, -bet)
        await ctx.send(f"You lost {bet} coins! Balance: {get_balance(ctx.author)}")

@bot.command()
async def slots(ctx, bet: int):
    if bet > get_balance(ctx.author):
        await ctx.send("Not enough coins!")
        return
    symbols = ["🍎", "🍌", "🍒", "🍇", "🍉"]
    result = [random.choice(symbols) for _ in range(3)]
    await ctx.send(" | ".join(result))
    if len(set(result)) == 1:
        win = bet * 3
        update_balance(ctx.author, win)
        await ctx.send(f"Jackpot! You won {win} coins! Balance: {get_balance(ctx.author)}")
    elif len(set(result)) == 2:
        win = bet
        update_balance(ctx.author, win)
        await ctx.send(f"You won {win} coins! Balance: {get_balance(ctx.author)}")
    else:
        update_balance(ctx.author, -bet)
        await ctx.send(f"You lost {bet} coins! Balance: {get_balance(ctx.author)}")

@bot.command()
async def roulette(ctx, bet: int, color: str):
    if bet > get_balance(ctx.author):
        await ctx.send("Not enough coins!")
        return
    color = color.lower()
    if color not in ["red", "black", "green"]:
        await ctx.send("Pick red, black, or green!")
        return
    outcome = random.choices(["red","black","green"], weights=[18,18,2])[0]
    if color == outcome:
        win = bet*2 if color!="green" else bet*14
        update_balance(ctx.author, win)
        await ctx.send(f"The ball landed on {outcome}! You won {win} coins! Balance: {get_balance(ctx.author)}")
    else:
        update_balance(ctx.author, -bet)
        await ctx.send(f"The ball landed on {outcome}! You lost {bet} coins! Balance: {get_balance(ctx.author)}")

# ============================
# Inventory & Pets
# ============================
@bot.command()
async def inventory(ctx):
    inv = inventory.get(ctx.author.id, [])
    await ctx.send(f"{ctx.author.mention}'s inventory: {', '.join(inv) if inv else 'Empty'}")

@bot.command()
async def adopt(ctx, pet_name: str):
    pets.setdefault(ctx.author.id, []).append(pet_name)
    await ctx.send(f"{ctx.author.mention} adopted {pet_name}!")

@bot.command()
async def petslist(ctx):
    p = pets.get(ctx.author.id, [])
    await ctx.send(f"{ctx.author.mention}'s pets: {', '.join(p) if p else 'None'}")

@bot.command()
async def fish(ctx):
    catch = random.choice(["🐟", "🐠", "🦈"])
    inventory.setdefault(ctx.author.id, []).append(catch)
    await ctx.send(f"{ctx.author.mention} caught a {catch}!")

@bot.command()
async def hunt(ctx):
    catch = random.choice(["🦌","🐗","🐇"])
    inventory.setdefault(ctx.author.id, []).append(catch)
    await ctx.send(f"{ctx.author.mention} hunted a {catch}!")

# ============================
# Shop Commands
# ============================
@bot.command()
async def shop(ctx):
    items = [f"{name}: {price} coins" for name, price in shop_items.items()]
    await ctx.send("Available items:\n" + "\n".join(items))

@bot.command()
async def buy(ctx, item: str):
    if item not in shop_items:
        await ctx.send("Item not found!")
        return
    price = shop_items[item]
    if get_balance(ctx.author) < price:
        await ctx.send("Not enough coins!")
        return
    update_balance(ctx.author, -price)
    inventory.setdefault(ctx.author.id, []).append(item)
    await ctx.send(f"{ctx.author.mention} bought {item}! Balance: {get_balance(ctx.author)}")

@bot.command()
async def sell(ctx, item: str):
    inv = inventory.get(ctx.author.id, [])
    if item not in inv:
        await ctx.send("You don't own that item!")
        return
    inv.remove(item)
    price = shop_items.get(item, 10)//2
    update_balance(ctx.author, price)
    await ctx.send(f"{ctx.author.mention} sold {item} for {price} coins! Balance: {get_balance(ctx.author)}")

# ============================
# Fun / Social
# ============================
@bot.command()
async def hug(ctx, user: discord.Member):
    await ctx.send(f"{ctx.author.mention} hugged {user.mention} 🤗")
@bot.command()
async def slap(ctx, user: discord.Member):
    await ctx.send(f"{ctx.author.mention} slapped {user.mention} 😡")
@bot.command()
async def kiss(ctx, user: discord.Member):
    await ctx.send(f"{ctx.author.mention} kissed {user.mention} 😘")
@bot.command()
async def poke(ctx, user: discord.Member):
    await ctx.send(f"{ctx.author.mention} poked {user.mention} 👈")
@bot.command()
async def feed(ctx, user: discord.Member):
    await ctx.send(f"{ctx.author.mention} fed {user.mention} 🍗")

# ============================
# Leaderboard
# ============================
@bot.command()
async def leaderboard(ctx):
    top = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)[:leaderboard_limit]
    msg = "Leaderboard:\n"
    for idx, (uid, bal) in enumerate(top, start=1):
        member = ctx.guild.get_member(uid)
        if member:
            msg += f"{idx}. {member.display_name}: {bal} coins\n"
    await ctx.send(msg)

# ============================
# Keep-alive for Replit
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
if not TOKEN:
    raise ValueError("Set DISCORD_TOKEN environment variable")

keep_alive()
bot.run(TOKEN)



