import discord
import random

def dice_roll(sides: int, rolls: int):
    """Rolls a dice."""

    if sides < 2 or rolls not in range(1, 101):
        return "The number of sides must be greater than 2 and the number of rolls must be between 1 and 100!"
    else:
        return " | ".join(str(random.randint(1, sides)) for r in range(rolls))