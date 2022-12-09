import psutil
import discord
import sys
import platform
from datetime import datetime

from variables import *
from data_store import *

SIZEBOT_VERSION = 1.0

def format_datetime(time: datetime) -> str:
    return datetime.strftime(time, "%Y-%m-%d %H:%M:%S")

def about_message(data_store: DataStore, interaction: discord.Interaction) -> str:
    process = psutil.Process(os.getpid())
    return f"""**SizeBot Version:** {SIZEBOT_VERSION}
**Python Version:** {sys.version}
**Local Time:** {format_datetime(datetime.now())}
**Running Since:** {format_datetime(datetime.fromtimestamp(process.create_time()))} 
**Operating System:** {platform.system()} {platform.release()} 
**CPU:** {platform.platform()} with {psutil.cpu_count()} cores at {psutil.cpu_percent()}% utilization
**RAM:** {int(psutil.virtual_memory().total)/(1024**3):.3f} GB with {psutil.virtual_memory().percent}% used
**The Girl Reading This:** {interaction.user.display_name}
"""