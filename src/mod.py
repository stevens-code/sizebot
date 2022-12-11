import discord
import random
import pathlib

from util import *
from data_store import *
from variables import *

# Mod-only commands
async def mod_set_sizebot_variable(data_store: DataStore, interaction: discord.Interaction, variable_name: str, variable_value: str = ""):
    """Set a variable in a guild's settings."""

    if variable_name in ["author", 'target']:
        await say(interaction, '🚨 **Error:** Cannot set that variable. The variables "author" and "target" are reserved for SizeBot. 🚨')
    else:
        cursor=data_store.db_connection.cursor()
        # Delete variable if it exists
        cursor.execute("DELETE FROM text_variables WHERE guild = ? AND variable_name = ?", (interaction.guild.id, variable_name))
        # Add variable
        cursor.execute("INSERT INTO text_variables(guild, timestamp, variable_name, variable_value) VALUES (?, ?, ?, ?)", (interaction.guild.id, datetime.now(), variable_name, variable_value))
        # Commit changes
        data_store.db_connection.commit()  

        # Respond with the current list of variables for the guild
        lines = [f'Variable "{variable_name}" set to "{variable_value}". You can now use it in message templates as {variable_format(variable_name)}"', "---", "**The server-specific variables can be used as:**"]
        lines.extend(get_variable_list(data_store, interaction.guild.id))
        await say(interaction, "\n".join(lines))

async def mod_delete_sizebot_variable(data_store: DataStore, interaction: discord.Interaction, variable_name: str):
    """Delete a variable from a guild's settings."""

    if variable_name in ["author", 'target']:
        await say(interaction, '🚨 **Error:** Cannot delete that variable. The variables "author" and "target" are reserved for SizeBot. 🚨')
    else:
        cursor=data_store.db_connection.cursor()
        # Delete variable
        cursor.execute("DELETE FROM text_variables WHERE guild = ? AND variable_name = ?", (interaction.guild.id, variable_name))
        # Commit changes
        data_store.db_connection.commit()  

        # Respond with the current list of variables for the guild
        lines = [f'Variable "{variable_name}" was deleted.', "---", "**The server-specific variables that remain are:**"]
        lines.extend(get_variable_list(data_store, interaction.guild.id))
        await say(interaction, "\n".join(lines))

def get_variable_list(data_store: DataStore, guild_id: int) -> list[str]:
    """Create a formated list of lines for a guild."""

    lines = []    
    variable_dict = get_guild_variables(data_store, guild_id)
    for variable_name in variable_dict:
        lines.append(f'*{variable_format(variable_name)}* for the value "{variable_dict[variable_name]}"')
    return lines

async def mod_set_sizebot_welcome(data_store: DataStore, interaction: discord.Interaction, file_attachment: discord.Attachment):
    """Set the SizeBot welcome image."""

    ext = pathlib.Path(file_attachment.filename).suffix.lower() 
    if ext not in DISCORD_SUPPORTED_FILE_EXTS:
        await say(interaction, f"🚨 **Error:** Not a supported file type. The supported types are: {DISCORD_SUPPORTED_FILE_EXTS}. 🚨")
    else:
        guild_id = f"{interaction.guild.id}"

        # Delete the old welcome image if it exists
        old_path = find_file_with_supported_ext("data/images/guild_custom/welcome/", guild_id)
        if os.path.exists(old_path):
            os.remove(old_path)

        await say(interaction, "Uploading new welcome image...")

        # Set the new one and send it back as a message
        file_path = f"data/images/guild_custom/welcome/{guild_id}{ext}"
        await file_attachment.save(file_path)
        await say_with_image(interaction, "Set new welcome image to:", file_path, True)

async def mod_reset_sizebot_welcome(data_store: DataStore, interaction: discord.Interaction):
    """Delete the custom SizeBot welcome image and reset to default."""

    old_path = find_file_with_supported_ext("data/images/guild_custom/welcome/", f"{interaction.guild.id}")
    if os.path.exists(old_path):
        os.remove(old_path)
    
    await say_with_image(interaction, "Reset welcome image back to default:", "data/images/welcome.jpg")

async def mod_set_sizebot_goodbye(data_store: DataStore, interaction: discord.Interaction, file_attachment: discord.Attachment):
    """Set the SizeBot goodbye image."""

    ext = pathlib.Path(file_attachment.filename).suffix.lower() 
    if ext not in DISCORD_SUPPORTED_FILE_EXTS:
        await say(interaction, f"🚨 **Error:** Not a supported file type. The supported types are: {DISCORD_SUPPORTED_FILE_EXTS}. 🚨")
    else:
        guild_id = f"{interaction.guild.id}"

        # Delete the old goodbye image if it exists
        old_path = find_file_with_supported_ext("data/images/guild_custom/goodbye/", guild_id)
        if os.path.exists(old_path):
            os.remove(old_path)

        await say(interaction, "Uploading new goodbye image...")

        # Set the new one and send it back as a message
        file_path = f"data/images/guild_custom/goodbye/{guild_id}{ext}"
        await file_attachment.save(file_path)
        await say_with_image(interaction, "Set new goodbye image to:", file_path, True)

async def mod_reset_sizebot_goodbye(data_store: DataStore, interaction: discord.Interaction):
    """Delete the custom SizeBot goodbye image and reset to default."""

    old_path = find_file_with_supported_ext("data/images/guild_custom/goodbye/", f"{interaction.guild.id}")
    if os.path.exists(old_path):
        os.remove(old_path)
    
    await say_with_image(interaction, "Reset goodbye image back to default:", "data/images/fallen.png")