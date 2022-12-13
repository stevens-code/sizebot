import discord
import os
from datetime import datetime
from typing import Union

# Various helper functions and constants
DISCORD_SUPPORTED_FILE_EXTS = [".jpg", ".jpeg", ".png", ".gif", ".gifv", ".webm", ".webp", ".mp4", ".wav", ".mp3", ".ogg"]

def format_datetime(time: datetime) -> str:
    """Formats a date and time to a clean format."""

    return datetime.strftime(time, f"%I:%M %p ({time.astimezone().tzname()}) on %m/%d/%Y")

async def say(sender: Union[discord.Interaction, discord.TextChannel], text: str, is_followup = False):
    """Wrapper for sending a plain text message."""

    if isinstance(sender, discord.Interaction):
        if is_followup:
            await sender.followup.send(text)
        else:
            await sender.response.send_message(text)
    else:
        await sender.send(text)


async def say_with_image(sender: Union[discord.Interaction, discord.TextChannel], text: str, image_path: str, is_followup = False):
    """Wrapper for sending a text message with an attached image."""

    file_name = os.path.basename(image_path)
    image_file = discord.File(image_path, filename=file_name)
    if isinstance(sender, discord.Interaction):
        if is_followup:
            await sender.followup.send(text, file = image_file)
        else:
            await sender.response.send_message(text, file = image_file)
    else:
        await sender.send(text, file = image_file)

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

def has_role(member: discord.Member, role_id: int) -> bool:
    """Check if a member has a role."""

    for role in member.roles:
        if role.id == role_id:
            return True
    
    return False

def create_folder_if_missing(folder: str):
    """Create a folder if it doesn't already exist."""

    if not os.path.exists(folder):
        os.makedirs(folder)