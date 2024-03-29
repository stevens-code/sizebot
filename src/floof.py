import discord

from variables import *
from data_store import *
from util import *

MAX_FLOOF_CHANGE = 1

async def add_floof_entry(data_store: DataStore, interaction: discord.Interaction, added_floof: int, target: discord.Member):
    if abs(added_floof) > MAX_FLOOF_CHANGE and not is_bot_creator(interaction.user):
        await say(interaction, f"{added_floof} is too much floof.")
    elif interaction.user.id == target.id:
        await say(interaction, "You can't add floof to yourself.")
    else:
        await add_floof(data_store, interaction, added_floof, target)

async def add_floof(data_store: DataStore, interaction: discord.Interaction, added_floof: int, target: discord.Member):
    """Add floof to a target."""

    await send_bot_thinking_response(interaction)

    added_floof_str = str(abs(added_floof))
    message = "Took " + added_floof_str + " floof from {{target}}. " if added_floof < 0 else "Added " + added_floof_str + " floof to {{target}}. "
    guild_id = interaction.guild.id
    target_id = target.id
    cursor = data_store.db_connection.execute(f"SELECT * FROM floof_count WHERE guild = ? AND member = ? ORDER BY timestamp DESC", (guild_id, target_id))
    result = cursor.fetchone()

    floof_count = 0
    if result is not None: # Already exists so add to it
        floof_count = int(result[3]) + added_floof
    else: # No floof found, so set it to the added floof
        floof_count = added_floof

    cursor.execute("DELETE FROM floof_count WHERE guild = ? AND member = ?", (guild_id, target_id))
    cursor.execute("INSERT INTO floof_count(guild, timestamp, member, floof_count) VALUES (?, ?, ?, ?)", (guild_id, datetime.now(), target_id, floof_count))
    data_store.db_connection.commit()

    message += f" They now have {floof_count} floof."

    await say(interaction, variable_replace(message, interaction, data_store, target), followup = True)