import discord
import os
from typing import Union

from data_store import *
from settings import *

# Various helper functions and constants
DISCORD_SUPPORTED_FILE_EXTS = [".jpg", ".jpeg", ".png", ".gif", ".gifv", ".webm", ".webp", ".mp4", ".wav", ".mp3", ".ogg"]
MAX_DISCORD_MESSAGE_LENGTH = 2000

async def send_bot_thinking_response(sender: Union[discord.Interaction, discord.TextChannel]):
    """Sends a bot thinking command."""

    # Only needed slash commands (discord.Interaction)
    if isinstance(sender, discord.Interaction):
        await sender.response.defer()

async def say(sender: Union[discord.Interaction, discord.TextChannel], text: str, followup = False, ephemeral = False):
    """Wrapper for sending a plain text message."""

    c_text = concat_text(text)

    if isinstance(sender, discord.Interaction):
        log_message(f"Saying '{c_text}' on server '{sender.guild.name}'")
        if followup:
            await sender.followup.send(c_text, ephemeral = ephemeral)
        else:
            await sender.response.send_message(c_text, ephemeral = ephemeral)
    else:
        log_message(f"Saying '{c_text}' on server '{sender.guild.name}'")
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

async def get_member(interaction: discord.Integration, id: int) -> discord.Member:
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
    """Format a member name for a message where you don't want to ping them."""

    return f"***{member.display_name}***"

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
        
def is_bot_creator(member: discord.Member):
    """Check if a member is the bot creator (Steven)."""

    bot_creator_id = 585925109236367401
    return member.id == bot_creator_id

def is_mod(member: discord.Member):
    """Check if a member is a mod or the bot creator (Steven)."""

    return member.guild_permissions.administrator or is_bot_creator(member)

async def deny_non_mod(sender: Union[discord.Interaction, discord.TextChannel]):
    """Send a message denying a non-mod member a certain action."""

    await say(sender, "🚨 **Error:** This is a mod-only command. 🚨")

def get_notifications_channel(data_store: DataStore, guild: discord.Guild) -> discord.channel.TextChannel:
    """Gets the custom notifications channel for a guild from the database, returns the default Discord text channel if there is none. Returns none if neither is set."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM notifications_channel WHERE guild = ?", (guild.id, ))    
    result = cursor.fetchone()
    if result is not None:
        channel_id = result[2]
        return guild.get_channel(channel_id)
    else:
        return guild.system_channel
    
def get_birthday_notifications_channel(data_store: DataStore, guild: discord.Guild):
    """Gets the birthday notifications channel for the server. If it is not set, return the notifications channel for the server."""

    birthday_channel = settings_get_channel(data_store, guild, "birthdays_channel")
    if birthday_channel == None:
        return get_notifications_channel(data_store, guild)
    else:
        return birthday_channel

def get_avatar_name(avatar: discord.Asset, guild_id: int, member_id: int) -> str:
    """Get an avatar's file name."""

    avatar_format = "gif" if avatar.is_animated() else "png"
    return f"{guild_id}_{member_id}.{avatar_format}"

def get_guild_avatar_name(avatar: discord.Asset, guild_id: int) -> str:
    """Get a server avatar's file name."""

    avatar_format = "gif" if avatar.is_animated() else "png"
    return f"{guild_id}.{avatar_format}"

def format_mention(mention: str) -> str:
    """Deal with Discord's stupid username change."""

    if mention.endswith("#0"):
        return mention.removesuffix("#0")
    else:
        return mention