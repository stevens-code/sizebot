import discord
import pathlib
import pandas

from util import *
from data_store import *
from variables import *
from birthday import *
from roles import *
from settings import *

# Mod-only commands
async def mod_set_sizebot_variable(data_store: DataStore, interaction: discord.Interaction, variable_name: str, variable_value: str = ""):
    """Set a variable in a guild's settings."""

    if variable_name in ["author", 'target']:
        await say(interaction, '🚨 **Error:** Cannot set that variable. The variables "author" and "target" are reserved for SizeBot. 🚨', ephemeral = True)
    else:
        cursor = data_store.db_connection.cursor()
        # Delete variable if it exists
        cursor.execute("DELETE FROM text_variables WHERE guild = ? AND variable_name = ?", (interaction.guild.id, variable_name))
        # Add variable
        cursor.execute("INSERT INTO text_variables(guild, timestamp, variable_name, variable_value) VALUES (?, ?, ?, ?)", (interaction.guild.id, datetime.now(), variable_name, variable_value))
        # Commit changes
        data_store.db_connection.commit()  

        # Respond with the current list of variables for the guild
        lines = [f'Variable "{variable_name}" set to "{variable_value}". You can now use it in message templates as {variable_format(variable_name)}"', "---", "**The server-specific variables can be used as:**"]
        lines.extend(get_variable_list(data_store, interaction.guild.id))
        await say(interaction, "\n".join(lines), ephemeral = True)

async def mod_delete_sizebot_variable(data_store: DataStore, interaction: discord.Interaction, variable_name: str):
    """Delete a variable from a guild's settings."""

    if variable_name in ["author", 'target']:
        await say(interaction, '🚨 **Error:** Cannot delete that variable. The variables "author" and "target" are reserved for SizeBot. 🚨', ephemeral = True)
    else:
        cursor = data_store.db_connection.cursor()
        # Delete variable
        cursor.execute("DELETE FROM text_variables WHERE guild = ? AND variable_name = ?", (interaction.guild.id, variable_name))
        # Commit changes
        data_store.db_connection.commit()  

        # Respond with the current list of variables for the guild
        lines = [f'Variable "{variable_name}" was deleted.', "---", "**The server-specific variables that remain are:**"]
        lines.extend(get_variable_list(data_store, interaction.guild.id))
        await say(interaction, "\n".join(lines), ephemeral = True)

def get_variable_list(data_store: DataStore, guild_id: int) -> list[str]:
    """Create a formatted list of variables for a guild."""

    lines = []    
    variable_dict = get_guild_variables(data_store, guild_id)
    for variable_name in variable_dict:
        lines.append(f'*{variable_format(variable_name)}* for the value "{variable_dict[variable_name]}"')
    return lines

async def mod_set_sizebot_welcome(data_store: DataStore, interaction: discord.Interaction, file_attachment: discord.Attachment):
    """Set the SizeBot welcome image."""

    ext = pathlib.Path(file_attachment.filename).suffix.lower() 
    if ext not in DISCORD_SUPPORTED_FILE_EXTS:
        await say(interaction, f"🚨 **Error:** Not a supported file type. The supported types are: {DISCORD_SUPPORTED_FILE_EXTS}. 🚨", ephemeral = True)
    else:
        guild_id = f"{interaction.guild.id}"

        # Delete the old welcome image if it exists
        old_path = find_file_with_supported_ext("data/images/guild_custom/welcome/", guild_id)
        if os.path.exists(old_path):
            os.remove(old_path)

        await say(interaction, "Uploading new welcome image...", ephemeral = True)

        # Set the new one and send it back as a message
        file_path = f"data/images/guild_custom/welcome/{guild_id}{ext}"
        await file_attachment.save(file_path)
        await say_with_image(interaction, "Set new welcome image to:", file_path, followup = True, ephemeral = True)

