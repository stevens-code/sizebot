import discord
import random

from variables import *
from data_store import *
from util import *

async def magic8_ask(data_store: DataStore, interaction: discord.Interaction, question: str):
    """Generate a message for a random Magic 8 ball result."""

    lines = []

    # Include the question in the response if they asked one
    if len(question) > 0:
        lines.append(f"***{question}***")

    # Choose an outcome and append the Magic 8 ball result
    random_option = random.choice(['positive', 'negative', 'noncommittal']);
    if random_option == 'positive':
        lines.append(f"✨🎱💚 {random.choice(data_store.magic8_positive_messages)} 💚🎱✨")
    elif random_option == 'negative':
        lines.append(f"✨🎱💔 {random.choice(data_store.magic8_negative_messages)} 💔🎱✨")
    else: # noncommittal
        lines.append(f"✨🎱💛 {random.choice(data_store.magic8_noncommittal_messages)} 💛🎱✨")
    
    await say(interaction, "\n".join(lines))