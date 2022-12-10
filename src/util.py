import discord
import os
from datetime import datetime

def format_datetime(time: datetime) -> str:
    return datetime.strftime(time, "%Y-%m-%d %H:%M:%S")

async def say(interaction: discord.Interaction, text: str):
    """Wrapper for sending a plain text message."""

    await interaction.response.send_message(text)

async def say_with_image(interaction: discord.Interaction, text: str, image_path: str):
    """Wrapper for sending a text message with an attached image."""

    file_name = os.path.basename(image_path)
    image_file = discord.File(image_path, filename=file_name)
    await interaction.response.send_message(text, file=image_file)