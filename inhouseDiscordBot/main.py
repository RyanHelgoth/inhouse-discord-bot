'''
Code written by Ryan Helgoth, references I used have been cited in the comments.

This is file contains the code that runs the bot.
'''

from tokens import config
from helperFunctions import commands as cmd
from helperFunctions import setup 

#TODO update firestore security settings
#TODO change command names
#TODO add user names to messages

def main():
    client = setup.getClient()
   
    @client.event
    async def on_ready():
        print("Bot has come online")

    '''
    This command displays help embed which contains a link explaining how to use the bot's commands.
    '''
    @client.command()
    async def inhouseHelp(ctx):
        await cmd.help(ctx)

    '''
    This command moves the users in teams to their corresponding team voice channels.
    '''
    @client.command()
    async def moveToTeams(ctx):
        await cmd.moveUsers(ctx, "teams")

    '''
    This command moves the users in teams to the main channel.
    '''
    @client.command()
    async def moveToMain(ctx):
        await cmd.moveUsers(ctx, "main")
     
    '''
    This command sets the team 1 voice channel.
    '''
    @client.command()
    async def setTeam1(ctx, *args):
        await cmd.setChannel(ctx, args, "one")
    
    '''
    This command sets the team 2 voice channel.
    '''
    @client.command()
    async def setTeam2(ctx, *args):
        await cmd.setChannel(ctx, args, "two")

    '''
    This command sets the main voice channel.
    '''
    @client.command()
    async def setMain(ctx, *args):
        await cmd.setChannel(ctx, args, "main")

    '''
    This command randomly splits the users in the main channel into team 1 and team 2.
    '''
    @client.command()
    async def randomize(ctx):
        await cmd.randomizeMain(ctx)
 
    '''
    This command displays the members of team 1 and team 2.
    '''
    @client.command()
    async def showTeams(ctx):
        await cmd.printTeams(ctx)
        
    '''
    This command allows the user to select members to put in team 1.
    '''
    @client.command()
    async def makeTeam1(ctx, *args):
        await cmd.makeTeam(ctx, args, "one")

    '''
    This command allows the user to select members to put in team 2.
    '''
    @client.command()
    async def makeTeam2(ctx, *args):
        await cmd.makeTeam(ctx, args, "two")

    client.run(config.botToken)

if __name__ == "__main__":
    main()