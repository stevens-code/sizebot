# This requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands

# Includes functions to load data from the system (including messages from the data/messages files)
from data_store import *
# Includes all the size ray command processing
from sizeray import *
# Includes all the Magic 8 Ball functionality
from magic8 import *
# Includes all the dice command processing
from dice import *

description = """SizeBot"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", description=description, intents=intents)

# Loads all of the data used by the bot such as messages, the database, and
# the Discord token that it needs to run
data_store = DataStore()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

# === Sizebot commands ===
@bot.command()
async def shrink(message_ctx: Context, target: discord.Member):
    await message_ctx.send(sizeray_shrink(data_store, message_ctx, target))

@bot.command()
async def grow(message_ctx: Context, target: discord.Member):
    await message_ctx.send(sizeray_grow(data_store, message_ctx, target))

@bot.command()
async def sizeray(message_ctx: Context, target: discord.Member):
    await message_ctx.send(sizeray_sizeray(data_store, message_ctx, target))

# === Dice commands ===
@bot.command()
async def roll(message_ctx: Context, limit: int, rolls: int = 1):
    await message_ctx.send(dice_roll(limit, rolls))

bot.run(data_store.discord_bot_token)