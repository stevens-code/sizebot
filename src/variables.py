import discord

from data_store import *
from util import *
from typing import Union

def get_guild_variables(data_store: DataStore, guild_id: int) -> dict:
    """A list of all variables for a guild."""

    results = {};

    variable_cursor = data_store.db_connection.execute(f"SELECT * from text_variables WHERE guild = ?", (guild_id, ))    
    variable_rows = variable_cursor.fetchall()
    for variable_row in variable_rows:
        variable_name = variable_row[2]
        variable_value = variable_row[3]
        results[variable_name] = variable_value
    
    return results

def variable_format(variable_name: str) -> str:
    """Format a variable name in the format of a SizeBot variable. For example, 'X' becomes '{{X}}'."""

    return "{{" + variable_name + "}}"

def variable_replace(text: str, sender: Union[discord.Interaction, discord.TextChannel], data_store: DataStore, target_user: discord.Member = None, target_no_ping: str = None):
    """Replaces context-specific variables in text."""

    result = text

    # Replace variables with guild-specific values
    variable_dict = get_guild_variables(data_store, sender.guild.id)
    for variable_name in variable_dict:
        result = result.replace(variable_format(variable_name), variable_dict[variable_name])

    # If there's any left over because the guild didn't have custom emojis for them,
    # replace them with the default emojis
    result = result.replace(variable_format("growth_ray"), "🔫⏫")
    result = result.replace(variable_format("shrink_ray"), "🔫⏬")
    result = result.replace(variable_format("size_ray"), "🔫")
    result = result.replace(variable_format("size_shield"), "🛡️")
    
    # Takes text and replaces variables {{target}} and {{author}} (if specified in function call) 
    # with strings mentioning the target and author members
    if target_user is not None:
        result = result.replace(variable_format("target"), target_user.mention)
    if isinstance(sender, discord.Interaction):
        result = result.replace(variable_format("author"), sender.user.mention)
    if target_no_ping is not None:
        result = result.replace(variable_format("target_no_ping"), target_no_ping)

    return result