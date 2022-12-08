import discord
import random

from variables import *
from data_store import *

# All of these functions take 3 arguments:
# - data_store: the data_store that is defined in main. This contains all the data including messages that are loaded from 
# the data/messages folder that start with "sizeray_". To add/remove/change the messages that are chosen at random for each
# sizeray function, change the corresponding file. Each message is on its own line.
# - target: the target member that the author is targeting
# - author: the member invoking the bot

def sizeray_shrink(data_store: DataStore, target: discord.Member, author: discord.Member) -> str:
    """Generate a message for shrinking a member"""

    random_message = variables_replace_target_author(random.choice(data_store.shrink_messages), target, author);
    return f":shrinkray:✨⚡ {target.mention} has been zapped by the shrink ray! {random_message} ⚡✨"

def sizeray_grow(data_store: DataStore, target: discord.Member, author: discord.Member) -> str:
    """Generate a message for growing a member"""

    random_message = variables_replace_target_author(random.choice(data_store.grow_messages), target, author);
    return f":growthray:✨⚡ {target.mention} has been zapped by the growth ray! {random_message} ⚡✨"

def sizeray_malfunction(data_store: DataStore, target: discord.Member, author: discord.Member) -> str:
    """Generate a message for a sizeray malfunction"""

    random_message = variables_replace_target_author(random.choice(data_store.malfunction_messages), target, author);    
    return f":sizeray:🔥⚠: The size ray's *malfunctioned*!! ⚠🔥  ⚡✨\n:sizeray: {random_message}"

def sizeray_sizeray(data_store: DataStore, target: discord.Member, author: discord.Member) -> str:
    """ Generate a message for a random sizeray operation  """

    # Include shrink and grow twice so they're more likely to occur than malfunction
    options = ['shrink', 'grow', 'shrink', 'grow', 'malfunction']
    random_option = random.choice(options);
    
    if random_option == 'shrink':
        return sizeray_shrink(data_store, target, author)
    elif random_option == 'grow':
        return sizeray_grow(data_store, target, author)
    else: # malfunction
        return sizeray_malfunction(data_store, target, author)