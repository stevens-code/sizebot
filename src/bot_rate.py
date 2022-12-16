import discord

from data_store import *
from util import *

async def bot_rate_bad(data_store: DataStore, interaction: discord.Interaction):
    """Have the bot apologize for what it has done."""

    await say(interaction, ":robot: :point_right::point_left: **I'm sorry, I'll do better.**")

async def bot_rate_good(data_store: DataStore, interaction: discord.Interaction):
    """Have the bot thank you the compliment."""

    await say(interaction, ":robot: :sparkling_heart: **Thank you!** :sparkling_heart:")