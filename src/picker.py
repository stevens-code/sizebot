import discord
import random

from util import *

async def picker_pick_random(data_store: DataStore, interaction: discord.Interaction, title: str, unsplit_options: str):
    """Pick a random option from a list of options."""

    lines = []

    # Include the title in the response if they supplied one
    if len(title) > 0:
        lines.append(f"***{title}:***")

    # Choose an outcome and append it
    options = unsplit_options.split("|")
    random_option = random.choice(options)
    lines.append(random_option.strip())

    await say(interaction, "\n".join(lines))