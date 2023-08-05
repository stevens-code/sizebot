
import pandas
import asyncio

from variables import *
from data_store import *
from util import *
from log import *

MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

async def birthday_monthly_list(data_store: DataStore, sender: Union[discord.Interaction, discord.TextChannel], month: int):
    """Message the monthly birthdays."""

    # If it's an automatic message and automatic messages are disabled
    if isinstance(sender, discord.TextChannel) and not is_birthday_messages_enabled(data_store, sender.guild.id): 
        await asyncio.sleep(0) # Return to caller

    birthday_list = get_monthly_birthday_list(data_store, sender.guild.id, month)
    lines = [f"🎂 Birthdays for {MONTH_NAMES[month - 1]}: "]
    lines.extend(birthday_list)

    await say(sender, "\n".join(lines))

async def birthday_monthly_csv(data_store: DataStore, interaction: discord.Interaction, month: int):
    """Export birthdays to a CSV."""

    lines = ["NAME,BIRTHDAY"]    
    birthday_list = get_guild_monthly_birthdays(data_store, interaction.guild.id, month)
    for name in birthday_list:
        birthday = birthday_list[name]
        no_comma_name = name.replace(',', '').strip()
        lines.append(f"{no_comma_name},{birthday[0]}/{birthday[1]}")

    temp_csv_path = f"data/temp/birthday_csv_{interaction.id}.csv"
    with open(temp_csv_path, "w") as f:
        f.write("\n".join(lines))
    
    await interaction.response.send_message(file = discord.File(temp_csv_path))
    log_message(f"Sending birthday sheet on server '{interaction.guild.name}'")
    os.remove(temp_csv_path)

async def birthday_daily_list(data_store: DataStore, sender: Union[discord.Interaction, discord.TextChannel], month: int, day: int):
    """Message the daily birthdays."""

    # If it's an automatic message and automatic messages are disabled
    if isinstance(sender, discord.TextChannel) and not is_birthday_messages_enabled(data_store, sender.guild.id): 
        await asyncio.sleep(0) # Return to caller

    birthday_list = get_guild_daily_birthdays(data_store, sender.guild.id, month, day)

    if len(birthday_list) > 0:
        lines = ["🎂 Happy birthday to:"]
        for name in birthday_list:
            lines.append(f"***{name}***")
        await say(sender, "\n".join(lines))
    elif isinstance(sender, discord.Interaction): # Not automated
        await say(sender, "No birthdays for today.")
    else:
        await asyncio.sleep(0) # Return to caller

async def birthday_get_info(data_store: DataStore, interaction: discord.Interaction):
    """Message the monthly birthdays."""
    
    cursor = data_store.db_connection.execute(f"SELECT * FROM birthday_source_info WHERE guild = ?", (interaction.guild.id, ))    
    result = cursor.fetchone()
    if result is not None:
        info = result[2]
        await say(interaction, variable_replace(info, interaction, data_store))
    else:
        await say(interaction, "The mods have not set any info on how to add/view birthdays from Google Sheets.")


