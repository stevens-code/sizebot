# This requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord import app_commands
from datetime import date
from datetime import time
from dateutil import tz
from discord.ext import tasks

# Includes functions to load data from the system (including messages from the data/messages files)
from data_store import *
# Size ray functionality
from sizeray import *
# Show stats about the size ray
from sizeray_stats import *
# Magic 8 Ball functionality
from magic8 import *
# Picker functionality
from picker import *
# Dice functionality
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
# Bot ratings
from bot_rate import *
# Birthdays
from birthday import *
# User cache
from user_cache import *
# Size ray roles
from roles import *
# Logging
from log import *
# Floof
from floof import *
# Duck Bucks
from duck_bucks import *

description = """SizeBot"""

# Loads all of the data used by the bot such as messages, the database, and
# the Discord token that it needs to run
data_store = DataStore()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
client = discord.Client(intents = intents)
tree = app_commands.CommandTree(client)

# === Size ray commands ===
@tree.command(name = "shrink", description = "Fires a shrink ray at someone.")
async def shrink(interaction: discord.Interaction, target: discord.Member):
    await sizeray_shrink(data_store, interaction, target)

@tree.command(name = "grow", description = "Fires a growth ray at someone.")
async def grow(interaction: discord.Interaction, target: discord.Member):
    await sizeray_grow(data_store, interaction, target)

@tree.command(name = "sizeray", description = "Fires the size ray at someone.")
async def sizeray(interaction: discord.Interaction, target: discord.Member):
    await sizeray_sizeray(data_store, interaction, target)

@tree.command(name = "toggle-immunity", description = "Toggles your size ray immunity.")
async def toggle_immunity(interaction: discord.Interaction):
    await sizeray_toggle_immunity(data_store, interaction)

# === Size ray stats ===
@tree.command(name = "stats-last-10", description = "Get a list of the last 10 size ray actions.")
async def stats_last_10(interaction: discord.Interaction):
    await sizeray_stats_last_10(data_store, interaction)

@tree.command(name = "stats-all", description = "Show the size ray actions stats for a whole server.")
async def stats_chart_all(interaction: discord.Interaction):
    await sizeray_stats_chart(data_store, interaction)

@tree.command(name = "stats-target", description = "Show the size ray actions that happened to a target.")
async def stats_chart_for(interaction: discord.Interaction, target: discord.Member):
    await sizeray_stats_chart_for(data_store, interaction, target)

@tree.command(name = "stats-biggest-users", description = "Show who the 10 biggest users and targets of the size ray are.")
async def stats_biggest_users(interaction: discord.Interaction):
    await sizeray_stats_biggest_users(data_store, interaction)

# === Size role switcher ===
@tree.command(name = "toggle-tiny", description = "Toggle your tiny role.")
async def shrink(interaction: discord.Interaction):
    await toggle_permanent_size_role(data_store, interaction.guild, interaction, "tiny")

@tree.command(name = "toggle-switch", description = "Toggle your switch role.")
async def shrink(interaction: discord.Interaction):
    await toggle_permanent_size_role(data_store, interaction.guild, interaction, "switch")

@tree.command(name = "toggle-giant", description = "Toggle your giant role.")
async def shrink(interaction: discord.Interaction):
    await toggle_permanent_size_role(data_store, interaction.guild, interaction, "giant")

# === Dice commands ===
@tree.command(name = "roll", description = "Rolls a X sided die for up to a 100 rolls. Defaults to a single roll of a 6 sided die.")
async def roll(interaction: discord.Interaction, sides: int = 6, rolls: int = 1):
    await dice_roll(interaction, sides, rolls)
    
# === Magic 8 ball commands ===
@tree.command(name = "magic8", description = "Ask the Magic 8 ball something.")
async def magic8(interaction: discord.Interaction, question: str = ""):
    await magic8_ask(data_store, interaction, question)

# === Picker commands ===
@tree.command(name = "pick-from", description = "Pick a random option from a list of options. The options are split by the character \"|\".")
async def pick_from(interaction: discord.Interaction, options: str, title: str = ""):
    await picker_pick_random(data_store, interaction, title, options)

