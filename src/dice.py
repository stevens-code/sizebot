import discord
import random
from util import *

async def dice_roll(sides: int, rolls: int):
    """Rolls a dice."""

    if sides < 2 or rolls not in range(1, 101):
        await say("The number of sides must be greater than 2 and the number of rolls must be between 1 and 100!")
    else:
        await say(" | ".join(str(random.randint(1, sides)) for r in range(rolls)))