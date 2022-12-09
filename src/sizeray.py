import discord
import random

from variables import *
from data_store import *

# All of these functions take 3 arguments:
# - data_store: the data_store that is defined in app_start. This contains all the data, including messages that are loaded from 
# the data/messages folder that start with "sizeray_". To add/remove/change the messages that are chosen at random for each
# sizeray function, change the corresponding file. Each message is on its own line.
# - message_ctx: the discord message's context
# - target: the target member that the author is targeting

def sizeray_shrink(data_store: DataStore, message_ctx: Context, target: discord.Member) -> str:
    """Generate a message for shrinking a member."""

    random_message = random.choice(data_store.shrink_messages);
    message_format = "{{shrink_ray}} ✨⚡ {{target}} has been zapped by the shrink ray! " + random_message + " ⚡✨"
    return variable_replace(message_format, message_ctx, data_store, target)

def sizeray_grow(data_store: DataStore, message_ctx: Context, target: discord.Member) -> str:
    """Generate a message for growing a member."""

    random_message = random.choice(data_store.grow_messages);
    message_format = "{{growth_ray}} ✨⚡ {{target}} has been zapped by the growth ray! " + random_message + " ⚡✨"    
    return variable_replace(message_format, message_ctx, data_store, target)

def sizeray_malfunction(data_store: DataStore, message_ctx: Context, target: discord.Member) -> str:
    """Generate a message for a size ray malfunction."""

    random_message = random.choice(data_store.malfunction_messages);
    message_format = "{{size_ray}} 🔥⚠: The size ray's *malfunctioned*!! ⚠🔥  ⚡✨\n{{size_ray}} " + random_message    
    return variable_replace(message_format, message_ctx, data_store, target) 

def sizeray_sizeray(data_store: DataStore, message_ctx: Context, target: discord.Member) -> str:
    """Generate a message for a random size ray operation."""

    # Include shrink and grow twice so they're more likely to occur than malfunction
    options = ['shrink', 'grow', 'shrink', 'grow', 'malfunction']
    random_option = random.choice(options);
    
    if random_option == 'shrink':
        return sizeray_shrink(data_store, message_ctx, target)
    elif random_option == 'grow':
        return sizeray_grow(data_store, message_ctx, target)
    else: # malfunction
        return sizeray_malfunction(data_store, message_ctx, target)