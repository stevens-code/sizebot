import discord
import random
import asyncio
from PIL import Image

from variables import *
from data_store import *
from util import *
from user_cache import *
from log import *

async def greeter_welcome(data_store: DataStore, sender: Union[discord.Interaction, discord.TextChannel], target: discord.Member):
    """Says hello to a new user."""

    # If it's an automatic message and automatic messages are disabled
    if isinstance(sender, discord.TextChannel) and not is_greeter_welcome_enabled(data_store, sender.guild.id): 
        await asyncio.sleep(0) # Return to caller 

    # Send message
    await send_bot_thinking_response(sender)
    random_message = random.choice(data_store.greeter_welcome_messages)
    welcome_image = get_welcome_image(sender.guild.id)
    await say_with_image(sender, variable_replace(random_message, sender, data_store, target), welcome_image, followup = True)

async def greeter_goodbye(data_store: DataStore, sender: Union[discord.Interaction, discord.TextChannel], target: discord.Member):
    """Generates an image for a member leaving and attaches it to a message saying goodbye. If a custom image is specified, uses that instead."""

    # If it's an automatic message and automatic messages are disabled
    if isinstance(sender, discord.TextChannel) and not is_greeter_goodbye_enabled(data_store, sender.guild.id): 
        await asyncio.sleep(0) # Return to caller

    # Send message
    await send_bot_thinking_response(sender)
    
    try:
        # Grab member from cache if an automatic message
        member = None 
        if isinstance(sender, discord.TextChannel):
            member = await get_cached_member(data_store, sender.guild, target.id)
        else:
            avatar_file = get_avatar_name(target.display_avatar, sender.guild.id, target.id)
            member = DiscordMember(target.id, sender.guild.id, target.display_name, avatar_file, str(target), datetime.min)
            await target.display_avatar.save(member.avatar_path())
        
        random_message = variable_replace(random.choice(data_store.greeter_goodbye_messages), sender, data_store, target_no_ping = f"{member.name} ({format_mention(member.handle)})")
        # If a custom image is specified for the guild, use that instead
        custom_image_path = find_file_with_supported_ext("data/images/guild_custom/goodbye", f"{sender.guild.id}")
        if os.path.exists(custom_image_path):
            await say_with_image(sender, random_message, custom_image_path)
        else:
            # If no custom image, generate an image from the member's avatar and say goodbye
            with Image.open("data/images/fallen.png") as fallen:
                temp_image_path = f"data/images/temp/fallen_{target.id}.png"
                with Image.open(member.avatar_path()) as avatar:
                    resized_avatar = avatar.resize((536,536))
                    generated_image = Image.new("RGBA", (fallen.width, fallen.height))  
                    generated_image.paste(resized_avatar, (1525, 455))
                    generated_image.paste(fallen, (0, 0), fallen)
                    generated_image.save(temp_image_path)
                    await say_with_image(sender, random_message, temp_image_path, followup = True)

                # Delete the temp images
                os.remove(temp_image_path)
    except Exception as e:
        log_message("Error creating image:")   
        log_message(str(e))     
        await asyncio.sleep(0) # Return to caller

def get_welcome_image(guild_id: int):
    """Get a guild-specific welcome image. Returns the default image if none is found."""

    custom_image_path = find_file_with_supported_ext("data/images/guild_custom/welcome", f"{guild_id}")

    if os.path.exists(custom_image_path):
        return custom_image_path
    else:
        return "data/images/welcome.jpg"

def is_greeter_welcome_enabled(data_store: DataStore, guild_id: int) -> bool:
    """Check if the automatic greeter welcome message is enabled."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM greeter_disable_welcome WHERE guild = ?", (guild_id, ))    
    result = cursor.fetchone()

    # If there is not entry in the disable table, it's enabled
    return result is None

def is_greeter_goodbye_enabled(data_store: DataStore, guild_id: int) -> bool:
    """Check if the automatic greeter goodbye message is enabled."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM greeter_disable_goodbye WHERE guild = ?", (guild_id, ))    
    result = cursor.fetchone()

    # If there is not entry in the disable table, it's enabled
    return result is None