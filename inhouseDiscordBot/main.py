'''
Code written by Ryan Helgoth, references I used have been cited in the comments.

This is file contains the code that runs the bot.
'''

from tokens import config
from functions import commands as cmd
from functions import setup 

#TODO check if team string is lower case for all functions
#TODO catch expception for unknown commands https://stackoverflow.com/a/52900437

def main():
    client = setup.getClient()
    db = setup.getDB()
   
    @client.event
    async def on_ready():
        print("Bot has come online")

    @client.event
    async def on_resumed():
        print("Bot has reconnected")

    @client.event
    async def on_disconnect():
        print("Bot has disconnected")

    '''
    This command displays help embed which contains a link explaining how to use the bot's commands.
    '''
    @client.command()
    async def inhousehelp(ctx):
        await cmd.help(ctx)

    '''
    This command moves the users in teams to their corresponding team voice channels.
    '''
    @client.command()
    async def movetoteams(ctx):
        await cmd.moveToChannel(ctx, db, "teams")

    '''
    This command moves the users in teams to the main channel.
    '''
    @client.command()
    async def movetomain(ctx):
        await cmd.moveToChannel(ctx, db, "main")
     
    '''
    This command sets the team 1 voice channel.
    '''
    @client.command()
    async def setteamchat1(ctx, *args):
        await cmd.setChannel(ctx, db, args, "Team 1")
    
    '''
    This command sets the team 2 voice channel.
    '''
    @client.command()
    async def setteamchat2(ctx, *args):
        await cmd.setChannel(ctx, db, args, "Team 2")

    '''
    This command sets the main voice channel.
    '''
    @client.command()
    async def setmainchat(ctx, *args):
        await cmd.setChannel(ctx, db, args, "Main")

    '''
    This command randomly splits the users in the main channel into team 1 and team 2.
    '''
    @client.command()
    async def randomize(ctx):
        await cmd.randomizeMain(ctx, db)
 
    '''
    This command displays the members of team 1 and team 2.
    '''
    @client.command()
    async def showteams(ctx):
        await cmd.printTeams(ctx, db)
        
    '''
    This command allows the user to select members to put in team 1.
    '''
    @client.command()
    async def maketeam1(ctx, *args):
        await cmd.makeTeam(ctx, db, args, "Team 1")

    '''
    This command allows the user to select members to put in team 2.
    '''
    @client.command()
    async def maketeam2(ctx, *args):
        await cmd.makeTeam(ctx, db, args, "Team 2")

    client.run(config.botToken)

if __name__ == "__main__":
    main()