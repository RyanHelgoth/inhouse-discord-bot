'''
Code written by Ryan Helgoth


'''

import discord 
from discord.ext import commands
import config
import random

#TODO organize code better
#TODO bug where user in main chat is not found if bot comes online after they joined
#TODO deal with adding users to team who are offline
#TODO make function for move to main/teams

def main():
    #https://stackoverflow.com/a/67145571
    botInfo = discord.Activity(type=discord.ActivityType.watching, name="for !inhouseHelp command")
    client = commands.Bot(command_prefix = "!", activity = botInfo, help_command = None)

    
    

    #using global varibles for now until I set up a database
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

    @client.command()
    async def inhouseHelp(ctx):
        #https://stackoverflow.com/a/64529788
        help = discord.Embed()
        help.title = "Inhouse Bot Help"
        help.description = ":keyboard: [Help and list of commands here!](https://github.com/RyanHelgoth/inhouse-discord-bot#how-do-you-use-the-bot)"
        await ctx.send(embed = help)

    @client.command()
    async def moveToTeams(ctx):
        if not None in (client.team1Channel, client.team2Channel, client.mainChannel):
            if len(client.team1) > 0 and len(client.team2) > 0:
                for member in client.team1:
                    try:
                        await member.move_to(client.team1Channel)
                        await ctx.send("Moved " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.team1Channel) + ">")
                    except discord.HTTPException:
                        await ctx.send("Error: Unable to move " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.team1Channel) + ">")
        
                for member in client.team2:
                    try:
                        await member.move_to(client.team2Channel)
                        await ctx.send("Moved " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.team2Channel) + ">")
                    except discord.HTTPException:
                        await ctx.send("Error: Unable to move " + "<@" + str(member.id) + ">" + " to " + "<#" + str(client.team2Channel) + ">")
            else:
                await ctx.send("Please populate teams before using this command.")
        else:
            await ctx.send("You must first set team and main channels before using this command")

    @client.command()
    async def moveToMain(ctx):
        
        # Checks that channels have been set 
        if not None in (client.team1Channel, client.team2Channel, client.mainChannel):
            if len(client.team1) > 0 and len(client.team2) > 0:
                for member in client.team1:
                    #Make into function to avoid repetition?
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
            await ctx.send("You must first set team and main channels before using this command")

    #TODO allow setting channels with multiple spaces (need to use qoutes)
    #TODO check that channel exists
    #TODO deal with channels withh the same name

    @client.command()
    async def setTeam1(ctx, *args):
        await setChannel(ctx, args, "one")
     

    @client.command()
    async def setTeam2(ctx, *args):
        await setChannel(ctx, args, "two")

    @client.command()
    async def setMain(ctx, *args):
        await setChannel(ctx, args, "main")

    @client.command()
    async def randomize(ctx):
        if not None in (client.team1Channel, client.team2Channel, client.mainChannel):
            members = client.mainChannel.members
            if len(members) > 0: #change 0 to 1 when done testing
                random.shuffle(members)
                half = len(members)//2
                client.team1 = members[0:half]
                client.team2 = members[half:len(members)]
                await printTeams(ctx)
            else:
                await ctx.send("There must be 2 or more people in the " + "<#" 
                + str(client.mainChannel.id) + ">" + " channel to use this command.")
        else:
            await ctx.send("You must first set team and main channels before using this command")

    @client.command()
    async def showTeams(ctx):
        await printTeams(ctx)
        
    @client.command()
    async def makeTeam1(ctx, *args):
        await makeTeam(ctx, args, "one")

    @client.command()
    async def makeTeam2(ctx, *args):
        await makeTeam(ctx, args, "two")
    
    async def printTeams(ctx):
        t1Members = []
        t2Members = []
        for member in client.team1:
            t1Members.append("<@" + str(member.id) + ">")
        for member in client.team2:
            t2Members.append("<@" + str(member.id) + ">")
        await ctx.send(":video_game: Team 1: " + ", ".join(map(str, t1Members)))
        await ctx.send(":video_game: Team 2: " + ", ".join(map(str, t2Members)))
        
    async def setChannel(ctx, args, channel):
        channelName = " ".join(args)
        
        if channel== "one":
            team1 = discord.utils.get(ctx.guild.channels, name = channelName) #TODO look into guild.get_channel instead
            if team1 == None:
                await ctx.send("Could not find a channel named \"" + channelName + "\" please try again.")
            elif str(team1.type) != "voice":
                await ctx.send("<#" + str(team1.id) + ">" + " is not a voice channel, you can only set voice channels.")
            else:
                client.team1Channel = team1
                await ctx.send("Team 1 channel set to " + "<#" + str(team1.id) + ">")
        elif channel == "two":
            team2= discord.utils.get(ctx.guild.channels, name = channelName)
            if team2 == None:
                await ctx.send("Could not find a channel named \"" + channelName + "\" please try again.")
            elif str(team2.type) != "voice":
                await ctx.send("<#" + str(team2.id) + ">" + " is not a voice channel, you can only set voice channels.")
            else:
                client.team2Channel = team2
                await ctx.send("Team 2 channel set to " + "<#" + str(team2.id) + ">")
        elif channel == "main":
            mainChannel = discord.utils.get(ctx.guild.channels, name = channelName)
            if mainChannel == None:
                await ctx.send("Could not find a channel named \"" + channelName + "\" please try again.")
            elif str(mainChannel.type) != "voice":
                await ctx.send("<#" + str(mainChannel.id) + ">" + " is not a voice channel, you can only set voice channels.")
            else:
                client.mainChannel = mainChannel
                await ctx.send("Main channel set to " + "<#" + str(mainChannel.id) + ">")

    #TODO Need error checking to make sure args are valid members
    async def makeTeam(ctx, args, team):
        members = []
        for arg in args:
            memberID = arg[3:-1] #Strips away characters to get id from <@id>
            
            #TODO use more specific exception
            try:
                member = await ctx.guild.fetch_member(memberID)
            except:
                await ctx.send("Error finding selected users. Please seperate each tagged user with 1 space.")
                return

            if member != None:
                members.append(member)
            elif member == None:
                await ctx.send("One or more users you entered were not found on this server. Please tag users you want to add, for example: @userName")
                return
            
        if team == "one":
            if not set(members).isdisjoint(client.team2):
                client.team2 = list(set(client.team2) - set(members))
                await ctx.send("Note: some members have been moved from team 1 to team 2.")
            client.team1 = members
            
        elif team == "two":
            if not set(members).isdisjoint(client.team1):
                client.team1 = list(set(client.team1) - set(members))
                await ctx.send("Note: some members have been moved from team 2 to team 1.")
            client.team2 = members
        await ctx.send("Teams successfully updated!")
        await printTeams(ctx)
        

    client.run(config.token)


if __name__ == "__main__":
    main()