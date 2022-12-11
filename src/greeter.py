import discord
import random
from PIL import Image

from variables import *
from data_store import *
from util import *

async def greeter_welcome(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Says hello to a new user"""
    
    await say_with_image(interaction, f"Welcome {target.mention}!", "data/images/welcome.jpg")

async def greeter_say_goodbye(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Generates an image for a member leaving and attaches it to a message saying goodbye."""

    try:
        # Generate an image from the member's avatar and say goodbye
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
                await say_with_image(interaction, f"Goodbye {target.mention}!", temp_image_path)

            # Delete the temp images
            os.remove(temp_image_path)
            os.remove(temp_avatar_path)
    except:
        print("Error creating image")
        await say(interaction, f"Goodbye {target.mention}!")