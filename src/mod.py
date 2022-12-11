import discord
import random

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