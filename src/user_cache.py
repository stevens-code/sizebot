import discord

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
        return DiscordMember(id, guild_id, name, avatar, handle, timestamp)
    else: # No user in cache, fall back to calling server
        member = guild.get_member(user_id)

        if member is not None:
            guild_id = guild.id
            id = member.id
            name = member.display_name
            avatar = member.display_avatar
            handle = str(member)
            return DiscordMember(id, guild_id, name, avatar, handle, datetime.min)
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
            cursor.execute("INSERT INTO member_cache(guild, timestamp, id, name, avatar, handle) VALUES (?, ?, ?, ?, ?, ?)", (guild.id, datetime.now(), member.id, member.display_name, avatar_file, str(member)))
        except Exception as e:
            log_message("Error caching user:")   
            log_message(str(e))    

    # Commit changes
    data_store.db_connection.commit()  