# === Greeter commands ===
@tree.command(name = "welcome", description = "Welcome a user.")
async def welcome(interaction: discord.Interaction, target: discord.Member):
    await greeter_welcome(data_store, interaction, target)

@tree.command(name = "goodbye", description = "Say goodbye to a user.")
async def goodbye(interaction: discord.Interaction, target: discord.Member):
    await greeter_goodbye(data_store, interaction, target)

# === Bot rate commands ===
@tree.command(name = "good-bot", description = "Tell SizeBot it's been good.")
async def good_bot(interaction: discord.Interaction):
    await bot_rate_good(data_store, interaction)

@tree.command(name = "bad-bot", description = "Tell SizeBot it's been bad.")
async def bad_bot(interaction: discord.Interaction):
    await bot_rate_bad(data_store, interaction)

# === Floof commands ===
@tree.command(name = "floof", description = "Add/remove floof from someone.")
async def floof(interaction: discord.Interaction, target: discord.Member, added_floof: int):
    await add_floof_entry(data_store, interaction, added_floof, target)

# === Duck Bucks commands ===
@tree.command(name = "duck-bucks", description = "Add/remove Duck Bucks from someone.")
async def duck_bucks(interaction: discord.Interaction, target: discord.Member, added_duck_bucks: int):
    await add_duck_bucks_entry(data_store, interaction, target, added_duck_bucks)

@tree.command(name = "get-duck-bucks", description = "See how many Duck Bucks someone has.")
async def get_duck_bucks(interaction: discord.Interaction, target: discord.Member):
    await get_duck_bucks_entry(data_store, interaction, target)

# === About commands ===
@tree.command(name = "about-sizebot", description = "Get info about SizeBot and the system it's running on.")
async def about_sizebot(interaction: discord.Interaction):
    await about_message(data_store, interaction)

# === Character commands ===
@tree.command(name = "scara", description = "Say a random Scaramouche elemental burst line.")
async def scara(interaction: discord.Interaction):
    await character_scara(data_store, interaction)

@tree.command(name = "zhongli", description = "Say a random Zhongli elemental burst line.")
async def zhongli(interaction: discord.Interaction):
    await character_zhongli(data_store, interaction)

@tree.command(name = "meow", description = "Say meow.")
async def meow(interaction: discord.Interaction):
    await character_cat(data_store, interaction)

# === Birthday commands ===
@tree.command(name = "birthdays", description = "Get a list of birthdays for a month (1-12, defaults to the current month).")
async def birthdays(interaction: discord.Interaction, month: int = -1):
    selected_month = month if month >= 1 and month <= 12 else date.today().month
    await birthday_monthly_list(data_store, interaction, selected_month)

@tree.command(name = "birthdays-sheet", description = "Get a CSV file of birthdays for a month (1-12. If no month specified, returns all months).")
async def birthdays_sheet(interaction: discord.Interaction, month: int = -1):
    if month == -1:
        await birthday_monthly_csv(data_store, interaction, -1)
    else:
        selected_month = month if month >= 1 and month <= 12 else date.today().month
        await birthday_monthly_csv(data_store, interaction, selected_month)

@tree.command(name = "birthdays-today", description = "Get a list of birthdays for today.")
async def birthdays_today(interaction: discord.Interaction):
    today = date.today()
    await birthday_daily_list(data_store, interaction, today.month, today.day)

@tree.command(name = "refresh-birthdays", description = "SizeBot will automatically check Google Sheets for updates daily, but this forces it to check now.")
async def refresh_birthdays(interaction: discord.Interaction):   
    log_message(f'Manually refreshing birthdays for "{interaction.guild.name}" ({interaction.guild.id})') 
    store_guild_birthdays(data_store, interaction.guild.id)
    await say(interaction, "Birthdays have been refreshed.", ephemeral = True)

@tree.command(name = "birthday-info", description = "Get the info for how to add/view birthdays (Google Sheets/Forms link).")
async def birthday_info(interaction: discord.Interaction):
    await birthday_get_info(data_store, interaction)

# === Mod-only commands ===
@tree.command(name = "update-guild-caches", description = "Mod-only: Update SizeBot guild and member caches.")
async def update_sizebot_guild_caches(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await say(interaction, f"Triggered cache updates for '{interaction.guild.name}'")
        await update_guild_cache(data_store, interaction.guild, client)
        await update_member_cache(data_store, interaction.guild)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "set-variable", description = "Mod-only: Set a server-specific variable to be replaced in SizeBot messages.")
