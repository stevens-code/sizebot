import psutil
import discord
import sys
import platform
from datetime import datetime

from variables import *
from data_store import *
from util import *

SIZEBOT_VERSION = 2.0

async def about_message(data_store: DataStore, interaction: discord.Interaction):
    """Responds with a message about SizeBot."""

    process = psutil.Process(os.getpid())
    await say(interaction, f"""**SizeBot Version:** {SIZEBOT_VERSION}
**GitHub Repository:** stevens-code/sizebot
**Python Version:** {sys.version}
**Current Local Time:** {format_datetime(datetime.now())}
**Running Since:** {format_datetime(datetime.fromtimestamp(process.create_time()))} 
**Operating System:** {platform.system()} {platform.release()} 
**CPU:** {platform.platform()} with {psutil.cpu_count()} cores at {psutil.cpu_percent()}% utilization
**RAM:** {int(psutil.virtual_memory().total)/(1024**3):.1f} GB with {psutil.virtual_memory().percent}% used
**The Girl Reading This:** {no_ping(interaction.user)}
""")
