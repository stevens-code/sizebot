import discord
import random

from variables import *
from data_store import *
from util import *

async def character_scara(data_store: DataStore, interaction: discord.Interaction):
    """Say a random Scaramouche elemental burst line."""

    random_message = random.choice(data_store.character_scara_messages);
    await say_with_image(interaction, variable_replace(f"***{random_message}***", interaction, data_store), "data/images/scara.gif")