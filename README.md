# SizeBot


## Setup
### Create a bot account
https://discordpy.readthedocs.io/en/stable/discord.html

### Create invite link
Go to the OAuth2/URL Generator in Discord's application settings.
Scopes: bot, applications.commands
Bot Permissions: manage roles, read messages/view channels, send messages, send messages in threads, embed links, attach files, read message history, use external emojis, use external stickers, add reactions, use slash commands

### Add token.txt
In order for the bot to run, it needs to have a token from Discord. From the Bot section in Discord's application settings, click the "Reset Token" button and copy the token generated into a file called "data/token.txt". Now the Bot will log into Discor using a token.

### Install Python packages
python3 -m pip install -U discord.py pysqlite3 psutil Pillow numpy pandas matplotlib seaborn
