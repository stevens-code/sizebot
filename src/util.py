import discord
import os
from datetime import datetime

# Various helper functions

def format_datetime(time: datetime) -> str:
    """Formats a date and time to a clean format."""

    return datetime.strftime(time, f"%I:%M %p ({time.astimezone().tzname()}) on %m/%d/%Y")

async def say(interaction: discord.Interaction, text: str):
    """Wrapper for sending a plain text message."""

    await interaction.response.send_message(text)

async def say_with_image(interaction: discord.Interaction, text: str, image_path: str):
    """Wrapper for sending a text message with an attached image."""

    file_name = os.path.basename(image_path)
    image_file = discord.File(image_path, filename=file_name)
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