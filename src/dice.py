import discord
import random

def dice_roll(limit: int, rolls: int):
    """Rolls a dice ."""

    if limit < 2 or rolls not in range(1, 11):
        return "The limit must be greater than 2 and the number of rolls must be between 1 and 10!"
    else:
        return ", ".join(str(random.randint(1, limit)) for r in range(rolls))