import discord
import random

from variables import *
from data_store import *
from util import *
from roles import *

# All of the command-related functions take 3 arguments:
# - data_store: the data_store that is defined in app_start. This contains all the data, including messages that are loaded from 
# the data/messages folder that start with "sizeray_". To add/remove/change the messages that are chosen at random for each
# sizeray function, change the corresponding file. Each message is on its own line.
# - interaction: the discord message's interaction context
# - target: the target member that the author is targeting

def sizeray_is_bot_targeted(interaction: discord.Interaction, target: discord.Member) -> bool:
    """Checks if the size ray is being targeted at the bot account itself."""

    return interaction.client.user == target

async def sizeray_malfunction(data_store: DataStore, interaction: discord.Interaction, target: discord.Member) -> str:
    """Generate a message for a size ray malfunction."""

    await send_bot_thinking_response(interaction)

    random_line = random.choice(data_store.malfunction_messages)
    rows = random_line.split("///")
    target_new_role = rows[0]
    author_new_role = rows[1]
    message = rows[2]
    message_format = "{{size_ray}} 🔥⚠ The size ray's *malfunctioned*!! ⚠🔥  ⚡✨\n{{size_ray}} " + message 

    if target_new_role != "nothing":
        await override_size_roles(data_store, target, interaction.guild, target_new_role)
    if author_new_role != "nothing":
        await override_size_roles(data_store, interaction.user, interaction.guild, author_new_role)

    sizeray_log_action(data_store, interaction.guild.id, "malfunction", target, interaction.user)   

    await say(interaction, variable_replace(message_format, interaction, data_store, target), followup = True)

async def sizeray_shrink(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Generate a message for shrinking a member."""

    if sizeray_is_bot_targeted(interaction, target):
        await sizeray_malfunction(data_store, interaction, target)
    elif sizeray_has_immunity(data_store, target):
        await sizeray_immunity_notice(data_store, interaction, target)
    else:
        await send_bot_thinking_response(interaction)
        random_message = random.choice(data_store.shrink_messages)
        message_format = "{{shrink_ray}} ✨⚡ {{target}} has been zapped by the shrink ray! " + random_message + " ⚡✨"
        sizeray_log_action(data_store, interaction.guild.id, "shrink", target, interaction.user)
        await override_size_roles(data_store, target, interaction.guild, "tiny")
        await say(interaction, variable_replace(message_format, interaction, data_store, target), followup = True)

async def sizeray_grow(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Generate a message for growing a member."""

    if sizeray_is_bot_targeted(interaction, target):
        await sizeray_malfunction(data_store, interaction, target)
    elif sizeray_has_immunity(data_store, target):
        await sizeray_immunity_notice(data_store, interaction, target)
    else:
        await send_bot_thinking_response(interaction)
        random_message = random.choice(data_store.grow_messages)
        message_format = "{{growth_ray}} ✨⚡ {{target}} has been zapped by the growth ray! " + random_message + " ⚡✨"   
        sizeray_log_action(data_store, interaction.guild.id, "grow", target, interaction.user)        
        await override_size_roles(data_store, target, interaction.guild, "giant")
        await say(interaction, variable_replace(message_format, interaction, data_store, target), followup = True)

async def sizeray_sizeray(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Generate a message for a random size ray operation."""

    if sizeray_is_bot_targeted(interaction, target):
        await sizeray_malfunction(data_store, interaction, target)
    elif sizeray_has_immunity(data_store, target):
        await sizeray_immunity_notice(data_store, interaction, target)
    else:
        # Include shrink and grow twice so they're more likely to occur than malfunction
        options = ['shrink', 'grow', 'shrink', 'grow', 'malfunction']
        random_option = random.choice(options)
        
        if random_option == 'shrink':
            await sizeray_shrink(data_store, interaction, target)
        elif random_option == 'grow':
            await sizeray_grow(data_store, interaction, target)
        else: # malfunction
            await sizeray_malfunction(data_store, interaction, target)

async def sizeray_immunity_notice(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Notify the author of a size ray action that the target can't be targeted because they have immunity."""

    await say(interaction, variable_replace("{{size_shield}} " + f"The size ray has no effect! {no_ping(target)} has size ray immunity!", interaction, data_store, target))

def sizeray_log_action(data_store: DataStore, guild_id: int, action: str, target: discord.Member, author: discord.Member):
        """Log a size ray action into the database."""

        cursor = data_store.db_connection.cursor()
        cursor.execute("INSERT INTO sizeray_actions(guild, timestamp, action, target, author) VALUES (?, ?, ?, ?, ?)", (guild_id, datetime.now(), action, target.id, author.id))
        data_store.db_connection.commit()

def sizeray_get_immunity_role(data_store: DataStore, guild_id: int) -> int:
    """Fetches the immunity role for a guild from the database."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM sizeray_immunity_roles WHERE guild = ?", (guild_id, ))    
    result = cursor.fetchone()
    if result is not None:
        return result[2]
    else:
        return None

def sizeray_has_immunity(data_store: DataStore, member: discord.Member) -> bool:
    """Check if a member has size ray immunity."""

    role_id = sizeray_get_immunity_role(data_store, member.guild.id)
    if role_id is not None:
        return has_role(member, role_id)
    else: # If no role is defined, no one has immunity
        return False

async def sizeray_toggle_immunity(data_store: DataStore, interaction: discord.Interaction) -> str:
    """Turn size ray immunity on or off for a user."""

    role_id = sizeray_get_immunity_role(data_store, interaction.guild.id)
    if role_id is None:
        await say(interaction, f"🚨 **Error:** Cannot toggle size ray immunity. The role is not defined for this server. 🚨")
    else:
        matching_role = interaction.guild.get_role(role_id)
        if has_role(interaction.user, role_id):
            # Turn it off if they have it
            await interaction.user.remove_roles(matching_role)
            await say(interaction, variable_replace("{{size_shield}}🔴 Your size ray immunity has been disabled {{author}}. 🔴{{size_shield}}", interaction, data_store))
        else:
            # Turn it on if they don't
            await interaction.user.add_roles(matching_role)
            await say(interaction, variable_replace("{{size_shield}}🟢 You now have size ray immunity, {{author}}. 🟢{{size_shield}}", interaction, data_store))
