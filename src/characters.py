import discord
import random

from variables import *
from data_store import *
from util import *
from typing import List

async def character_scara(data_store: DataStore, interaction: discord.Interaction):
    """Say a random Scaramouche elemental burst line."""

    await send_bot_thinking_response(interaction)
    random_message = random.choice(data_store.character_scara_messages)
    await say_with_image(interaction, variable_replace(f"***{random_message}***", interaction, data_store), "data/images/scara.gif", followup = True)

async def character_zhongli(data_store: DataStore, interaction: discord.Interaction):
    """Say a random Zhongli elemental burst line."""

    await send_bot_thinking_response(interaction)
    random_message = random.choice(data_store.character_zhongli_messages)
    await say_with_image(interaction, variable_replace(f"***{random_message}***", interaction, data_store), "data/images/zhongli.gif", followup = True)

async def character_cat(data_store: DataStore, interaction: discord.Interaction):
    """Say a random cat sound."""

    await send_bot_thinking_response(interaction)
    random_message = random.choice(data_store.character_cat_messages)
    await say(interaction, variable_replace(f"*{random_message}*", interaction, data_store), followup = True)

def character_get_all(data_store: DataStore, guild_id: int) -> List[str]:
    """Gets all characters for a server."""

    cursor = data_store.db_connection.execute(f"SELECT * from characters WHERE guild = ?", (guild_id, ))    
    rows = cursor.fetchall()
    characters: List[str] = []
    for row in rows:
        name = row[2]
        characters.append(name)

    return characters

def character_get_random(data_store: DataStore, guild_id: int) -> str:
    """Gets a random character for a server."""

    all_characters = character_get_all(data_store, guild_id)
    if len(all_characters) == 0:
        return ""
    else:
        return random.choice(all_characters)

def character_get_messages(data_store: DataStore, guild_id: int, character: str, message_type: str) -> List[str]:
    """Gets all messages for a character."""

    cursor = data_store.db_connection.execute(f"SELECT * from character_messages WHERE guild = ? AND message_character = ? AND message_type = ?", (guild_id, character, message_type))    
    rows = cursor.fetchall()
    character_messages: List[str] = []
    for row in rows:
        message_value = row[4]
        character_messages.append(message_value)

    return character_messages

def character_get_random_message(data_store: DataStore, guild_id: int, character: str, message_type: str) -> str:
    """Gets a random message for a character."""

    all_messages = character_get_messages(data_store, guild_id, character, message_type)
    if len(all_messages) == 0:
        return ""
    else:
        return random.choice(all_messages)