async def mod_add_sizebot_character(data_store: DataStore, interaction: discord.Interaction, name: str, avatar: discord.Attachment):
    """Set the SizeBot welcome image."""

    ext = pathlib.Path(avatar.filename).suffix.lower() 
    if ext not in DISCORD_SUPPORTED_FILE_EXTS:
        await say(interaction, f"🚨 **Error:** Not a supported file type. The supported types are: {DISCORD_SUPPORTED_FILE_EXTS}. 🚨", ephemeral = True)
    else:
        guild_id = f"{interaction.guild.id}"

        await say(interaction, "Adding character...", ephemeral = True)

        # Save character to DB
        cursor = data_store.db_connection.cursor()
        # Delete character if they exist 
        cursor.execute("DELETE FROM characters WHERE guild = ? AND character_name = ?", (guild_id, name))
        # Add character
        cursor.execute("INSERT INTO characters(guild, timestamp, character_name) VALUES (?, ?, ?)", (interaction.guild.id, datetime.now(), name))
        # Commit changes
        data_store.db_connection.commit()  

        # Delete the old character image if it exists
        old_path = find_file_with_supported_ext("data/images/guild_custom/character_images/", f"{guild_id}_welcome_{name}")
        if os.path.exists(old_path):
            os.remove(old_path)

        # Set the new one and send it back as a message
        file_path = f"data/images/guild_custom/character_images/{guild_id}_welcome_{name}{ext}"
        await avatar.save(file_path)
        await say_with_image(interaction, f"Added character with the name \"{name}\":", file_path, followup = True, ephemeral = True)

async def mod_remove_sizebot_character(data_store: DataStore, interaction: discord.Interaction, name: str):
    """Remove a SizeBot character."""

    guild_id = f"{interaction.guild.id}"

    await say(interaction, "Removing character...", ephemeral = True)

    # Delete character from DB
    cursor = data_store.db_connection.cursor()
    # Delete character
    cursor.execute("DELETE FROM characters WHERE guild = ? AND character_name = ?", (guild_id, name))
    # Delete all their messages
    cursor.execute("DELETE FROM character_messages WHERE guild = ? AND message_character = ?", (interaction.guild.id, name))
    # Commit changes
    data_store.db_connection.commit()  

    # Delete the old character image
    old_path = find_file_with_supported_ext("data/images/guild_custom/character_images/", f"{guild_id}_welcome_{name}")
    if os.path.exists(old_path):
        os.remove(old_path)

    # Set the new one and send it back as a message
    await say(interaction, f"Removed character with the name \"{name}\":", followup = True, ephemeral = True)

async def mod_list_sizebot_characters(data_store: DataStore, interaction: discord.Interaction) -> list[str]:
    """List the characters for a guild."""

    lines = ["**The characters for this server are:**"]
    cursor = data_store.db_connection.execute(f"SELECT * FROM characters WHERE guild = ?", (interaction.guild.id, ))
    rows = cursor.fetchall()

    for row in rows:
        character_name = row[2]
        lines.append(character_name)

    if len(rows) == 0:
        lines.append("*There are no characters defined for this server.*")

    await say(interaction, "\n".join(lines), ephemeral = True)

async def mod_set_sizebot_character_messages(data_store: DataStore, interaction: discord.Interaction, character_name: str, message_type: str, messages: str):
    """Add SizeBot character messages. Each message separated by |."""
    lines = [f"**The character messages for \"{character_name}\" in this server are:**"]
    split_messages = messages.split("|")
    await say(interaction, "Adding character messages...", ephemeral = True)

    # Save character message to DB
    cursor = data_store.db_connection.cursor()
    # Delete character messages if they exist
    cursor.execute("DELETE FROM character_messages WHERE guild = ? AND message_character = ? AND message_type = ?", (interaction.guild.id, character_name, message_type))
    # Add character messages
    for message in split_messages:
        lines.append(f"\"{message}\"")
        cursor.execute("INSERT INTO character_messages(guild, timestamp, message_type, message_character, message_value) VALUES (?, ?, ?, ?, ?)", (interaction.guild.id, datetime.now(), message_type, character_name, message))
    # Commit changes
    data_store.db_connection.commit()

    await say(interaction, "\n".join(lines), ephemeral = True, followup = True)

async def mod_delete_sizebot_character_messages(data_store: DataStore, interaction: discord.Interaction, character_name: str, message_type: str):
    """Delete SizeBot character messages."""
    await say(interaction, "Removing character messages...", ephemeral = True)

    cursor = data_store.db_connection.cursor()
    # Delete character messages
    cursor.execute("DELETE FROM character_messages WHERE guild = ? AND message_character = ? AND message_type = ?", (interaction.guild.id, character_name, message_type))
    # Commit changes
    data_store.db_connection.commit()

    await say(interaction, f"Character messages for \"{character_name}\" removed.", ephemeral = True, followup = True)

