# This requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext.commands import has_permissions
from discord import app_commands

# Includes functions to load data from the system (including messages from the data/messages files)
from data_store import *
# Includes all the size ray functionality
from sizeray import *
# Includes all the Magic 8 Ball functionality
from magic8 import *
# Includes all the dice functionality
from dice import *
# Includes all greeter functionality
from greeter import *
# Includes app info
from about import *
# Includes utility functions
from util import *
# Includes mod functions
from mod import *
# Character lines
from characters import *

description = """SizeBot"""

# Loads all of the data used by the bot such as messages, the database, and
# the Discord token that it needs to run
data_store = DataStore()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# === Events ===
# Automatically send a message when someone joins
@client.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    channel = member.guild.system_channel # Get the channel to send notifications in
    if channel.permissions_for(guild.me).send_messages: # Check for permissions
        await greeter_welcome(data_store, channel, member)
    print(f'"{member.display_name}" has joined the server "{guild.name}"')

# Automatically send a message when someone leaves
@client.event
async def on_member_remove(member: discord.Member):
    guild = member.guild
    channel = member.guild.system_channel # Get the channel to send notifications in
    if channel.permissions_for(guild.me).send_messages: # Check for permissions
        await greeter_goodbye(data_store, channel, member)
    print(f'"{member.display_name}" has left the server "{guild.name}"')

# === Size ray commands ===
@tree.command(name = "shrink", description = "Fires a shrink ray at someone.")
async def shrink(interaction: discord.Interaction, target: discord.Member):
    await sizeray_shrink(data_store, interaction, target)

@tree.command(name = "grow", description = "Fires a growth ray at someone.")
async def grow(interaction: discord.Interaction, target: discord.Member):
    await sizeray_grow(data_store, interaction, target)

@tree.command( name = "sizeray", description = "Fires the size ray at someone.")
async def sizeray(interaction: discord.Interaction, target: discord.Member):
    await sizeray_sizeray(data_store, interaction, target)

@tree.command( name = "toggle-immunity", description = "Toggles your size ray immunity.")
async def toggle_immunity(interaction: discord.Interaction):
    await sizeray_toggle_immunity(data_store, interaction)

@tree.command( name = "sizeray-last-10", description = "Get a list of the last 10 size ray actions.")
async def sizeray_last_10(interaction: discord.Interaction):
    await sizeray_get_last_10(data_store, interaction)

# === Dice commands ===
@tree.command(name = "roll", description = "Rolls a X sided die for up to a 100 rolls. Defaults to a single roll of a 6 sided die.")
async def roll(interaction: discord.Interaction, sides: int = 6, rolls: int = 1):
    await dice_roll(interaction, sides, rolls)
    
# === Magic 8 ball commands ===
@tree.command(name = "magic8", description = "Ask the Magic 8 ball something.")
async def magic8(interaction: discord.Interaction, question: str = ""):
    await magic8_ask(data_store, interaction, question)

# === Greeter commands ===
@tree.command(name = "welcome", description = "Welcome a user.")
async def welcome(interaction: discord.Interaction, target: discord.Member):
    await greeter_welcome(data_store, interaction, target)

@tree.command(name = "goodbye", description = "Say goodbye to a user.")
async def goodbye(interaction: discord.Interaction, target: discord.Member):
    await greeter_goodbye(data_store, interaction, target)

# === About commands ===
@tree.command(name = "about-sizebot", description = "Get info about SizeBot and the system it's running on.")
async def about_sizebot(interaction: discord.Interaction):
    await about_message(data_store, interaction)

# === Character commands ===
@tree.command(name = "scara", description = "Say a random scaramouche elemental burst line.")
async def scara(interaction: discord.Interaction):
    await character_scara(data_store, interaction)

# === Mod-only commands ===
@tree.command(name="set-sizebot-variable", description = "Set a server-specific variable to be replaced in SizeBot messages.")
@has_permissions(administrator = True)
async def set_sizebot_variable(interaction: discord.Interaction, variable_name: str, variable_value: str):
    await mod_set_sizebot_variable(data_store, interaction, variable_name, variable_value)

@tree.command(name="delete-sizebot-variable", description = "Delete a server-specific variable from SizeBot.")
@has_permissions(administrator = True)
async def delete_sizebot_variable(interaction: discord.Interaction, variable_name: str):
    await mod_delete_sizebot_variable(data_store, interaction, variable_name)

@tree.command(name="set-sizebot-welcome", description = "Set the SizeBot welcome image.")
@has_permissions(administrator = True)
async def set_sizebot_welcome(interaction: discord.Interaction, file: discord.Attachment):
    await mod_set_sizebot_welcome(data_store, interaction, file)

@tree.command(name="reset-sizebot-welcome", description = "Delete the custom SizeBot welcome image and reset to default.")
@has_permissions(administrator = True)
async def reset_sizebot_welcome(interaction: discord.Interaction):
    await mod_reset_sizebot_welcome(data_store, interaction)

@tree.command(name="set-sizebot-goodbye", description = "Set the SizeBot goodbye image.")
@has_permissions(administrator = True)
async def set_sizebot_goodbye(interaction: discord.Interaction, file: discord.Attachment):
    await mod_set_sizebot_goodbye(data_store, interaction, file)

@tree.command(name="reset-sizebot-goodbye", description = "Delete the custom SizeBot goodbye image and reset to default.")
@has_permissions(administrator = True)
async def reset_sizebot_goodbye(interaction: discord.Interaction):
    await mod_reset_sizebot_goodbye(data_store, interaction)

@tree.command(name="set-sizeray-immunity-role", description = "Set the size ray immunity role.")
@has_permissions(administrator = True)
async def set_sizeray_immunity_role(interaction: discord.Interaction, role: discord.Role):
    await mod_set_sizeray_immunity_role(data_store, interaction, role)

@tree.command(name="enable-sizebot-welcome", description = "Allow SizeBot to send welcome messages.")
@has_permissions(administrator = True)
async def enable_sizebot_welcome(interaction: discord.Interaction):
    await mod_enable_sizebot_welcome(data_store, interaction)

@tree.command(name="disable-sizebot-welcome", description = "Don't allow SizeBot to send welcome messages.")
@has_permissions(administrator = True)
async def disable_sizebot_welcome(interaction: discord.Interaction):
    await mod_disable_sizebot_welcome(data_store, interaction)

@tree.command(name="enable-sizebot-goodbye", description = "Allow SizeBot to send goodbye messages.")
@has_permissions(administrator = True)
async def enable_sizebot_goodbye(interaction: discord.Interaction):
    await mod_enable_sizebot_goodbye(data_store, interaction)

@tree.command(name="disable-sizebot-goodbye", description = "Don't allow SizeBot to send goodbye messages.")
@has_permissions(administrator = True)
async def disable_sizebot_goodbye(interaction: discord.Interaction):
    await mod_disable_sizebot_goodbye(data_store, interaction)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")

    # Get guilds
    for guild in client.guilds:
        print(guild.id)

    # Sync slash commands
    for guild in data_store.guilds:
        print(f"Syncing tree for guild {guild.id}")
        tree.copy_global_to(guild=guild)
        await tree.sync(guild= guild)

    print("Finished all tree syncs")

# Launch the app
client.run(data_store.discord_bot_token)