def is_birthday_messages_enabled(data_store: DataStore, guild_id: int) -> bool:
    """Check if the automatic birthday message feature is enabled."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM birthday_disable WHERE guild = ?", (guild_id, ))    
    result = cursor.fetchone()

    # If there is not entry in the disable table, it's enabled
    return result is None

def store_guild_birthdays(data_store: DataStore, guild_id: int) -> dict:
    """Read guild birthdays from Google Sheets and store them in the database."""

    # Get the birthday settings for the server
    settings_cursor = data_store.db_connection.execute(f"SELECT * FROM birthday_settings WHERE guild = ?", (guild_id, ))    
    settings_result = settings_cursor.fetchone()
    if settings_result is not None:
        try:
            # Dates must be in MM/DD format (i.e. 2/1 for February 1st)
            sheets_key = settings_result[2]
            name_column = settings_result[3]
            birthday_column = settings_result[4]
            url = f"https://docs.google.com/spreadsheets/d/{sheets_key}/export?format=csv"
            data = pandas.read_csv(url, usecols= [name_column, birthday_column])  
            
            birthday_cursor = data_store.db_connection.cursor()
            # Delete birthday entries
            birthday_cursor.execute("DELETE FROM birthdays WHERE guild = ?", (guild_id, ))
            # Add birthday entries
            for index, row in data.iterrows():
                name = row[name_column]
                birthday_str = row[birthday_column]
                if "/" in birthday_str:
                    birthday = birthday_str.split("/")
                    month = int(birthday[0])
                    day = int(birthday[1])
                    birthday_cursor.execute("INSERT INTO birthdays(guild, timestamp, name, month, day) VALUES (?, ?, ?, ?, ?)", (guild_id, datetime.now(), name, month, day))
            # Commit changes
            data_store.db_connection.commit()  
            log_message(f"Loaded {len(data.index)} birthday(s) for {guild_id}")
        except:
            log_message(f"Error fetching and storing birthday data for {guild_id}!")
    else:
        log_message(f"No birthday settings for {guild_id}.")

def is_birthday_notify_enabled(data_store: DataStore, guild_id: int) -> bool:
    """Check if automatic birthday notifications are enabled."""

    cursor = data_store.db_connection.execute(f"SELECT * FROM birthday_disable WHERE guild = ?", (guild_id, ))    
    result = cursor.fetchone()

    # If there is not entry in the disable table, it's enabled
    return result is None

def get_guild_monthly_birthdays(data_store: DataStore, guild_id: int, search_month: int) -> dict:
    """A list of all birthdays for a guild in a month. If month is -1, returns all birthdays, ordered by month and day."""

    results = {}

    cursor = data_store.db_connection.execute(f"SELECT * FROM birthdays WHERE guild = ?", (guild_id, )) if search_month == -1 else data_store.db_connection.execute(f"SELECT * FROM birthdays WHERE guild = ? AND month = ?", (guild_id, search_month)) 
    rows = cursor.fetchall()
    for row in rows:
        name = row[2]
        month = row[3]
        day = row[4]
        results[name] = datetime(2000, month, day)

    # Sort the results by date and create a new dictionary from it
    sorted_results = dict(sorted(results.items(), key=lambda item: item[1]))    
    returned_results = {}
    for sorted_key in sorted_results:
        sorted_result = sorted_results[sorted_key]
        returned_results[sorted_key] = (sorted_result.month, sorted_result.day)
    
    return returned_results

def get_guild_daily_birthdays(data_store: DataStore, guild_id: int, search_month: int, search_day: int) -> dict:
    """A list of all birthdays for a guild for a day."""

    results = {}

    cursor = data_store.db_connection.execute(f"SELECT * FROM birthdays WHERE guild = ? AND month = ? AND day = ? ORDER BY month ASC, day ASC", (guild_id, search_month, search_day))    
    rows = cursor.fetchall()
    for row in rows:
        name = row[2]
        month = row[3]
        day = row[4]
        results[name] = (month, day)
    
    return results

def get_guild_birthdays(data_store: DataStore, guild_id: int) -> dict:
    """A list of all birthdays for a guild."""

    results = {}

    cursor = data_store.db_connection.execute(f"SELECT * FROM birthdays WHERE guild = ? ORDER BY month ASC, day ASC", (guild_id, ))    
    rows = cursor.fetchall()
    for row in rows:
        name = row[2]
        month = row[3]
        day = row[4]
        results[name] = (month, day)
    
    return results

def get_birthday_list(data_store: DataStore, guild_id: int) -> list[str]:
    """Create a formatted list of birthdays for a guild."""

    lines = []    
    birthday_list = get_guild_birthdays(data_store, guild_id)
    for name in birthday_list:
        birthday = birthday_list[name]
        lines.append(f'***{name}*** has a birthday on *{birthday[0]}/{birthday[1]}*')
        
    return lines

def get_monthly_birthday_list(data_store: DataStore, guild_id: int, search_month: int) -> list[str]:
    """Create a formatted list of birthdays this month for a guild."""

    lines = []    
    birthday_list = get_guild_monthly_birthdays(data_store, guild_id, search_month)
    for name in birthday_list:
        birthday = birthday_list[name]
        lines.append(f'***{name}*** has a birthday on *{birthday[0]}/{birthday[1]}*')

    return lines