async def mod_list_sizebot_character_messages(data_store: DataStore, interaction: discord.Interaction, character_name: str, message_type: str):
    """List SizeBot character messages."""
    lines = [f"**The character messages for \"{character_name}\" in this server are:**"]
    messages = []

    # Save character to DB
    cursor = data_store.db_connection.cursor()
    # Get the character messages
    cursor = data_store.db_connection.execute("SELECT * FROM character_messages WHERE guild = ? AND message_character = ? AND message_type = ?", (interaction.guild.id, character_name, message_type))
    # Add character messages
    rows = cursor.fetchall()
    for row in rows:
        message = row[4]
        messages.append(message)
        lines.append(f"\"{message}\"")
    
    if len(rows) == 0:
        lines.append("*There are no character messages defined on this server for this character*")
    else:
        # Add in the message formatted so that it can be edited
        lines.append("\n Copy this and modify it when editing using /set-welcome-messages to change the messages for this character:")
        joined_messages = "|".join(messages)
        lines.append(f"`{joined_messages}`")

    await say(interaction, "\n".join(lines), ephemeral = True)

async def mod_reset_sizebot_welcome(data_store: DataStore, interaction: discord.Interaction):
    """Delete the custom SizeBot welcome image and reset to default."""

    old_path = find_file_with_supported_ext("data/images/guild_custom/welcome/", f"{interaction.guild.id}")
    if os.path.exists(old_path):
        os.remove(old_path)
    
    await say_with_image(interaction, "Reset welcome image back to default:", "data/images/welcome.jpg", ephemeral = True)

async def mod_set_sizebot_goodbye(data_store: DataStore, interaction: discord.Interaction, file_attachment: discord.Attachment):
    """Set the SizeBot goodbye image."""

    ext = pathlib.Path(file_attachment.filename).suffix.lower() 
    if ext not in DISCORD_SUPPORTED_FILE_EXTS:
        await say(interaction, f"🚨 **Error:** Not a supported file type. The supported types are: {DISCORD_SUPPORTED_FILE_EXTS}. 🚨", ephemeral = True)
    else:
        guild_id = f"{interaction.guild.id}"

        # Delete the old goodbye image if it exists
        old_path = find_file_with_supported_ext("data/images/guild_custom/goodbye/", guild_id)
        if os.path.exists(old_path):
            os.remove(old_path)

        await say(interaction, "Uploading new goodbye image...", ephemeral = True)

        # Set the new one and send it back as a message
        file_path = f"data/images/guild_custom/goodbye/{guild_id}{ext}"
        await file_attachment.save(file_path)
        await say_with_image(interaction, "Set new goodbye image to:", file_path, followup = True, ephemeral = True)

async def mod_reset_sizebot_goodbye(data_store: DataStore, interaction: discord.Interaction):
    """Delete the custom SizeBot goodbye image and reset to default."""

    old_path = find_file_with_supported_ext("data/images/guild_custom/goodbye/", f"{interaction.guild.id}")
    if os.path.exists(old_path):
        os.remove(old_path)
    
    await say_with_image(interaction, "Reset goodbye image back to default:", "data/images/fallen.png", ephemeral = True)

async def mod_set_sizeray_immunity_role(data_store: DataStore, interaction: discord.Interaction, role: discord.Role):
    """Set the size ray immunity role for a guild."""

    cursor = data_store.db_connection.cursor()
    # Delete role if it exists 
    cursor.execute("DELETE FROM sizeray_immunity_roles WHERE guild = ?", (interaction.guild.id, ))
    # Add role
    cursor.execute("INSERT INTO sizeray_immunity_roles(guild, timestamp, role) VALUES (?, ?, ?)", (interaction.guild.id, datetime.now(), role.id))
    # Commit changes
    data_store.db_connection.commit()  

    # Respond with the size ray immunity role for the guild
    await say(interaction, f"The role for size ray immunity now is ***{role.name}***", ephemeral = True)

async def mod_enable_sizebot_welcome(data_store: DataStore, interaction: discord.Interaction):
    """Allow SizeBot to send welcome messages."""

    settings_set_bool(data_store, interaction.guild, "disable_welcome", False)  
    await say(interaction, "The automatic welcome message is now enabled for this server.", ephemeral = True)

