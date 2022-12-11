import discord
import os
from datetime import datetime

# Various helper functions and constants
DISCORD_SUPPORTED_FILE_EXTS = [".jpg", ".jpeg", ".png", ".gif", ".gifv", ".webm", ".webp", ".mp4", ".wav", ".mp3", ".ogg"]

def format_datetime(time: datetime) -> str:
    """Formats a date and time to a clean format."""

    return datetime.strftime(time, f"%I:%M %p ({time.astimezone().tzname()}) on %m/%d/%Y")

async def say(interaction: discord.Interaction, text: str, is_followup = False):
    """Wrapper for sending a plain text message."""

    if is_followup:
        await interaction.followup.send(text)
    else:
        await interaction.response.send_message(text)

async def say_with_image(interaction: discord.Interaction, text: str, image_path: str, is_followup = False):
    """Wrapper for sending a text message with an attached image."""

    file_name = os.path.basename(image_path)
    image_file = discord.File(image_path, filename=file_name)
    if is_followup:
        await interaction.followup.send(text, file=image_file)
    else:
        await interaction.response.send_message(text, file=image_file)

async def get_user(interaction: discord.Integration, id: int) -> discord.Member:
    """Get a member by ID."""
    
    # Try to find member in cache first (way faster)
    found_member = interaction.guild.get_member(id)
    if found_member is not None:
        return found_member
    else:
        # If not, query Discord servers (slow)
        return await interaction.guild.fetch_member(id)

def no_ping(member: discord.Member):
    """Format a member name for a meesage where you don't want to ping them."""

    return f"***{member.name}***";

def find_file_with_supported_ext(folder: str, file_name: str) -> str:
    """Searches a folder for a file name that has one of Discord's supported file extensions."""

    for ext in DISCORD_SUPPORTED_FILE_EXTS:
        path = os.path.join(folder, f"{file_name}{ext}")
        if os.path.exists(path):
            return path

    return ""
