'''
Code written by Ryan Helgoth, references I used have been cited in the comments.

This is file contains the code that runs the bot.
'''

import discord 
from discord.ext import commands
import config
import random

#TODO test moving offline users to a channel
#TODO make function for move to main/teams
#TODO move functions into seperate file
#TODO deal with channels withh the same name

def main():
    ''' 
    Link: https://stackoverflow.com/a/65368556
    Author: kubaki18
    Date: Dec 19 '20 at 9:54
    License: SA 4.0

    I used this post to learn help fix a bug in which members
    were not found in voice channels due to not gaving the 
    members intent enabled.
    '''
    intents = discord.Intents().default()
    intents.members = True
    botInfo = discord.Activity(type=discord.ActivityType.watching, name="for !inhouseHelp command")
    client = commands.Bot(command_prefix = "!", activity = botInfo, help_command = None, intents=intents)

    #using global varibles for now until I set up a database
    #TODO store channel id's and arrays of user id's in database and get the actual objects on startup (maybe use pickle library)

    client.mainChannel = None
    client.team1Channel = None
    client.team2Channel = None
    client.team1 = []
    client.team2 = []

    @client.event
    async def on_ready():
        print("Bot has come online")
        #TODO get saved settings from database
        #https://stackoverflow.com/a/67145571

    '''
    This command displays help embed which contains a link explaining how to use the bot's commands.
    '''
    @client.command()
    async def inhouseHelp(ctx):
        ''' 
        Link: https://stackoverflow.com/a/64529788
        Author: stijndcl
        Date: Oct 25 '20 at 23:17
        License: SA 4.0

        I used this post to learn how to send
        hyperlinks with the bot.
        '''
        help = discord.Embed()
        help.title = "Inhouse Bot Help"
        help.description = ":keyboard: [Help and list of commands here!](https://github.com/RyanHelgoth/inhouse-discord-bot#how-do-you-use-the-bot)"
        await ctx.send(embed = help)

    '''
    This command moves the users in teams to their team voice channels.
    '''
    @client.command()
    async def moveToTeams(ctx):
        if not None in (client.team1Channel, client.team2Channel):
            if len(client.team1) > 0 and len(client.team2) > 0:
                for member in client.team1:
                    try:
                        await member.move_to(client.team1Channel)
                        await ctx.send("Moved " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.team1Channel.id) + ">")
                    except discord.HTTPException:
                        await ctx.send("Error: Unable to move " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.team1Channel.id) + ">")
                for member in client.team2:
                    try:
                        await member.move_to(client.team2Channel)
                        await ctx.send("Moved " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.team2Channel.id) + ">")
                    except discord.HTTPException:
                        await ctx.send("Error: Unable to move " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.team2Channel.id) + ">")
            else:
                await ctx.send("Please populate teams before using this command.")
        else:
            await ctx.send("You must first set team channels before using this command")

    '''
    This command moves the users in teams to the main channel.
    '''
    @client.command()
    async def moveToMain(ctx):
        if client.mainChannel is not None:
            if len(client.team1) > 0 and len(client.team2) > 0:
                for member in client.team1:
                    #TODO Make into function to avoid repetition?
                    try:
                        await member.move_to(client.mainChannel)
                        await ctx.send("Moved " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.mainChannel.id) + ">")
                    except discord.HTTPException:
                        await ctx.send("Error: Unable to move " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.mainChannel.id) + ">")
                for member in client.team2:
                    try:
                        await member.move_to(client.mainChannel)
                        await ctx.send("Moved " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.mainChannel.id) + ">")
                    except discord.HTTPException:
                        await ctx.send("Error: Unable to move " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.mainChannel.id) + ">")
            else:
                await ctx.send("Please populate teams before using this command.")
        else:
            await ctx.send("You must first set the main channel before using this command")

    '''
    This command sets the team 1 voice channel.
    '''
    @client.command()
    async def setTeam1(ctx, *args):
        await setChannel(ctx, args, "one")
    
    '''
    This command sets the team 2 voice channel.
    '''
    @client.command()
    async def setTeam2(ctx, *args):
        await setChannel(ctx, args, "two")

    '''
    This command sets the main voice channel.
    '''
    @client.command()
    async def setMain(ctx, *args):
        await setChannel(ctx, args, "main")

    '''
    This command randomly splits the users in the main channel into team 1 and team 2.
    '''
    @client.command()
    async def randomize(ctx):
        '''
        Randomization is done by shuffling the members in the main channel
        and then spliting the list of members in half to form two teams.
        '''
        if client.mainChannel is not None:
            members = client.mainChannel.members
            if len(members) > 0: #TODO change 0 to 1 when done testing
                random.shuffle(members)
                half = len(members)//2
                client.team1 = members[0:half]
                client.team2 = members[half:len(members)]
                await printTeams(ctx)
            else:
                await ctx.send("There must be 2 or more people in the " + "<#" 
                + str(client.mainChannel.id) + ">" + " channel to use this command.")
        else:
            await ctx.send("You must first set the main channel before using this command")

    '''
    This command displays the members of team 1 and team 2.
    '''
    @client.command()
    async def showTeams(ctx):
        await printTeams(ctx)
        
    '''
    This command allows the user to select members to put in team 1.
    '''
    @client.command()
    async def makeTeam1(ctx, *args):
        await makeTeam(ctx, args, "one")

    '''
    This command allows the user to select members to put in team 2.
    '''
    @client.command()
    async def makeTeam2(ctx, *args):
        await makeTeam(ctx, args, "two")
    
    '''
    This function displays the members in team 1 and 2.
    '''
    async def printTeams(ctx):
        t1Members = []
        t2Members = []
        for member in client.team1:
            t1Members.append("<@" + str(member.id) + ">")
        for member in client.team2:
            t2Members.append("<@" + str(member.id) + ">")
        await ctx.send(":video_game: Team 1: " + ", ".join(map(str, t1Members)))
        await ctx.send(":video_game: Team 2: " + ", ".join(map(str, t2Members)))
    
    '''
    This function sets the team or main channels.
    '''
    async def setChannel(ctx, args, channel):
        channelName = " ".join(args)

        if channel == "one":
            team1 = discord.utils.get(ctx.guild.channels, name = channelName)
            if team1 is None:
                await ctx.send("Could not find a channel named \"" + channelName + "\" please try again.")
            elif str(team1.type) != "voice":
                await ctx.send("<#" + str(team1.id) + ">" + " is not a voice channel, you can only set voice channels.")
            else:
                client.team1Channel = team1
                await ctx.send("Team 1 channel set to " + "<#" + str(team1.id) + ">")
        elif channel == "two":
            team2= discord.utils.get(ctx.guild.channels, name = channelName)
            if team2 is None:
                await ctx.send("Could not find a channel named \"" + channelName + "\" please try again.")
            elif str(team2.type) != "voice":
                await ctx.send("<#" + str(team2.id) + ">" + " is not a voice channel, you can only set voice channels.")
            else:
                client.team2Channel = team2
                await ctx.send("Team 2 channel set to " + "<#" + str(team2.id) + ">")
        elif channel == "main":
            mainChannel = discord.utils.get(ctx.guild.channels, name = channelName)
            if mainChannel is None:
                await ctx.send("Could not find a channel named \"" + channelName + "\" please try again.")
            elif str(mainChannel.type) != "voice":
                await ctx.send("<#" + str(mainChannel.id) + ">" + " is not a voice channel, you can only set voice channels.")
            else:
                client.mainChannel = mainChannel
                await ctx.send("Main channel set to " + "<#" + str(mainChannel.id) + ">")

    '''
    This function puts members chosen by the user into teams.
    '''
    async def makeTeam(ctx, args, team):
        members = []
        for arg in args:
            try:
                memberID = int(arg[3:-1]) #Strips away characters to get id from <@id>
            except ValueError:
                await ctx.send("Error: you entered an invalid user id. Please tag users you want to add, for example: @userName")
                return

            member = ctx.guild.get_member(memberID)

            if member is None:
                await ctx.send("Error: could not find one or more selected users. Please tag users you want to add, " + 
                "for example: @userName. Please also seperate each tagged user with 1 space. ")
                return

            if not member in members:
                members.append(member)
            else:
                await ctx.send("Error: You can not add the same user to a team more than once.")
                return
              
        if team == "one":
            if not set(members).isdisjoint(client.team2):
                #Removes members in team 2 who are being added to team 1.
                client.team2 = list(set(client.team2) - set(members))
                await ctx.send("Note: some members have been moved from team 1 to team 2.")
            client.team1 = members
        elif team == "two":
            if not set(members).isdisjoint(client.team1):
                #Removes members in team 1 who are being added to team 2.
                client.team1 = list(set(client.team1) - set(members))
                await ctx.send("Note: some members have been moved from team 2 to team 1.")
            client.team2 = members
        await ctx.send("Teams successfully updated!")
        await printTeams(ctx)
        
    client.run(config.token)

if __name__ == "__main__":
    main()