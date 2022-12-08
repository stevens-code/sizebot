import os
import sys

# Handles loading data from files and environment

def data_read_list_file(filename: str) -> list[str]:
    """Helper function to read all lines from a file into a list of strings"""

    with open(filename) as file:
        return file.read().splitlines()

class DataStore:
    """A class that stores all the data that is loaded from the environment. This should be a singleton (only have
    one instance in the entire application) and be initialized in the main.py file. From there, you can pass it to other
    functions throughout the application that need the data it contains."""

    def __init__(self) -> None:
        # These are the messages that are chosen from at random when someone is shrunk
        self.shrink_messages = []
        # These are the messages that are chosen from at random when someone is grown
        self.grow_messages = []
        # These are the messages that are chosen from at random when the sizeray malfunctions
        self.malfunction_messages = []

        # Discord bot token - A environment variable "SIZEBOT_TOKEN", which is the token Discord provides 
        # you for running a bot. If this is not defined, the application cannot run. After setting it, log in and
        # out again so it can take effect globally.
        self.discord_bot_token = ''

        # Initial call to load data from messages
        self.load_messages()

        # Intial call to load environment variables
        self.load_environment_variables()

    def load_messages(self):
        """Load all message files from their folder into their lists"""

        self.shrink_messages = data_read_list_file('data/messages/sizeray_shrink.txt')
        print('Loaded sizeray_shrink.txt:')
        print(self.shrink_messages)

        self.grow_messages = data_read_list_file('data/messages/sizeray_grow.txt')
        print('Loaded sizeray_grow.txt:')
        print(self.grow_messages)

        self.malfunction_messages = data_read_list_file('data/messages/sizeray_malfunction.txt')
        print('Loaded sizeray_malfunction.txt:')
        print(self.malfunction_messages) 

    def load_environment_variables(self):
        """Load environment variables into local variables"""

        try:  
            self.discord_bot_token = os.environ['SIZEBOT_TOKEN']
        except KeyError:
            print('Please define the environment variable SIZEBOT_TOKEN. This is the token given by Discord that allows you to connect.')
            sys.exit(1)