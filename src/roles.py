import discord

from variables import *
from data_store import *
from util import *

async def apply_old_size_roles(data_store: DataStore, client: discord.Client):
    """Apply the old size roles for a user"""
    
    # Get the new roles and delete them
    cursor = data_store.db_connection.execute(f"SELECT * FROM sizeray_new_roles")
    rows = cursor.fetchall()

    for row in rows:
        guild_id = row[0]
        member_id = row[2]
        guild = client.get_guild(guild_id)
        size_roles = get_size_roles(data_store, guild_id)
        member = guild.get_member(member_id)

        for size_role in size_roles:
            role = guild.get_role(size_role)
            if member is not None and role is not None:
                await member.remove_roles(role)

    # Get the old roles and apply them
    cursor = data_store.db_connection.execute(f"SELECT * FROM sizeray_old_roles")
    rows = cursor.fetchall()

    for row in rows:
        guild_id = row[0]
        member_id = row[2]
        role_id = row[3]
        guild = client.get_guild(guild_id)
        member = guild.get_member(member_id)
        role = guild.get_role(role_id)

        if member is not None and role is not None:
            await member.add_roles(role)

    # Clear old roles
    data_store.db_connection.execute(f"DELETE FROM sizeray_old_roles")
    data_store.db_connection.execute(f"DELETE FROM sizeray_new_roles")
    data_store.db_connection.commit()

def get_member_size_roles(data_store: DataStore, member: discord.Member) -> list[int]:
    """Gets all roles a member has that are defined as a size ray role"""

    matching_roles = []
    cursor = data_store.db_connection.execute(f"SELECT * FROM sizeray_roles")
    rows = cursor.fetchall()

    for row in rows:
        role_id = row[2]
        if member.get_role(role_id) is not None:
            matching_roles.append(role_id)

    return matching_roles

def get_size_roles(data_store: DataStore, guild_id: int) -> list[int]:
    """Gets all roles defined as a size role for a guild"""

    size_roles = []
    cursor = data_store.db_connection.execute(f"SELECT * FROM sizeray_roles WHERE guild = ?", (guild_id, ))
    rows = cursor.fetchall()

    for row in rows:
        role_id = row[2]
        size_roles.append(role_id)

    return size_roles

def get_size_role(data_store: DataStore, guild_id: int, role_name: str) -> int:
    """Get a size role id by name"""

    cursor = data_store.db_connection.execute(f"SELECT * FROM sizeray_roles WHERE guild = ? AND name = ?", (guild_id, role_name))    
    result = cursor.fetchone()
    if result is not None:
        role_id = result[2]
        return role_id
    else:
        return -1

def has_old_roles(data_store: DataStore, member: discord.Member, guild: discord.Guild):
    """Check if the user has existing old roles."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM sizeray_old_roles WHERE guild = ? AND member = ?", (guild.id, member.id))    
    result = cursor.fetchone()
    return result is not None

async def swap_size_roles(data_store: DataStore, member: discord.Member, guild: discord.Guild, old_roles: list[int], new_roles: list[int]):
    """Swap size roles for a member"""
    
    cursor = data_store.db_connection.cursor()
    existing_roles = has_old_roles(data_store, member, guild)
    # Add a dummy role with ID 0 if there are no roles (this is so has_old_roles() can know this has already been done)
    if len(old_roles) == 0:
        old_roles.append(0)
    # Loop through old roles and store them
    for old_role in old_roles:
        # Don't overwrite old roles if they exist
        if not existing_roles:
            cursor.execute("INSERT INTO sizeray_old_roles(guild, timestamp, member, role) VALUES (?, ?, ?, ?)", (guild.id, datetime.now(), member.id, old_role))
        role = guild.get_role(old_role)
        if role is not None:
            await member.remove_roles(role)
    # Store the new roles
    for new_role in new_roles:
        cursor.execute("INSERT INTO sizeray_new_roles(guild, timestamp, member, role) VALUES (?, ?, ?, ?)", (guild.id, datetime.now(), member.id, new_role))
        role = guild.get_role(new_role)
        if role is not None:
            await member.add_roles(role)
    data_store.db_connection.commit()

async def override_size_roles(data_store: DataStore, member: discord.Member, guild: discord.Guild, new_role_name: str):
    """Override all other size roles for a member with a new role if that role's name is found."""

    found_role = get_size_role(data_store, guild.id, new_role_name)
    if found_role != -1:
        old_roles = get_member_size_roles(data_store, member)
        await swap_size_roles(data_store, member, guild, old_roles, [found_role])