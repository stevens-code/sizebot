import discord
import random

from variables import *
from data_store import *
from util import *

# All of the command-related functions take 3 arguments:
# - data_store: the data_store that is defined in app_start. This contains all the data, including messages that are loaded from 
# the data/messages folder that start with "sizeray_". To add/remove/change the messages that are chosen at random for each
# sizeray function, change the corresponding file. Each message is on its own line.
# - interaction: the discord message's interaction context
# - target: the target member that the author is targeting

def sizeray_is_bot_targeted(interaction: discord.Interaction, target: discord.Member):
    """Checks if the size ray is being targeted at the bot account itself."""

    return interaction.client.user == target

async def sizeray_malfunction(data_store: DataStore, interaction: discord.Interaction, target: discord.Member) -> str:
    """Generate a message for a size ray malfunction."""

    random_message = random.choice(data_store.malfunction_messages);
    message_format = "{{size_ray}} 🔥⚠ The size ray's *malfunctioned*!! ⚠🔥  ⚡✨\n{{size_ray}} " + random_message  
    sizeray_log_action(data_store, interaction.guild.id, "malfunction", target, interaction.user)   
    await say(interaction, variable_replace(message_format, interaction, data_store, target))

async def sizeray_shrink(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Generate a message for shrinking a member."""

    if sizeray_is_bot_targeted(interaction, target):
        await sizeray_malfunction(data_store, interaction, target)
    else:
        random_message = random.choice(data_store.shrink_messages);
        message_format = "{{shrink_ray}} ✨⚡ {{target}} has been zapped by the shrink ray! " + random_message + " ⚡✨"
        sizeray_log_action(data_store, interaction.guild.id, "shrink", target, interaction.user) 
        await say(interaction, variable_replace(message_format, interaction, data_store, target))

async def sizeray_grow(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Generate a message for growing a member."""

    if sizeray_is_bot_targeted(interaction, target):
        await sizeray_malfunction(data_store, interaction, target)
    else:
        random_message = random.choice(data_store.grow_messages);
        message_format = "{{growth_ray}} ✨⚡ {{target}} has been zapped by the growth ray! " + random_message + " ⚡✨"   
        sizeray_log_action(data_store, interaction.guild.id, "grow", target, interaction.user) 
        await say(interaction, variable_replace(message_format, interaction, data_store, target))

async def sizeray_sizeray(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Generate a message for a random size ray operation."""

    if sizeray_is_bot_targeted(interaction, target):
        await sizeray_malfunction(data_store, interaction, target)
    else:
        # Include shrink and grow twice so they're more likely to occur than malfunction
        options = ['shrink', 'grow', 'shrink', 'grow', 'malfunction']
        random_option = random.choice(options);
        
        if random_option == 'shrink':
            await sizeray_shrink(data_store, interaction, target)
        elif random_option == 'grow':
            await sizeray_grow(data_store, interaction, target)
        else: # malfunction
            await sizeray_malfunction(data_store, interaction, target)

async def sizeray_get_last_10(data_store: DataStore, interaction: discord.Interaction):
    lines = ["**The last 10 size ray actions were:**"];

    cursor = data_store.db_connection.execute(f"SELECT * from sizeray_actions WHERE guild = ? ORDER BY timestamp DESC LIMIT 10", (interaction.guild.id, ))    
    rows = cursor.fetchall()
    i = 1
    for row in rows:
        time = format_datetime(row[1])
        action = row[2]
        target = await get_user(interaction, row[3])
        author = await get_user(interaction, row[4])

        if author is not None and target is not None:
            if action == "malfunction":
                lines.append(f"({i}) The size ray *malfunctioned* on {no_ping(author)} while they were trying to use it on {no_ping(target)} at {time}")            
            elif action == "shrink":
                lines.append(f"({i}) {no_ping(author)} *shrank* {no_ping(target)} at {time}")     
            elif action == "grow":
                lines.append(f"({i}) {no_ping(author)} *grew* {no_ping(target)} at {time}")  
        else:
            lines.append(f"({i}) Sadly, the author or target of this action has left us")   
        
        i += 1
    
    await say(interaction, "\n".join(lines))

def sizeray_log_action(data_store: DataStore, guild_id: int, action: str, target: discord.Member, author: discord.Member):
        cursor=data_store.db_connection.cursor()
        cursor.execute("INSERT INTO sizeray_actions(guild, timestamp, action, target, author) VALUES (?, ?, ?, ?, ?)", (guild_id, datetime.now(), action, target.id, author.id))
        data_store.db_connection.commit()

def sizeray_has_shield(data_store: DataStore, member: discord.Member) -> bool:
    return False

def sizeray_toggle_shield(data_store: DataStore, interaction: discord.Interaction, target: discord.Member) -> str:
    """Turn the shield on for a user."""

    return ""