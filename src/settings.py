import discord

from data_store import *

# Handles generic settings tables

def settings_get_channel(data_store: DataStore, guild: discord.Guild, key: str) -> discord.channel.TextChannel:
    """Gets a channel by key for a guild from the database. Returns none if it is not set."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM settings_channel WHERE guild = ? AND key = ?", (guild.id, key))    
    result = cursor.fetchone()
    if result is not None:
        value = result[3]
        return guild.get_channel(value)
    else:
        return None

def settings_set_channel(data_store: DataStore, guild: discord.Guild, key: str, value: discord.channel.TextChannel):
    """Sets a channel value by key for a guild from the database."""

    cursor = data_store.db_connection.cursor()
    # Delete entry if it exists
    cursor.execute("DELETE FROM settings_channel WHERE guild = ? AND key = ?", (guild.id, key))
    # Add a new entry
    cursor.execute("INSERT INTO settings_channel(guild, timestamp, key, value) VALUES (?, ?, ?, ?)", (guild.id, datetime.now(), key, value.id if value is not None else None))
    # Commit changes
    data_store.db_connection.commit()

def settings_get_text(data_store: DataStore, guild: discord.Guild, key: str) -> str:
    """Gets a text value by key for a guild from the database. Returns none if it is not set."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM settings_text WHERE guild = ? AND key = ?", (guild.id, key))    
    result = cursor.fetchone()
    if result is not None:
        value = result[3]
        return value
    else:
        return None

def settings_set_text(data_store: DataStore, guild: discord.Guild, key: str, value: str):
    """Sets a text value by key for a guild from the database."""

    cursor = data_store.db_connection.cursor()
    # Delete entry if it exists
    cursor.execute("DELETE FROM settings_text WHERE guild = ? AND key = ?", (guild.id, key))    
    # Add a new entry
    cursor.execute("INSERT INTO settings_text(guild, timestamp, key, value) VALUES (?, ?, ?, ?)", (guild.id, datetime.now(), key, value))
    # Commit changes
    data_store.db_connection.commit()

def settings_get_bool(data_store: DataStore, guild: discord.Guild, key: str) -> bool:
    """Gets a bool value by key for a guild from the database. Returns False if it is not set."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM settings_bool WHERE guild = ? AND key = ?", (guild.id, key))    
    result = cursor.fetchone()
    if result is not None:
        value = result[3]
        return value
    else:
        return False

def settings_set_bool(data_store: DataStore, guild: discord.Guild, key: str, value: bool):
    """Sets a bool value by key for a guild from the database."""

    cursor = data_store.db_connection.cursor()
    # Delete entry if it exists
    cursor.execute("DELETE FROM settings_bool WHERE guild = ? AND key = ?", (guild.id, key))    
    # Add a new entry
    cursor.execute("INSERT INTO settings_bool(guild, timestamp, key, value) VALUES (?, ?, ?, ?)", (guild.id, datetime.now(), key, value))
    # Commit changes
    data_store.db_connection.commit()

def settings_get_int(data_store: DataStore, guild: discord.Guild, key: str) -> int:
    """Gets a int value by key for a guild from the database. Returns none if it is not set."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM settings_int WHERE guild = ? AND key = ?", (guild.id, key))    
    result = cursor.fetchone()
    if result is not None:
        value = result[3]
        return value
    else:
        return None

def settings_set_int(data_store: DataStore, guild: discord.Guild, key: str, value: int):
    """Sets a int value by key for a guild from the database."""

    cursor = data_store.db_connection.cursor()
    # Delete entry if it exists
    cursor.execute("DELETE FROM settings_int WHERE guild = ? AND key = ?", (guild.id, key))    
    # Add a new entry
    cursor.execute("INSERT INTO settings_int(guild, timestamp, key, value) VALUES (?, ?, ?, ?)", (guild.id, datetime.now(), key, value))
    # Commit changes
    data_store.db_connection.commit()