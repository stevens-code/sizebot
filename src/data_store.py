import os
import sys
import sqlite3

# Handles loading data from files and environment
def data_read_list_file(filename: str) -> list[str]:
    """Helper function to read all lines from a file into a list of strings"""

    with open(filename) as file:
        return file.read().splitlines()

class DataStore:
    """A class that stores all the data that is loaded from the environment. This should be a singleton (only have
    one instance in the entire application) and be initialized in the main.py file. From there, you can pass it to other
    functions throughout the application that need the data it contains."""

    # Constants
    CREATE_TABLES_SQL_PATH = "sql/create_tables.sql"
    DATABASE_PATH = "data/bot_data.db"
    SIZERAY_SHRINK_MESSAGES_PATH = "data/messages/sizeray_shrink.txt"
    SIZERAY_GROW_MESSAGES_PATH = "data/messages/sizeray_grow.txt"
    SIZERAY_MALFUNCTION_MESSAGES_PATH = "data/messages/sizeray_malfunction.txt"

    def __init__(self) -> None:
        # These are the messages that are chosen from at random when someone is shrunk
        self.shrink_messages = []
        # These are the messages that are chosen from at random when someone is grown
        self.grow_messages = []
        # These are the messages that are chosen from at random when the sizeray malfunctions
        self.malfunction_messages = []

        # Discord bot token - An environment variable "SIZEBOT_TOKEN", which is the token Discord provides 
        # you for running a bot. If this is not defined, the application cannot run. After setting it, log in and
        # out again so it can take effect globally.
        self.discord_bot_token = ""

        # Load environment variables
        self.load_environment_variables()
        # Load data from messages
        self.load_messages()
        # Load database
        self.db_connection = self.load_db()

    def load_messages(self):
        """Load all message files from their folder into their lists."""

        self.shrink_messages = data_read_list_file(DataStore.SIZERAY_SHRINK_MESSAGES_PATH)
        print("Loaded size ray shrink messages:")
        print(self.shrink_messages)

        self.grow_messages = data_read_list_file(DataStore.SIZERAY_GROW_MESSAGES_PATH)
        print("Loaded size ray grow messages:")
        print(self.grow_messages)

        self.malfunction_messages = data_read_list_file(DataStore.SIZERAY_MALFUNCTION_MESSAGES_PATH)
        print("Loaded size ray malfunction messages:")
        print(self.malfunction_messages) 

    def load_environment_variables(self):
        """Load environment variables into local variables"""

        try:  
            self.discord_bot_token = os.environ["SIZEBOT_TOKEN"]
        except KeyError:
            print("Please define the environment variable SIZEBOT_TOKEN. This is the token given by Discord that allows you to connect.")
            sys.exit(1)

    def load_db(self) -> sqlite3.Connection:
        """Load a SqlLite database file data/bot_data.db (this is created if it doesn't already exist).
        This stores server specific data for the bot."""

        print("Loading database...")
        existing_db = os.path.exists(DataStore.DATABASE_PATH)
        connection = sqlite3.connect(DataStore.DATABASE_PATH)

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