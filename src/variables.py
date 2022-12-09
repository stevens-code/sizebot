import discord
from discord.ext.commands import Context

from data_store import *

# Replace variables in messages
def variable_replace(text: str, interaction: discord.Interaction, data_store: DataStore, target_user: discord.Member = None):
    """Replaces context-specific variables in text."""

    result = text

    # Replace variables with server-specific emojis
    emoji_cursor = data_store.db_connection.execute(f"SELECT * from emoji_variables WHERE guild = {interaction.guild.id}")    
    emoji_rows = emoji_cursor.fetchall()
    for emoji_row in emoji_rows:
        variable_name = emoji_row[3]
        emoji = emoji_row[2]
        result = result.replace(variable_name, emoji)
    emoji_cursor.close()

    # If there's any left over because the server didn't have custom emojis for them,
    # replace them with the default emojis
    result = result.replace("{{growth_ray}}", "🔫⏫")
    result = result.replace("{{shrink_ray}}", "🔫⏬")
    result = result.replace("{{size_ray}}", "🔫")
    
    # Takes text and replaces variables {{target}} and {{author}} (if specified in function call) 
    # with strings mentioning the target and author members
    if target_user is not None:
        result = result.replace("{{target}}", target_user.mention)
    result = result.replace("{{author}}", interaction.user.mention)

    return result