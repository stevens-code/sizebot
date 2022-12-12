import numpy
import pandas
from matplotlib import pyplot
import seaborn
import discord
import random

from variables import *
from data_store import *
from util import *

# A palette for actions
ACTIONS_PALETTE = ["#ad0d2f", "#0749ad", "#78b116"]

async def sizeray_stats_last_10(data_store: DataStore, interaction: discord.Interaction):
    """Lists the last 10 size ray actions"""

    lines = ["**The last 10 size ray actions were:**"]

    cursor = data_store.db_connection.execute(f"SELECT * from sizeray_actions WHERE guild = ? ORDER BY timestamp DESC LIMIT 10", (interaction.guild.id, ))    
    rows = cursor.fetchall()
    i = 1
    for row in rows:
        time = format_datetime(row[1])
        action = row[2]
        target = await get_user(interaction, row[3])
        author = await get_user(interaction, row[4])

        if author is not None and target is not None:
            if action == "malfunction":
                lines.append(f"({i}) The size ray *malfunctioned* on {no_ping(author)} while they were trying to use it on {no_ping(target)} at {time}")            
            elif action == "shrink":
                lines.append(f"({i}) {no_ping(author)} *shrank* {no_ping(target)} at {time}")     
            elif action == "grow":
                lines.append(f"({i}) {no_ping(author)} *grew* {no_ping(target)} at {time}")  
        else:
            lines.append(f"({i}) Sadly, the author or target of this action has left us")
        
        i += 1
    
    await say(interaction, "\n".join(lines))

async def sizeray_stats_chart(data_store: DataStore, interaction: discord.Interaction):
    """Show the size ray actions stats in a chart."""

    # Fetch the data
    await say(interaction, "Generating size ray stats chart...")
    cursor = data_store.db_connection.execute(f"SELECT [action], COUNT(*) [count] from sizeray_actions WHERE guild = ? GROUP BY [action] ORDER BY [action] ASC", (interaction.guild.id, ))    
    rows = cursor.fetchall()
    action_counts = {}
    for row in rows:
        action_counts[row[0]] = row[1]
    
    if len(action_counts) == 0:
        await say(interaction, "There are no stats available for this server.", True)
    else:
        # Generate the chart
        keys = list(action_counts.keys())
        vals = [int(action_counts[k]) for k in keys]
        palette = seaborn.color_palette(ACTIONS_PALETTE)
        seaborn.barplot(x=keys, y=vals, palette=palette) 
        temp_chart_path = f"data/images/temp/stats_{random.randint(0, 100000)}.png"
        pyplot.title(f'Size ray stats for "{interaction.guild.name}"')
        pyplot.xlabel("Action type", color='#555555')
        pyplot.ylabel("Count", color='#555555')
        pyplot.isinteractive = False
        pyplot.savefig(temp_chart_path)
        # Post it
        await say_with_image(interaction, "", temp_chart_path, True)
        # Delete once it's done
        os.remove(temp_chart_path)

async def sizeray_stats_chart_for(data_store: DataStore, interaction: discord.Interaction, target: discord.Member):
    """Show the size ray actions stats in a chart for member."""

    # Fetch the data
    await say(interaction, f"Generating size ray stats chart for {no_ping(target)}...")
    cursor = data_store.db_connection.execute(f"SELECT [action], COUNT(*) [count] from sizeray_actions WHERE guild = ? AND target = ? GROUP BY [action] ORDER BY [action] ASC", (interaction.guild.id, target.id))    
    rows = cursor.fetchall()
    action_counts = {}
    for row in rows:
        action_counts[row[0]] = row[1]
    
    if len(action_counts) == 0:
        await say(interaction, f"There are no stats available for {no_ping(target)}.", True)
    else:
        # Generate the chart
        keys = list(action_counts.keys())
        vals = [int(action_counts[k]) for k in keys]
        palette = seaborn.color_palette(ACTIONS_PALETTE)
        seaborn.barplot(x=keys, y=vals, palette=palette) 
        temp_chart_path = f"data/images/temp/stats_{random.randint(0, 100000)}.png"
        pyplot.title(f'Size ray stats for "{target.display_name}"')
        pyplot.xlabel("Action type", color='#555555')
        pyplot.ylabel("Times targeted", color='#555555')
        pyplot.isinteractive = False
        pyplot.savefig(temp_chart_path)
        # Post it
        await say_with_image(interaction, "", temp_chart_path, True)
        # Delete once it's done
        os.remove(temp_chart_path)


async def sizeray_stats_biggest_users(data_store: DataStore, interaction: discord.Interaction):
    # Fetch the biggest users
    cursor = data_store.db_connection.execute(f"SELECT [author], COUNT(*) [count] from sizeray_actions WHERE guild = ? GROUP BY [author] ORDER BY [count] DESC LIMIT 10", (interaction.guild.id, ))    
    rows = cursor.fetchall()
    lines = ["**The top 10 biggest size ray users were:**"]
    i = 1
    for row in rows:
        user: discord.Member = await get_user(interaction, row[0])        
        if user is not None:
            lines.append(f"({i}) {no_ping(user)}, who used the size ray {row[1]} time(s).")
        else:
            lines.append(f"({i}) A user who cannot be found, who used the size ray {row[1]} time(s).")
        i += 1

    # Fetch the biggest targets
    cursor = data_store.db_connection.execute(f"SELECT [target], COUNT(*) [count] from sizeray_actions WHERE guild = ? GROUP BY [target] ORDER BY [count] DESC LIMIT 10", (interaction.guild.id, ))    
    rows = cursor.fetchall()
    lines.append("\n**The top 10 biggest size ray targets were:**")
    i = 1
    for row in rows:
        user: discord.Member = await get_user(interaction, row[0])        
        if user is not None:
            lines.append(f"({i}) {no_ping(user)}, who was hit by the size ray {row[1]} time(s).")
        else:
            lines.append(f"({i}) A user who cannot be found, who was hit by the size ray {row[1]} time(s).")
        i += 1

    await say(interaction, "\n".join(lines))
    