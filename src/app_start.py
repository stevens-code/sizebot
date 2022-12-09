# This requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord import app_commands

# Includes functions to load data from the system (including messages from the data/messages files)
from data_store import *
# Includes all the size ray command processing
from sizeray import *
# Includes all the Magic 8 Ball functionality
from magic8 import *
# Includes all the dice command processing
from dice import *

description = """SizeBot"""

# Loads all of the data used by the bot such as messages, the database, and
# the Discord token that it needs to run
data_store = DataStore()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# === Sizebot commands ===
@tree.command(description = "Fires a shrink ray at someone.")
async def shrink(interaction: discord.Interaction, target: discord.Member):
    await interaction.response.send_message(sizeray_shrink(data_store, interaction, target))

@tree.command(description = "Fires a growth ray at someone.")
async def grow(interaction: discord.Interaction, target: discord.Member):
    await interaction.response.send_message(sizeray_grow(data_store, interaction, target))

@tree.command(description = "Fires the size ray at someone.")
async def sizeray(interaction: discord.Interaction, target: discord.Member):
    await interaction.response.send_message(sizeray_sizeray(data_store, interaction, target))

# === Dice commands ===
@tree.command(description = "Rolls the dice.")
async def roll(interaction: discord.Interaction, limit: int, rolls: int = 1):
    await interaction.response.send_message(dice_roll(limit, rolls))

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")

    # Sync slash commands
    for guild in data_store.guilds:
        print(f"Syncing tree for guild {guild}")
        await tree.sync(guild= guild)

    print("Finished all tree syncs")

client.run(data_store.discord_bot_token)