async def mod_disable_sizebot_welcome(data_store: DataStore, interaction: discord.Interaction):
    """Don't allow SizeBot to send welcome messages."""

    settings_set_bool(data_store, interaction.guild, "disable_welcome", True)
    await say(interaction, "The automatic welcome message is now disabled for this server.", ephemeral = True)

async def mod_enable_sizebot_welcome_characters(data_store: DataStore, interaction: discord.Interaction):
    """Set SizeBot to send welcome messages with characters."""

    settings_set_bool(data_store, interaction.guild, "welcome_message_characters", True)  
    await say(interaction, "Welcome message characters are now enabled for this server.", ephemeral = True)

async def mod_disable_sizebot_welcome_characters(data_store: DataStore, interaction: discord.Interaction):
    """Turn off SizeBot welcome messages with characters."""

    settings_set_bool(data_store, interaction.guild, "welcome_message_characters", False)
    await say(interaction, "Welcome message characters are now disabled for this server.", ephemeral = True)

async def mod_enable_sizebot_goodbye(data_store: DataStore, interaction: discord.Interaction):
    """Allow SizeBot to send goodbye messages."""

    settings_set_bool(data_store, interaction.guild, "disable_goodbye", False)
    await say(interaction, "The automatic goodbye message is now enabled for this server.", ephemeral = True)

async def mod_disable_sizebot_goodbye(data_store: DataStore, interaction: discord.Interaction):
    """Don't allow SizeBot to send goodbye messages."""

    settings_set_bool(data_store, interaction.guild, "disable_goodbye", True)
    await say(interaction, "The automatic goodbye message is now disabled for this server.", ephemeral = True)

async def mod_enable_sizebot_birthdays(data_store: DataStore, interaction: discord.Interaction):
    """Allow SizeBot to send birthday messages."""

    settings_set_bool(data_store, interaction.guild, "disable_birthdays", False)
    await say(interaction, "The automatic birthday message is now enabled for this server.", ephemeral = True)

async def mod_disable_sizebot_birthdays(data_store: DataStore, interaction: discord.Interaction):
    """Don't allow SizeBot to send birthday messages."""

    settings_set_bool(data_store, interaction.guild, "disable_birthdays", True)
    await say(interaction, "The automatic birthday message is now disabled for this server.", ephemeral = True)

async def mod_set_birthday_source(data_store: DataStore, interaction: discord.Interaction, sheets_key: str, name_column: str, birthday_column: str):
    """Set the birthday data source in a guild's settings."""

    url = f"https://docs.google.com/spreadsheets/d/{sheets_key}/export?format=csv"
    await say(interaction, f'Setting birthday data source to "{url}"...', ephemeral = True)

    try:
        # Try and load the data, it will throw an exception if invalid
        data = pandas.read_csv(url, usecols= [name_column, birthday_column])  

        cursor = data_store.db_connection.cursor()
        # Delete if it exists
        cursor.execute("DELETE FROM birthday_settings WHERE guild = ?", (interaction.guild.id, ))
        # Add birthday settings
        cursor.execute("INSERT INTO birthday_settings(guild, timestamp, sheets_key, sheets_name_column, sheets_birthday_column) VALUES (?, ?, ?, ?, ?)", (interaction.guild.id, datetime.now(), sheets_key, name_column, birthday_column))
        # Commit changes
        data_store.db_connection.commit()  

        # Respond with the current list of birthdays for the guild
        store_guild_birthdays(data_store, interaction.guild.id)
        birthday_list = get_birthday_list(data_store, interaction.guild.id)
        lines = [f'SizeBot will now download birthdays from "{url}".', "---", "**The birthdays on this server are:**"]
        lines.extend(birthday_list)
        result = "\n".join(lines)
        await say(interaction, result + "...", ephemeral = True, followup = True)
    except:
        await say(interaction, f'🚨 **Error:** The url "{url}" does not return data that SizeBot can use. 🚨', ephemeral = True, followup = True)

async def mod_set_birthday_info(data_store: DataStore, interaction: discord.Interaction, info: str):
    """Set message to send members about how to add their birthdays."""

    cursor = data_store.db_connection.cursor()
    # Delete if it exists 
    cursor.execute("DELETE FROM birthday_source_info WHERE guild = ?", (interaction.guild.id, ))
    # Add the info
    cursor.execute("INSERT INTO birthday_source_info(guild, timestamp, info) VALUES (?, ?, ?)", (interaction.guild.id, datetime.now(), info))
    # Commit changes
    data_store.db_connection.commit()  

    # Respond with the new channel name
    await say(interaction, f"The info that appears when running /birthday-info is: \n {info}", ephemeral = True)

