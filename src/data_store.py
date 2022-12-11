import os
import sys
import sqlite3
import discord

# Handles loading data from files and environment
def data_read_list_file(filename: str, enable_comments: bool = False) -> list[str]:
    """Helper function to read all lines from a file into a list of strings"""

    with open(filename) as file:
        lines = file.read().splitlines()

        # Strip out comments (lines that start with "//"), if enabled
        if enable_comments:
            stripped_lines = []
            for line in lines:
                if not line.startswith("//"):
                    stripped_lines.append(line)
            return stripped_lines
        else:
            return lines

def load_lines_file(path: str, message: str) -> list[str]:
    lines = data_read_list_file(path)
    print(f"{message:}")
    print(lines)

    return lines

class DataStore:
    """A class that stores all the data that is loaded from the environment. This should be a singleton (only have
    one instance in the entire application) and be initialized in the main.py file. From there, you can pass it to other
    functions throughout the application that need the data it contains."""

    # Constants
    CREATE_TABLES_SQL_PATH = "sql/create_tables.sql"
    DATABASE_PATH = "data/bot_data.db"
    GUILDS_LIST_PATH = "data/guilds.txt"
    DISCORD_TOKEN_PATH = "data/token.txt"
    SIZERAY_SHRINK_MESSAGES_PATH = "data/messages/sizeray_shrink.txt"
    SIZERAY_GROW_MESSAGES_PATH = "data/messages/sizeray_grow.txt"
    SIZERAY_MALFUNCTION_MESSAGES_PATH = "data/messages/sizeray_malfunction.txt"
    CHARACTER_SCARA_MESSAGES_PATH = "data/messages/character_scara.txt"
    GREETER_WELCOME_MESSAGES_PATH = "data/messages/greeter_welcome.txt"
    GREETER_GOODBYE_MESSAGES_PATH = "data/messages/greeter_goodbye.txt"
    MAGIC8_POSITIVE_MESSAGES_PATH = "data/messages/magic8_positive.txt"
    MAGIC8_NEGATIVE_MESSAGES_PATH = "data/messages/magic8_negative.txt"
    MAGIC8_NONCOMMITTAL_MESSAGES_PATH = "data/messages/magic8_noncommittal.txt"

    def __init__(self) -> None:
        # These are the messages that are chosen from at random when someone is shrunk
        self.shrink_messages = []
        # These are the messages that are chosen from at random when someone is grown
        self.grow_messages = []
        # These are the messages that are chosen from at random when the sizeray malfunctions
        self.malfunction_messages = []
        # These are the messages that are chosen from at random when welcoming someone
        self.greeter_welcome_messages = []
        # These are the messages that are chosen from at random when saying goodbye to someone
        self.greeter_goodbye_messages = []
        # Postive responses from the Magic 8 Ball
        self.magic8_positive_messages = []
        # Negative responses from the Magic 8 Ball
        self.magic8_negative_messages = []
        # Non-committal responses from the Magic 8 Ball
        self.magic8_noncommittal_messages = []

        # A list of Discord guild id that the bot targets
        self.guild_ids = []
        # A list of Discord guilds that the bot targets (created from guild_ids)
        self.guilds = []

        # Discord bot token - Provided in the data/token.txt file, which is a plain text file including the token 
        # Discord provides you for running a bot. If this is not defined, the bot cannot run.
        self.discord_bot_token = ""

        # Load the token
        self.load_discord_token()
        # Load guilds
        self.load_guilds()
        # Load data from messages
        self.load_messages()
        # Load database
        self.db_connection = self.load_db()

    def load_guilds(self):
        """Load guilds that this bot is targeting."""

        self.guild_ids = data_read_list_file(DataStore.GUILDS_LIST_PATH, True)
        for guild_id in self.guild_ids:
            self.guilds.append(discord.Object(id=guild_id))
        print("Loaded list of guilds:")
        print(self.guild_ids)

    def load_messages(self):
        """Load all message files from their folder into their lists."""

        self.shrink_messages = load_lines_file(DataStore.SIZERAY_SHRINK_MESSAGES_PATH, "Loaded size ray shrink messages")
        self.grow_messages = load_lines_file(DataStore.SIZERAY_GROW_MESSAGES_PATH, "Loaded size ray grow messages")
        self.malfunction_messages = load_lines_file(DataStore.SIZERAY_MALFUNCTION_MESSAGES_PATH, "Loaded size ray malfunction messages")
        self.character_scara_messages = load_lines_file(DataStore.CHARACTER_SCARA_MESSAGES_PATH, "Loaded size ray malfunction messages")
        self.greeter_welcome_messages = load_lines_file(DataStore.GREETER_WELCOME_MESSAGES_PATH, "Loaded greeter welcome messages")
        self.greeter_goodbye_messages = load_lines_file(DataStore.GREETER_GOODBYE_MESSAGES_PATH, "Loaded greeter goodbye messages")
        self.magic8_positive_messages = load_lines_file(DataStore.MAGIC8_POSITIVE_MESSAGES_PATH, "Loaded Magic 8 positive messages")
        self.magic8_negative_messages = load_lines_file(DataStore.MAGIC8_NEGATIVE_MESSAGES_PATH, "Loaded Magic 8 negative messages")
        self.magic8_noncommittal_messages = load_lines_file(DataStore.MAGIC8_NONCOMMITTAL_MESSAGES_PATH, "Loaded Magic 8 non-committal messages")

    def load_discord_token(self):
        """Load the Discord token from file."""

        if os.path.exists(DataStore.DISCORD_TOKEN_PATH):            
            with open(DataStore.DISCORD_TOKEN_PATH) as file:
                self.discord_bot_token  = file.read()
        else:
            self.discord_bot_token = ""

    def load_db(self) -> sqlite3.Connection:
        """Load a SqlLite database file data/bot_data.db (this is created if it doesn't already exist).
        This stores server specific data for the bot."""

        print("Loading database...")
        existing_db = os.path.exists(DataStore.DATABASE_PATH)
        connection = sqlite3.connect(DataStore.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

        # Create the tables if the database file was not found
        if not existing_db:
            self.create_db(connection)

        return connection

    def create_db(self, connection: sqlite3.Connection):
        """Create database tables."""

        print("Creating tables...")

        with open(DataStore.CREATE_TABLES_SQL_PATH) as file:
            create_tables_sql = file.read()
            connection.executescript(create_tables_sql); 