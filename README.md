# What is Inhouse Discord Bot?
- Inhouse Discord Bot is a Discord bot that randomizes teams and puts users in the correct voice channels. Simplifies setting up inhouse/scrim games with friends.

# How can I add the bot to my server?
- Currently the bot is under development, but after it is done a link will be posted here to add the bot to your server.

# How do you use the bot?
- # Overview
- # Commands
  - **!inhousehelp** \- Shows an embed with a link to this page.
    - **Arguments:** none
    <br/>
  - **!showteams** \- Shows members of the command user's team 1 and team 2. 
    - **Arguments:** none
    <br/>
  - **!setmainchat** \- Sets the command user's main voice channel.
    - **Arguments:** name of channel you want to set.
    <br/>
  - **!setteamchat1** \- Sets the command user's team 1 voice channel.
    - **Arguments:** name of channel you want to set.
    <br/>
  - **!setteamchat2** \- Sets the command user's team 2 voice channel.
    - **Arguments:** name of channel you want to set.
    <br/>
  - **!maketeam1** \- Sets the command user's list of team members for their team 1.
    - **Arguments:** tagged users seperated by spaces (either select users by typing "@" and then picking users, or by typing <@\*> where the "\*" is a user id).
    <br/>
  - **!maketeam2** \- Sets the command user's list of team members for their team 2.
    - **Arguments:** tagged users seperated by spaces (either select users by typing "@" and then picking users, or by typing <@\*> where the "\*" is a user id).
    <br/>
  - **!randomize** \- Creates a randomized team 1 and team 2 for the command user with members from their main channel. 
    - **Arguments:** none
    <br/>
  - **!movetoteams** \- Moves the command user's team 1 and team 2 members to the command user's corresponding team channels.
    - **Arguments:** none
    <br/>
  - **!movetomain** \- Moves the command user's team 1 and team 2 members to the command user's main channel.
    - **Arguments:** none
    
   
    

# How can I run the code on my computer?
- The code for this bot is available to download and modify, however the code will not run without a token. This token is private and I cannot share it for security reasons. 
- To get your own token you will have to create a bot through the [Discord developer portal](https://discord.com/developers/applications). Then you can put the line token = "\<YOUR TOKEN HERE\>" into a file named config.py in the same folder as main.py and the code should now work for you. 

# Who worked on Inhouse Discord Bot?
- All the Python code is written by Ryan Helgoth