async def mod_set_notifications_channel(data_store: DataStore, interaction: discord.Interaction, channel: discord.channel.TextChannel):
    """Set the notifications channel for SizeBot."""

    cursor = data_store.db_connection.cursor()
    # Delete channel setting if it exists 
    cursor.execute("DELETE FROM notifications_channel WHERE guild = ?", (interaction.guild.id, ))
    # Add channel
    cursor.execute("INSERT INTO notifications_channel(guild, timestamp, channel) VALUES (?, ?, ?)", (interaction.guild.id, datetime.now(), channel.id))
    # Commit changes
    data_store.db_connection.commit()  

    # Respond with the new channel name
    await say(interaction, f"The channel for SizeBot notifications is now ***{channel.name}***", ephemeral = True)

async def mod_reset_notifications_channel(data_store: DataStore, interaction: discord.Interaction):
    """Reset the notifications channel for SizeBot back to the Discord default notifications channel."""

    cursor = data_store.db_connection.cursor()
    # Delete channel setting if it exists 
    cursor.execute("DELETE FROM notifications_channel WHERE guild = ?", (interaction.guild.id, ))
    # Commit changes
    data_store.db_connection.commit()  

    # Respond with the new channel name
    await say(interaction, f"The channel for SizeBot notifications is now reset to Discord's default notification channel.", ephemeral = True)

async def mod_set_birthdays_channel(data_store: DataStore, interaction: discord.Interaction, channel: discord.channel.TextChannel):
    """Set the birthday notifications channel for SizeBot."""

    # Set the channel
    settings_set_channel(data_store, interaction.guild, "birthdays_channel", channel)
    # Respond with the new channel name
    await say(interaction, f"The channel for SizeBot birthday notifications is now ***{channel.name}***", ephemeral = True)

async def mod_reset_birthdays_channel(data_store: DataStore, interaction: discord.Interaction):
    """Reset the birthday notifications channel for SizeBot back to the Discord default notifications channel."""

    settings_set_channel(data_store, interaction.guild, "birthdays_channel", None)
    await say(interaction, f"The channel for SizeBot birthday notifications is now reset to Discord's default notification channel.", ephemeral = True)

async def mod_set_sizebot_size_role(data_store: DataStore, interaction: discord.Interaction, role_name: str, role_id: int):
    """Set a size ray role in a guild's settings."""

    cursor = data_store.db_connection.cursor()
    # Delete role if it exists
    cursor.execute("DELETE FROM sizeray_roles WHERE guild = ? AND name = ?", (interaction.guild.id, role_name))
    # Add role
    cursor.execute("INSERT INTO sizeray_roles(guild, timestamp, id, name) VALUES (?, ?, ?, ?)", (interaction.guild.id, datetime.now(), role_id, role_name))
    # Commit changes
    data_store.db_connection.commit()  

    # Respond with the current list of variables for the guild
    await say(interaction, f'Role "{role_name}" set to id "{role_id}".', ephemeral = True)

async def mod_delete_sizebot_size_role(data_store: DataStore, interaction: discord.Interaction, role_name: str):
    """Delete a size ray role from a guild's settings."""

    cursor = data_store.db_connection.cursor()
    # Delete role
    cursor.execute("DELETE FROM sizeray_roles WHERE guild = ? AND name = ?", (interaction.guild.id, role_name))
    # Commit changes
    data_store.db_connection.commit()  

    await say(interaction, f'The role with name "{role_name}" was deleted".', ephemeral = True)

async def mod_list_sizebot_size_roles(data_store: DataStore, interaction: discord.Interaction) -> list[str]:
    """List the size roles for a guild."""

    lines = ["**The size roles are:**"]
    cursor = data_store.db_connection.execute(f"SELECT * FROM sizeray_roles WHERE guild = ?", (interaction.guild.id, ))
    rows = cursor.fetchall()

    for row in rows:
        role_id = row[2]
        role_name = row[3]
        lines.append(f'*"{role_name}"* with the id "{role_id}"')

    await say(interaction, "\n".join(lines), ephemeral = True)