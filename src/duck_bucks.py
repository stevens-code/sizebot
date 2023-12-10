import discord

from variables import *
from data_store import *
from util import *

MAX_DUCK_BUCKS_TRANSACTION = 100 # The max amount of Duck Bucks to send/receive per command
DUCK_BUCKS_DAILY = 1 # The amount of Duck Bucks to add daily to each user
DUCK_BUCKS_DEFAULT = 10 # The amount of Duck Bucks to initialize a new user with if they don't have a record
DUCK_BUCKS_CAP = 100_000 # The max amount of Duck Bucks you can have

async def add_duck_bucks_entry(data_store: DataStore, interaction: discord.Interaction, target: discord.Member, added_duck_bucks: int):
    await send_bot_thinking_response(interaction)

    abs_duck_bucks = abs(added_duck_bucks)
    initial_sender_duck_bucks = get_duck_bucks(data_store, interaction.guild.id, interaction.user.id)

    if abs_duck_bucks > MAX_DUCK_BUCKS_TRANSACTION and not is_bot_creator(interaction.user):
        await say(interaction, f"{added_duck_bucks} is too many Duck Bucks.", followup = True)
    elif interaction.user.id == target.id:
        await say(interaction, "You can't add Duck Bucks to yourself.", followup = True)
    elif initial_sender_duck_bucks - added_duck_bucks < 0:
        await say(interaction, f"You do not have enough Duck Bucks. You currently have {initial_sender_duck_bucks}.", followup = True)
    else:
        target_duck_bucks =  add_duck_bucks(data_store, interaction.guild.id, target.id, added_duck_bucks)
        sender_duck_bucks = add_duck_bucks(data_store, interaction.guild.id, interaction.user.id, -1 * added_duck_bucks)
        target_mention = target.mention

        if added_duck_bucks < 0:
            await say(interaction, f"Took {abs_duck_bucks} Duck Bucks from {target_mention}. They now have {target_duck_bucks} Duck Bucks. You now have {sender_duck_bucks} Duck Bucks.", followup = True)
        else:
            await say(interaction, f"Gave {abs_duck_bucks} Duck Bucks to {target_mention}. They now have {target_duck_bucks} Duck Bucks. You now have {sender_duck_bucks} Duck Bucks.", followup = True)

async def get_duck_bucks_entry(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    await send_bot_thinking_response(interaction)
    duck_bucks = get_duck_bucks(data_store, interaction.guild.id, target.id)
    await say(interaction, f"{target.mention} has {duck_bucks} Duck Bucks.", followup = True)


def add_duck_bucks(data_store: DataStore, guild_id: int, target_id: int, added_duck_bucks: int) -> int:
    """Add Duck Bucks to a target."""

    # Get the source's Duck Bucks
    cursor = data_store.db_connection.execute(f"SELECT * FROM duck_bucks WHERE guild = ? AND member = ? ORDER BY timestamp DESC", (guild_id, target_id))
    result = cursor.fetchone()

    duck_bucks = 0
    if result is not None: # Already exists so add to it
        duck_bucks = int(result[3]) + added_duck_bucks
    else: # Not found so set to default initial value + the added value
        duck_bucks = DUCK_BUCKS_DEFAULT + added_duck_bucks
    
    if duck_bucks <= 100_000:
        cursor.execute("DELETE FROM duck_bucks WHERE guild = ? AND member = ?", (guild_id, target_id))
        cursor.execute("INSERT INTO duck_bucks(guild, timestamp, member, duck_bucks) VALUES (?, ?, ?, ?)", (guild_id, datetime.now(), target_id, duck_bucks))
        data_store.db_connection.commit()

    return duck_bucks

def get_duck_bucks(data_store: DataStore, guild_id: int, target_id: int) -> int:
    """Get Duck Bucks to a target."""

    # Get the source's Duck Bucks
    cursor = data_store.db_connection.execute(f"SELECT * FROM duck_bucks WHERE guild = ? AND member = ? ORDER BY timestamp DESC", (guild_id, target_id))
    result = cursor.fetchone()

    duck_bucks = 0
    if result is not None: # Already exists
        duck_bucks = int(result[3]) 
    else: # Not found so set to default initial value
        cursor.execute("INSERT INTO duck_bucks(guild, timestamp, member, duck_bucks) VALUES (?, ?, ?, ?)", (guild_id, datetime.now(), target_id, DUCK_BUCKS_DEFAULT))
        data_store.db_connection.commit()
        duck_bucks = DUCK_BUCKS_DEFAULT

    return duck_bucks