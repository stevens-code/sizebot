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

### Bot invite
The invite for the current version is:
https://discord.com/api/oauth2/authorize?client_id=1050257321848217650&permissions=414733159488&scope=bot%20applications.commands

If you are setting up SizeBot to run off of your own machine the settings would look like this:
<img width="1728" alt="OAuth" src="https://user-images.githubusercontent.com/120059830/207387978-550403db-07d7-4a27-88ff-f0efff84afa0.png">

### Permissions
To allow the users to access the application commands, make sure they have the "Use Application Commands" permission and make sure the channels you want to have the bot run in have that permsision enabled as well.
<img width="1025" alt="Permissions" src="https://user-images.githubusercontent.com/120059830/207387248-8f817a75-ed25-42da-b10c-3f2ad39482c3.png">

When users have the correct permissions, they should have this pop up after typing "/" into Discord listing the available commands:
<img width="1151" alt="AvailableCommannds" src="https://user-images.githubusercontent.com/120059830/207387494-cffdbdca-fcdc-4282-8cd2-d13fa8ae04a5.png">

### Restricting commands
To restrict commands, you can go to the server settings and under Apps > Integrations, click on SizeBot and it will display a list of commands. Since it uses Discord's slash commands for all of it's commands, SizeBot's commands can all be managed from here. This includes restricting certain commands to certain channels or only allowing certain commands to be run by certain roles/users.
<img width="1133" alt="ManagingCommands" src="https://user-images.githubusercontent.com/120059830/207387125-4b7f5165-e218-4f85-8afb-8ee3c93fa7c5.png">
<img width="1133" alt="RestrictingCommands" src="https://user-images.githubusercontent.com/120059830/207387157-106e3713-47f8-4319-a5f5-94e13a3af7b3.png">

### Mod settings
There are a variety of mod-specific commands to set settinging on SizeBot. For example this one sets the welcome image that greets new users:
<img width="1133" alt="CustomWelcom" src="https://user-images.githubusercontent.com/120059830/207387644-4200d53b-d1f6-41fd-9a7d-b87fab996470.png">

#### Current mod commands
***set-sizebot-variable:*** Set a server-specific variable to be replaced in SizeBot messages.   
***delete-sizebot-variable:*** Delete a server-specific variable from SizeBot.   
***set-sizebot-welcome:*** Set the SizeBot welcome image.   
***reset-sizebot-welcome:*** Delete the custom SizeBot welcome image and reset to default.   
***set-sizebot-goodbye:*** Set the SizeBot goodbye image.   
***reset-sizebot-goodbye:*** Delete the custom SizeBot goodbye image and reset to default.  
***set-sizeray-immunity-role:*** Set the size ray immunity role.  
***enable-sizebot-welcome:*** Allow SizeBot to send welcome messages.   
***disable-sizebot-welcome:*** Don't allow SizeBot to send welcome messages.  
***enable-sizebot-goodbye:*** Allow SizeBot to send goodbye messages.   
***disable-sizebot-goodbye:*** Don't allow SizeBot to send goodbye messages.  

### Server variables
To set custom emojis for the server to use in messages, use the ***set-sizebot-variable*** command. The variables that matter currently are: growth_ray (growth ray emoji), shrink_ray (shrink ray emoji), size_ray (size ray emoji), and size_shield (size immunity shield emoji).

Setting the custom emoji variables:   
<img width="652" alt="Setting Variables" src="https://user-images.githubusercontent.com/120059830/207391663-7264f845-82e8-4b64-89df-07626a70156e.png">

The emojis in use by the bot:
<img width="1097" alt="Custom Emojis" src="https://user-images.githubusercontent.com/120059830/207391505-7e7f0147-7757-45df-880d-243a56242ff6.png">

### Changing the bot's name
To change the bot's name in your server, right click on the bot and select "Change Nickname..." and type in the new name:
<img width="604" alt="ChangeNickname" src="https://user-images.githubusercontent.com/120059830/207395955-f3dce7b0-7226-4611-9b46-1be07570f1d9.png">
<img width="604" alt="ChangeNicknameDialog" src="https://user-images.githubusercontent.com/120059830/207395981-bf164fa8-595a-42b5-8127-d70af4746042.png">

After clicking save, the new name should apply:  
<img width="252" alt="NewNickname" src="https://user-images.githubusercontent.com/120059830/207396038-e9c2bbed-58ec-4087-ae3f-e88f26932f21.png">

