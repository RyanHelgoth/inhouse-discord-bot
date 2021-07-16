# What is Inhouse Bot?
- Inhouse Bot is a Discord bot that makes setting up [inhouse games](https://www.urbandictionary.com/define.php?term=inhouse) easier by moving users between team voice channels and a main channel for pre/after match talks. Inhouse Bot also has a randomize feature to make teams for you when you are having trouble deciding how to split teams up.

# How can I add the bot to my discord server?
- Click [here](https://discord.com/api/oauth2/authorize?client_id=852327548704915486&permissions=16862208&scope=bot) to add Inhouse Bot to your discord server!

# How do you use the bot?
- # Overview
  - To get started use the !setmainchat, !setteamchat1, and !setteamchat2 commands to set the voice channels you will use for communications. The main channel acts as a place to gather before and after matches, while the team channels act as channels that are used for communications during matches. 
  - The next thing you will want to do is create your teams. You can do this by either gathering everyone in the main channel you've set and then using the !randomize command to make random teams or you can manually create teams with !maketeam1 and !maketeam2.
  - Now that your teams are made you can use the !movetoteams and !movetomain commands to move members of your teams between your set channels.
  - If you forget who is on a team you can use the !showteams command to see who is on your teams.
  
  - # Notes
    - Every user on a sever has their own teams as well as main and team channels. For example if another user makes teams or sets channels in the same server, it will not affect your teams or channels.
    - Settings are saved per server so if you set teams or channles on one server, you will not have access to them on other servers.
    - All command arguments are seperated by one space.
    - When making teams select members by typing "@" and then picking users, or by typing <@\*> where the "\*" is a user id. When setting channels do not use id, instead just type the channel name.
    - I am hosting the bot locally on one of my computers, so if the bot is not responding or is offline, it is likely due to internet issues on my side. If the bot does go offline then it should come back online automatically once my internet issues get resolved.

- # Commands
  - **!inhousehelp** \- Shows an embed with a link to this page.
    - **Arguments:** none
    <br/>
  - **!showteams** \- Shows members of the command user's team 1 and team 2. 
    - **Arguments:** none
    <br/>
  - **!setmainchat** \- Sets the command user's main voice channel.
    - **Arguments:** name of the channel you want to set.
    <br/>
  - **!setteamchat1** \- Sets the command user's team 1 voice channel.
    - **Arguments:** name of the channel you want to set.
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
- The code for this bot is available to download and modify, however the code will not run without a discord bot token and a firebase key. These files are private and I cannot share them for security reasons. 
- To get your own discord bot token you will have to create a bot through the [Discord developer portal](https://discord.com/developers/applications). Then you can put the line token = "YOUR TOKEN HERE" into a file named config.py. Then create a folder called "tokens" and put it in the "inhouseDiscordBot" folder, after put config.py in the tokens folder.
- Next you will have to get your own firebase key. You can do this by setting up a firebase firestore project and generating a key using the [setup guide](https://firebase.google.com/docs/firestore/quickstart). After generating the key you should get a .json file. Name it "firebaseKey.json" and put it in the "tokens" folder you already made. 
- Lastly you will have to install the firestore library [here](https://firebase.google.com/docs/firestore/quickstart#set_up_your_development_environment) and install the discord library [here](https://discordpy.readthedocs.io/en/stable/intro.html#installing). Now you should be ready to go!

# Who worked on Inhouse Discord Bot?
- All the Python code is written by Ryan Helgoth with references used cited in comments in the code.
