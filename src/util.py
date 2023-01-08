import discord
import os
from datetime import datetime
from typing import Union

from data_store import *

# Various helper functions and constants
DISCORD_SUPPORTED_FILE_EXTS = [".jpg", ".jpeg", ".png", ".gif", ".gifv", ".webm", ".webp", ".mp4", ".wav", ".mp3", ".ogg"]
MAX_DISCORD_MESSAGE_LENGTH = 2000

def format_datetime(time: datetime) -> str:
    """Formats a date and time to a clean format."""

    return datetime.strftime(time, f"%I:%M %p ({time.astimezone().tzname()}) on %m/%d/%Y")

async def send_bot_thinking_response(sender: Union[discord.Interaction, discord.TextChannel]):
    """Sends a bot thinking command."""

    # Only needed slash commands (discord.Interaction)
    if isinstance(sender, discord.Interaction):
        await sender.response.defer()

async def say(sender: Union[discord.Interaction, discord.TextChannel], text: str, followup = False, ephemeral = False):
    """Wrapper for sending a plain text message."""

    c_text = concat_text(text)

    if isinstance(sender, discord.Interaction):
        if followup:
            await sender.followup.send(c_text, ephemeral = ephemeral)
        else:
            await sender.response.send_message(c_text, ephemeral = ephemeral)
    else:
        await sender.send(c_text)


async def say_with_image(sender: Union[discord.Interaction, discord.TextChannel], text: str, image_path: str, followup = False, ephemeral = False):
    """Wrapper for sending a text message with an attached image."""

    c_text = concat_text(text)
    file_name = os.path.basename(image_path)
    image_file = discord.File(image_path, filename=file_name)
    if isinstance(sender, discord.Interaction):
        if followup:
            await sender.followup.send(c_text, file = image_file, ephemeral = ephemeral)
        else:
            await sender.response.send_message(c_text, file = image_file, ephemeral = ephemeral)
    else:
        await sender.send(c_text, file = image_file)

async def get_user(interaction: discord.Integration, id: int) -> discord.Member:
    """Get a member by ID."""
    
    # Try to find member in cache first (way faster)
    found_member = interaction.guild.get_member(id)
    if found_member is not None:
        return found_member
    else:
        # If not, query Discord servers (slow)
        return await interaction.guild.fetch_member(id)

def concat_text(text: str):
    """Make sure text is less than Discord's max message length, concat it if not."""

    return text if len(text) <= MAX_DISCORD_MESSAGE_LENGTH else f"{text[:MAX_DISCORD_MESSAGE_LENGTH - 3]}..."

def no_ping(member: discord.Member):
    """Format a member name for a meesage where you don't want to ping them."""

    return f"***{member.display_name}***";

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

def is_mod(member: discord.Member):
    """Check if a member is a mod or the bot creator (Steven)."""

    bot_creator_id = 585925109236367401
    return member.guild_permissions.administrator or member.id == bot_creator_id

async def deny_non_mod(sender: Union[discord.Interaction, discord.TextChannel]):
    """Send a message denying a non-mod member a certain action"""

    await say(sender, "🚨 **Error:** This is a mod-only command. 🚨")

def get_notifications_channel(data_store: DataStore, guild: discord.Guild) -> discord.channel.TextChannel:
    """Gets the custom notifications channel for a guild from the database, returns the default Discord text channel if there is none. Returns none if neither is set."""

    cursor = data_store.db_connection.execute(f"SELECT * from notifications_channel WHERE guild = ? ", (guild.id, ))    
    result = cursor.fetchone()
    if result is not None:
        channel_id = result[2]
        return guild.get_channel(channel_id)
    else:
        return guild.system_channel