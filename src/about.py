import psutil
import discord
import sys
import platform
import datetime

from variables import *
from data_store import *

SIZEBOT_VERSION = 1.0

def about_message(data_store: DataStore, interaction: discord.Interaction) -> str:
    return f"""**SizeBot Version:** {SIZEBOT_VERSION}
**Python Version:** {sys.version}
**Local Time:** {datetime.datetime.now()}
**Operating System:** {platform.system()} {platform.release()} 
**CPU:** {platform.platform()} with {psutil.cpu_count()} cores at {psutil.cpu_percent()}% utilization
**RAM:** {int(psutil.virtual_memory().total)/(1024**3):.3f} GB with {psutil.virtual_memory().percent}% used
**The Girl Reading This:** {interaction.user.display_name}
"""