async def set_sizebot_variable(interaction: discord.Interaction, variable_name: str, variable_value: str):
    if is_mod(interaction.user):
        await mod_set_sizebot_variable(data_store, interaction, variable_name, variable_value)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "delete-variable", description = "Mod-only: Delete a server-specific variable from SizeBot.")
async def delete_sizebot_variable(interaction: discord.Interaction, variable_name: str):
    if is_mod(interaction.user):
        await mod_delete_sizebot_variable(data_store, interaction, variable_name)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "set-welcome", description = "Mod-only: Set the SizeBot welcome image.")
async def set_sizebot_welcome(interaction: discord.Interaction, file: discord.Attachment):
    if is_mod(interaction.user):
        await mod_set_sizebot_welcome(data_store, interaction, file)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "add-character", description = "Mod-only: Add a SizeBot character.")
async def add_sizebot_character(interaction: discord.Interaction, name: str, avatar: discord.Attachment):
    if is_mod(interaction.user):
        await mod_add_sizebot_character(data_store, interaction, name, avatar)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "remove-character", description = "Mod-only: Remove a SizeBot character.")
async def remove_sizebot_character(interaction: discord.Interaction, name: str):
    if is_mod(interaction.user):
        await mod_remove_sizebot_character(data_store, interaction, name)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "list-characters", description = "Mod-only: List all SizeBot characters.")
async def list_sizebot_characters(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_list_sizebot_characters(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "set-welcome-messages", description = "Mod-only: Add SizeBot character welcome messages. Each message separated by \"|\".")
async def set_sizebot_character_welcome_messages(interaction: discord.Interaction, character_name: str, messages: str):
    if is_mod(interaction.user):
        await mod_set_sizebot_character_messages(data_store, interaction, character_name, "welcome", messages)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "remove-welcome-messages", description = "Mod-only: Remove all SizeBot character welcome messages.")
async def remove_sizebot_character_welcome_messages(interaction: discord.Interaction, character_name: str):
    if is_mod(interaction.user):
        await mod_delete_sizebot_character_messages(data_store, interaction, character_name, "welcome")
    else:
        await deny_non_mod(interaction)

@tree.command(name = "list-welcome-messages", description = "Mod-only: List all SizeBot character welcome messages.")
async def remove_sizebot_character_welcome_messages(interaction: discord.Interaction, character_name: str):
    if is_mod(interaction.user):
        await mod_list_sizebot_character_messages(data_store, interaction, character_name, "welcome")
    else:
        await deny_non_mod(interaction)

@tree.command(name = "reset-welcome", description = "Mod-only: Delete the custom SizeBot welcome image and reset to default.")
async def reset_sizebot_welcome(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_reset_sizebot_welcome(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "set-goodbye", description = "Mod-only: Set the SizeBot goodbye image.")
async def set_sizebot_goodbye(interaction: discord.Interaction, file: discord.Attachment):
    if is_mod(interaction.user):
        await mod_set_sizebot_goodbye(data_store, interaction, file)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "reset-goodbye", description = "Mod-only: Delete the custom SizeBot goodbye image and reset to default.")
async def reset_sizebot_goodbye(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_reset_sizebot_goodbye(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "set-sizeray-immunity-role", description = "Mod-only: Set the size ray immunity role.")
async def set_sizeray_immunity_role(interaction: discord.Interaction, role: discord.Role):
    if is_mod(interaction.user):
        await mod_set_sizeray_immunity_role(data_store, interaction, role)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "enable-welcome", description = "Mod-only: Allow SizeBot to send welcome messages.")
