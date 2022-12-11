import discord
import random
from PIL import Image

from variables import *
from data_store import *
from util import *

async def greeter_welcome(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Says hello to a new user."""
    
    welcome_image = get_welcome_image(interaction.guild.id)
    random_message = random.choice(data_store.greeter_welcome_messages);
    await say_with_image(interaction, variable_replace(random_message, interaction, data_store, target), welcome_image)

async def greeter_say_goodbye(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Generates an image for a member leaving and attaches it to a message saying goodbye. If a custom image is specified, uses that instead."""

    random_message = random.choice(data_store.greeter_goodbye_messages);

    try:
        # If a custom image is specified for the guild, use that instead
        custom_image_path = find_file_with_supported_ext("data/images/guild_custom/goodbye", f"{interaction.guild.id}")
        if os.path.exists(custom_image_path):
            await say_with_image(interaction, variable_replace(random_message, interaction, data_store, target), custom_image_path)
        else:
            # If no custom image, generate an image from the member's avatar and say goodbye
            with Image.open("data/images/fallen.png") as fallen:
                temp_image_path = f"data/images/temp/fallen_{target.id}.png"
                temp_avatar_path = f"data/images/temp/avatar_{target.id}.png"
                await target.avatar.save(temp_avatar_path)
                with Image.open(temp_avatar_path) as avatar:
                    resized_avatar = avatar.resize((536,536))
                    generated_image = Image.new("RGBA", (fallen.width, fallen.height))  
                    generated_image.paste(resized_avatar, (1525, 455))
                    generated_image.paste(fallen, (0, 0), fallen)
                    generated_image.save(temp_image_path)
                    await say_with_image(interaction, variable_replace(random_message, interaction, data_store, target), temp_image_path)

                # Delete the temp images
                os.remove(temp_image_path)
                os.remove(temp_avatar_path)
    except:
        print("Error creating image")
        await say(interaction, variable_replace(random_message, interaction, data_store, target))

def get_welcome_image(guild_id: int):
    """Get a guild-specific welcome image. Returns the default image if none is found."""

    custom_image_path = find_file_with_supported_ext("data/images/guild_custom/welcome", f"{guild_id}")

    if os.path.exists(custom_image_path):
        return custom_image_path
    else:
        return "data/images/welcome.jpg"