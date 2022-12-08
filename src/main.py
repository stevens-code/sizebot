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

description = '''SizeBot'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

# Load messages from files so they can be used by the commands 
# Also loads the bot token used to authenticate the bot
data_store = DataStore()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def reloadmessages(ctx, member: discord.Member):
    data_store.load_messages()
    await ctx.send("Reloaded messages")

@bot.command()
async def shrink(ctx, member: discord.Member):
    await ctx.send(sizeray_shrink(data_store, member, ctx.message.author))

@bot.command()
async def grow(ctx, member: discord.Member):
    await ctx.send(sizeray_grow(data_store, member, ctx.message.author))

@bot.command()
async def sizeray(ctx, member: discord.Member):
    await ctx.send(sizeray_sizeray(data_store, member, ctx.message.author))

@bot.command()
async def roll(ctx, limit: int, rolls: int = 1):
    await ctx.send(dice_roll(limit, rolls))

bot.run(data_store.discord_bot_token)