async def enable_sizebot_welcome(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_enable_sizebot_welcome(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "disable-welcome", description = "Mod-only: Don't allow SizeBot to send welcome messages.")
async def disable_sizebot_welcome(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_disable_sizebot_welcome(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "enable-welcome-characters", description = "Mod-only: Set SizeBot to send welcome messages with characters.")
async def enable_sizebot_welcome_characters(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_enable_sizebot_welcome_characters(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "disable-welcome-characters", description = "Mod-only: Turn off SizeBot welcome messages with characters.")
async def disable_sizebot_welcome_characters(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_disable_sizebot_welcome_characters(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "enable-goodbye", description = "Mod-only: Allow SizeBot to send goodbye messages.")
async def enable_sizebot_goodbye(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_enable_sizebot_goodbye(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "disable-goodbye", description = "Mod-only: Don't allow SizeBot to send goodbye messages.")
async def disable_sizebot_goodbye(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_disable_sizebot_goodbye(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "enable-birthdays", description = "Mod-only: Allow SizeBot to send birthday messages.")
async def enable_sizebot_birthdays(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_enable_sizebot_birthdays(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "disable-birthdays", description = "Mod-only: Don't allow SizeBot to send birthday messages.")
async def disable_sizebot_birthdays(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_disable_sizebot_birthdays(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "set-birthday-source", description = "Mod-only: Set the Google Sheets data source for birthdays.")
async def set_sizebot_birthday_source(interaction: discord.Interaction, sheets_key: str, name_column: str, birthday_column: str):
    if is_mod(interaction.user):
        await mod_set_birthday_source(data_store, interaction, sheets_key, name_column, birthday_column)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "set-birthday-info", description = "Mod-only: Set the info for how to add/view birthdays (Google Sheets/Forms link).")
async def set_sizebot_birthday_info(interaction: discord.Interaction, info: str):
    if is_mod(interaction.user):
        await mod_set_birthday_info(data_store, interaction, info)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "set-notify-channel", description = "Mod-only: Set the channel for SizeBot notifications (welcome, goodbye, etc..).")
async def set_sizebot_notifications_channel(interaction: discord.Interaction, channel: discord.channel.TextChannel):
    if is_mod(interaction.user):
        await mod_set_notifications_channel(data_store, interaction, channel)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "reset-notify-channel", description = "Mod-only: Reset the channel for SizeBot notifications (welcome, goodbye, etc..).")
async def reset_sizebot_notifications_channel(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_reset_notifications_channel(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "set-birthday-channel", description = "Mod-only: Set the channel for SizeBot birthday notifications.")
async def set_sizebot_birthday_channel(interaction: discord.Interaction, channel: discord.channel.TextChannel):
    if is_mod(interaction.user):
        await mod_set_birthdays_channel(data_store, interaction, channel)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "reset-birthday-channel", description = "Mod-only: Reset the channel for SizeBot birthday notifications.")
async def reset_sizebot_birthday_channel(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_reset_birthdays_channel(data_store, interaction)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "set-size-role", description = "Mod-only: Set a server-specific size role.")
async def set_sizebot_size_role(interaction: discord.Interaction, name: str, role: discord.Role):
    if is_mod(interaction.user):
        await mod_set_sizebot_size_role(data_store, interaction, name, role.id)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "delete-size-role", description = "Mod-only: Delete a server-specific size role from SizeBot.")
async def delete_sizebot_size_role(interaction: discord.Interaction, name: str):
    if is_mod(interaction.user):
        await mod_delete_sizebot_size_role(data_store, interaction, name)
    else:
        await deny_non_mod(interaction)

@tree.command(name = "list-size-roles", description = "Mod-only: List all server-specific size roles.")
async def list_sizebot_size_roles(interaction: discord.Interaction):
    if is_mod(interaction.user):
        await mod_list_sizebot_size_roles(data_store, interaction)
    else:
        await deny_non_mod(interaction)

# === Background tasks ===
# Check for birthdays every 12 hours
@tasks.loop(hours = 12)
async def load_birthdays_task():
    # Load birthdays for each guild
    for guild in client.guilds:
        store_guild_birthdays(data_store, guild.id)    
    log_message("Finished loading birthdays")
    await asyncio.sleep(0) # Return to caller

# Check for daily and monthly birthdays daily, running at 6AM MST
@tasks.loop(time = time(hour = 6, minute = 0, tzinfo = tz.gettz("MST")))
async def notify_birthdays_task():
    today = date.today()

    for guild in client.guilds:
        channel = get_birthday_notifications_channel(data_store, guild)
        if channel is not None and is_birthday_notify_enabled(data_store, guild):
            can_notify = channel.permissions_for(guild.me).send_messages
            # Send a monthly birthday list on the 1st of each month
            if today.day == 1 and can_notify:
                await birthday_monthly_list(data_store, channel, date.today().month)

            # Send a daily birthday list if there are any
            if can_notify:
                await birthday_daily_list(data_store, channel, today.month, today.day)

# Update status
@tasks.loop(hours = 1)
async def update_status_task():
    log_message("Updating the bot's status")
    activity = discord.Activity(type = discord.ActivityType.playing, name = f"Version {SIZEBOT_VERSION_STR}")
    await client.change_presence(status = discord.Status.online, activity = activity)
    log_message("Finished updating bot's status")

# Update guild and member caches every few hours
@tasks.loop(hours = 6)
async def update_caches_task():
    for guild in client.guilds:
        log_message(f'Updating caches for guild: "{guild.name}" (Id: {guild.id})')
        await update_guild_cache(data_store, guild, client)
        await update_member_cache(data_store, guild)
    log_message("Finished all cache updates")

# Update Duck Bucks every day
@tasks.loop(hours=24)
async def update_duck_bucks_task():
    for guild in client.guilds:
        log_message(f'Updating Duck Bucks for guild: "{guild.name}" (Id: {guild.id})')
        for member in guild.members:
            add_duck_bucks(data_store, guild.id, member.id, DUCK_BUCKS_DAILY)
    log_message("Finished all Duck Bucks updates")

# Remove temp size ray roles every 15 minutes
@tasks.loop(minutes = 15)
async def update_roles_task():    
    # Apply old roles and remove new ones
    log_message("Updating temp size ray roles")
    await apply_old_size_roles(data_store, client)
    log_message("Finished updating temp size ray roles")

# === Events ===
# When the bot has loaded
@client.event
async def on_ready():
    log_message(f"Logged in as {client.user} (Id: {client.user.id})")

    # Create empty folders, if they don't exist
    create_folder_if_missing("data/images/guild_custom/welcome")
    create_folder_if_missing("data/images/guild_custom/goodbye")
    create_folder_if_missing("data/images/guild_custom/character_images")
    create_folder_if_missing("data/images/temp")
    create_folder_if_missing("data/images/avatar_cache")
    create_folder_if_missing("data/images/server_avatar_cache")
    create_folder_if_missing("data/temp")

    # Start tasks
    load_birthdays_task.start()
    notify_birthdays_task.start()
    update_caches_task.start()
    update_roles_task.start()
    update_status_task.start()
    update_duck_bucks_task.start()

    # Get guilds and add the slash commands to them
    for guild in client.guilds:
        log_message(f"Syncing tree for guild {guild.id} ({guild.name})")
        tree.copy_global_to(guild = guild)
        await tree.sync(guild = guild)
    log_message("Finished all tree syncs")

# Automatically send a message when someone joins
@client.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    channel = get_notifications_channel(data_store, guild)
    if channel is not None and channel.permissions_for(guild.me).send_messages:
        await greeter_welcome(data_store, channel, member)
    else:
        log_message(f'No channel set with permissions that allow SizeBot to send welcome messages on the server "{guild.name}"')

    log_message(f'"{member.display_name}" has joined the server "{guild.name}"')

    # Update cache
    await update_member_cache(data_store, member.guild)

# Automatically send a message when someone leaves
@client.event
async def on_member_remove(member: discord.Member):
    guild = member.guild
    channel = get_notifications_channel(data_store, guild)
    if guild.me is not None and channel is not None: # Don't wanna have the bot try and send a goodbye message for itself
        if channel.permissions_for(guild.me).send_messages:
            await greeter_goodbye(data_store, channel, member)
        log_message(f'"{member.display_name}" has left the server "{guild.name}"')

# When the bot joins a new guild
@client.event
async def on_guild_join(guild: discord.Guild):
    log_message(f'Joined new guild: "{guild.name}" (Id: {guild.id})')
    # Sync the command tree with the new guild
    tree.copy_global_to(guild = guild)
    await tree.sync(guild = guild)
    log_message("Finish syncing commands to new guild")
    # Update caches
    await update_guild_cache(data_store, guild, client)
    await update_member_cache(data_store, guild)

# Launch the app
client.run(data_store.discord_bot_token)