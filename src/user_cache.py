import discord
from datetime import datetime, timezone

from data_store import *
from util import *
from log import *

async def get_cached_member(data_store: DataStore, guild: discord.Guild, user_id: int) -> DiscordMember:
    """Get a member from the cache, if none is available, call Discord's APIs."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM member_cache WHERE guild = ? AND id = ? ORDER BY timestamp DESC", (guild.id, user_id))
    result = cursor.fetchone()

    if result is not None:
        guild_id = result[0] 
        timestamp = result[1]
        id = result[2]
        name = result[3]
        avatar = result[4]
        handle = result[5]
        joined_at = result[6]
        return DiscordMember(id, guild_id, name, avatar, handle, joined_at, timestamp)
    else: # No user in cache, fall back to calling server
        member = guild.get_member(user_id)

        if member is not None:
            guild_id = guild.id
            id = member.id
            name = member.display_name
            avatar = member.display_avatar
            handle = str(member)
            joined_at = member.joined_at
            return DiscordMember(id, guild_id, name, avatar, handle, joined_at, datetime.min)
        else: # No user in cache or server
            return None

async def update_member_cache(data_store: DataStore, guild: discord.Guild):
    """Update the member cache for a server."""

    cursor = data_store.db_connection.cursor()

    for member in guild.members:
        try:
            # Get old cached member
            cached_member = await get_cached_member(data_store, guild, member.id)
            # Delete old cached member
            cursor.execute("DELETE FROM member_cache WHERE guild = ? AND id = ?", (guild.id, member.id))
            # Add new cached member
            avatar_file = get_avatar_name(member.display_avatar, guild.id, member.id)
            if not cached_member.avatar_exists() or cached_member.is_old():
                await member.display_avatar.save(f"data/images/avatar_cache/{avatar_file}")
            # microseconds cause SQLite to freak out when they're 0 and we don't care about them, so set them to a non-zero value
            joined_at = member.joined_at
            adjusted_joined_at = datetime(joined_at.year, joined_at.month, joined_at.day, joined_at.hour, joined_at.minute, joined_at.second, 999990)
            cursor.execute("INSERT INTO member_cache(guild, timestamp, id, name, avatar, handle, joined_at) VALUES (?, ?, ?, ?, ?, ?, ?)", (guild.id, datetime.now(), member.id, member.display_name, avatar_file, str(member), adjusted_joined_at))
        except Exception as e:
            log_message("Error caching user:")   
            log_message(str(e))    

    # Commit changes
    data_store.db_connection.commit()

async def get_cached_guild(data_store: DataStore, guild_id: int, client: discord.Client) -> DiscordGuild:
    """Get a guild from the cache, if none is available, call Discord's APIs."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM guild_cache WHERE guild = ? ORDER BY timestamp DESC", (guild_id, ))
    result = cursor.fetchone()

    if result is not None:
        guild_id = result[0] 
        timestamp = result[1]
        name = result[2]
        avatar = result[3]
        return DiscordGuild(guild_id, name, avatar, timestamp)
    else: # No guild in cache, fall back to API
        guild = client.get_guild(guild_id)

        if guild is not None:
            guild_id = guild.id
            name = guild.name
            avatar = get_guild_avatar_name(guild.icon, guild.id)
            return DiscordGuild(guild_id, name, avatar, datetime.min)
        else: # No user in cache or server
            return None

async def update_guild_cache(data_store: DataStore, guild: discord.Guild, client: discord.Client):
    """Update the guild cache for a guild."""

    cursor = data_store.db_connection.cursor()

    try:
        # Get old cached guild
        cached_guild = await get_cached_guild(data_store, guild.id, client)
        # Delete old cached guild
        cursor.execute("DELETE FROM guild_cache WHERE guild = ?", (guild.id, ))
        # Add new cached guild
        avatar_file = get_guild_avatar_name(guild.icon, guild.id)
        if not cached_guild.avatar_exists() or cached_guild.is_old():
            await guild.icon.save(f"data/images/server_avatar_cache/{avatar_file}")
        cursor.execute("INSERT INTO guild_cache(guild, timestamp, name, avatar) VALUES (?, ?, ?, ?)", (guild.id, datetime.now(), guild.name, avatar_file))
    except Exception as e:
        log_message("Error caching guild:")   
        log_message(str(e))    

    # Commit changes
    data_store.db_connection.commit()