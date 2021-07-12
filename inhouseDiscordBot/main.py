'''
Code written by Ryan Helgoth, references I used have been cited in the comments.

This is file contains the code that runs the bot.
'''

import discord 
from discord.ext import commands
import config
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#TODO test moving offline users to a channel
#TODO make function for move to main/teams
#TODO move functions into seperate file
#TODO deal with channels withh the same name
#TODO get rid of client vars
#TODO update firestore security settings

def main():
    cred = credentials.Certificate("firebaseKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()


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
        serverID = str(ctx.guild.id)
        userID = str(ctx.message.author.id)
        docRef = db.collection("servers").document(serverID).collection("users").document(userID)
        doc = docRef.get()

        if doc.exists:
            data = doc.to_dict()
            if "voice1" in data and "voice2" in data and "team1" in data and "team2" in data:
                try:
                    team1ID = int(data["voice1"]) 
                except ValueError:
                    await ctx.send("Error: team 1 channel preference was corrupted, please set it again.") 
                    return

                try:
                    team2ID = int(data["voice2"]) 
                except ValueError:
                    await ctx.send("Error: team 2 channel preference was corrupted, please set it again.") 
                    return
                
                team1Channel = discord.utils.get(ctx.guild.channels, id = team1ID) #Returns None if channel is not found
                team2Channel = discord.utils.get(ctx.guild.channels, id = team2ID) #Returns None if channel is not found
                
                if team1Channel is None:
                    await ctx.send("Error: couldn't find team 1 channel, please try setting it again.") 
                elif team2Channel is None:
                    await ctx.send("Error: couldn't find team 2 channel, please try setting it again.") 
                else:
                    team1 = data["team1"]
                    team2 = data["team2"]
                    for memberID in team1:
                        try:
                            memberID = int(memberID) 
                        except ValueError:
                            await ctx.send("Error: team 1 is corrupted, please make team 1 again.") 
                            return

                        member = ctx.guild.get_member(memberID)
                        if member is None:
                            await ctx.send("Error: could not find one or more users, please make team 1 again.")
                            return

                        try:
                            await member.move_to(team1Channel)
                            await ctx.send("Moved " + "<@" + str(memberID) + ">" + " to " + "<#" + str(team1ID) + ">")
                        except discord.HTTPException:
                            await ctx.send("Error: Unable to move " + "<@" + str(memberID) + ">" + " to " + "<#" + str(team1ID) + ">") 
                    
                    for memberID in team2:
                        try:
                            memberID = int(memberID) 
                        except ValueError:
                            await ctx.send("Error: team 2 is corrupted, please make team 2 again.") 
                            return

                        member = ctx.guild.get_member(memberID)
                        if member is None:
                            await ctx.send("Error: could not find one or more users, please make team 2 again.")
                            return

                        try:
                            await member.move_to(team2Channel)
                            await ctx.send("Moved " + "<@" + str(memberID) + ">" + " to " + "<#" + str(team2ID) + ">")
                        except discord.HTTPException:
                            await ctx.send("Error: Unable to move " + "<@" + str(memberID) + ">" + " to " + "<#" + str(team2ID) + ">") 
            else:
                await ctx.send("You must first set team 1, team 2, team 1 channel and team 2 channel before using this command.")
        else:
            await ctx.send("You must first set team 1, team 2, team 1 channel and team 2 channel before using this command.")

    '''
    This command moves the users in teams to the main channel.
    '''
    @client.command()
    async def moveToMain(ctx):
        serverID = str(ctx.guild.id)
        userID = str(ctx.message.author.id)
        docRef = db.collection("servers").document(serverID).collection("users").document(userID)
        doc = docRef.get()

        if doc.exists:
            data = doc.to_dict()
            if "voiceMain" in data and "team1" in data and "team2" in data:
                try:
                    channelID = int(data["voiceMain"]) 
                except ValueError:
                    await ctx.send("Error: main channel preference was corrupted, please set it again.") 
                    return
                
                mainChannel = discord.utils.get(ctx.guild.channels, id = channelID) #Returns None if channel is not found
                if mainChannel is None:
                    await ctx.send("Error: couldn't find mainChannel, please try setting it again.") 
                else:
                    team1 = data["team1"]
                    team2 = data["team2"]
                    for memberID in team1:
                        try:
                            memberID = int(memberID) 
                        except ValueError:
                            await ctx.send("Error: team 1 is corrupted, please make team 1 again.") 
                            return

                        member = ctx.guild.get_member(memberID)
                        if member is None:
                            await ctx.send("Error: could not find one or more users, please make team 1 again.")
                            return

                        try:
                            await member.move_to(mainChannel)
                            await ctx.send("Moved " + "<@" + str(memberID) + ">" + " to " + "<#" + str(channelID) + ">")
                        except discord.HTTPException:
                            await ctx.send("Error: Unable to move " + "<@" + str(memberID) + ">" + " to " + "<#" + str(channelID) + ">") 
                    
                    for memberID in team2:
                        try:
                            memberID = int(memberID) 
                        except ValueError:
                            await ctx.send("Error: team 2 is corrupted, please make team 2 again.") 
                            return

                        member = ctx.guild.get_member(memberID)
                        if member is None:
                            await ctx.send("Error: could not find one or more users, please make team 2 again.")
                            return

                        try:
                            await member.move_to(mainChannel)
                            await ctx.send("Moved " + "<@" + str(memberID) + ">" + " to " + "<#" + str(channelID) + ">")
                        except discord.HTTPException:
                            await ctx.send("Error: Unable to move " + "<@" + str(memberID) + ">" + " to " + "<#" + str(channelID) + ">") 
            else:
                await ctx.send("You must first set team 1, team 2 and the main channel before using this command.")
        else:
            await ctx.send("You must first set team 1, team 2 and the main channel before using this command.")


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
        serverID = str(ctx.guild.id)
        userID = str(ctx.message.author.id)
        docRef = db.collection("servers").document(serverID).collection("users").document(userID)
        doc = docRef.get()

        if doc.exists:
            data = doc.to_dict()
            if "voiceMain" in data:
                '''
                Channel IDs should always be integers, but I put this try block 
                here just in case the data gets corrupted somehow leading to a non-numerical ID.
                '''
                try:
                    channelID = int(data["voiceMain"]) 
                except ValueError:
                    await ctx.send("Error: main channel preference was corrupted, please set it again.") 
                    return
                
                mainChannel = discord.utils.get(ctx.guild.channels, id = channelID) #Returns None if channel is not found
                if mainChannel is None:
                    await ctx.send("Error: couldn't find mainChannel, please try setting it again.") 
                else:
                    members = mainChannel.members
                    memberIDS = [str(member.id) for member in members]
                    if len(memberIDS) > 0: #TODO change 0 to 1 when done testing
                        random.shuffle(memberIDS)
                        half = len(memberIDS)//2
                        team1 = memberIDS[0:half]
                        team2 = memberIDS[half:len(memberIDS)]
                        data = {"team1" : team1, "team2" : team2}
                        docRef.set(data, merge = True)
                        await printTeams(ctx)
                    else:
                        await ctx.send("There must be 2 or more people in the " + "<#" 
                        + str(channelID) + ">" + " channel to use this command.")
            else:
                await ctx.send("You must first set the main channel before using this command") 
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

        serverID = str(ctx.guild.id)
        userID = str(ctx.message.author.id)
        docRef = db.collection("servers").document(serverID).collection("users").document(userID)
        doc = docRef.get()
    
        if doc.exists:
            data = doc.to_dict()
            
            #TODO check that user exits?
            if "team1" in data:
                team1 = data["team1"]
                for memberID in team1:
                    t1Members.append("<@" + memberID + ">")

            if "team2" in data:
                team2 = data["team2"]
                for memberID in team2:
                    t2Members.append("<@" + memberID + ">")
        
        
        await ctx.send(":video_game: Team 1: " + ", ".join(map(str, t1Members)))
        await ctx.send(":video_game: Team 2: " + ", ".join(map(str, t2Members)))
    
    '''
    This function sets the team or main channels.
    '''
    async def setChannel(ctx, args, channel):
        channelName = " ".join(args)
        serverID = str(ctx.guild.id)
        userID = str(ctx.message.author.id)
        docRef = db.collection("servers").document(serverID).collection("users").document(userID)

        if channel == "one":      
            team1 = discord.utils.get(ctx.guild.channels, name = channelName)
            if team1 is None:
                await ctx.send("Could not find a channel named \"" + channelName + "\" please try again.")
            elif str(team1.type) != "voice":
                await ctx.send("<#" + str(team1.id) + ">" + " is not a voice channel, you can only set voice channels.")
            else:
                

                data = {"voice1" : str(team1.id)}
                docRef.set(data, merge = True)

                await ctx.send("Team 1 channel set to " + "<#" + str(team1.id) + ">")
        elif channel == "two":
            team2 = discord.utils.get(ctx.guild.channels, name = channelName)
            if team2 is None:
                await ctx.send("Could not find a channel named \"" + channelName + "\" please try again.")
            elif str(team2.type) != "voice":
                await ctx.send("<#" + str(team2.id) + ">" + " is not a voice channel, you can only set voice channels.")
            else:
                

                data = {"voice2" : str(team2.id)}
                docRef.set(data, merge = True)

                await ctx.send("Team 2 channel set to " + "<#" + str(team2.id) + ">")
        elif channel == "main":
            mainChannel = discord.utils.get(ctx.guild.channels, name = channelName)
            if mainChannel is None:
                await ctx.send("Could not find a channel named \"" + channelName + "\" please try again.")
            elif str(mainChannel.type) != "voice":
                await ctx.send("<#" + str(mainChannel.id) + ">" + " is not a voice channel, you can only set voice channels.")
            else:
                
                
                
                #https://cloud.google.com/firestore/docs/manage-data/add-data#set_a_document
                
                #Saves user's channel setting in db
                data = {"voiceMain" : str(mainChannel.id)}
                docRef.set(data, merge = True)
                
                await ctx.send("Main channel set to " + "<#" + str(mainChannel.id) + ">")

    '''
    This function puts members chosen by the user into teams.
    '''
    async def makeTeam(ctx, args, team):
        serverID = str(ctx.guild.id)
        userID = str(ctx.message.author.id)
        docRef = db.collection("servers").document(serverID).collection("users").document(userID)
        doc = docRef.get()
        members = []#NOTE members now contains user id string and not members objects

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
                members.append(str(member.id))
            else:
                await ctx.send("Error: You can not add the same user to a team more than once.")
                return
              
        if team == "one":
            if doc.exists:
                data = doc.to_dict()

                #TODO maybe check if members exist
                if "team2" in data:
                    team2 = data["team2"]
                    if not set(members).isdisjoint(team2):
                        #Removes members in team 2 who are being added to team 1.
                        team2 = list(set(team2) - set(members))
                        team2Data = {"team2" : team2}
                        docRef.set(team2Data, merge = True)
                        await ctx.send("Note: some members have been moved from team 1 to team 2.")
            
            
            
            data = {"team1" : members}
            docRef.set(data, merge = True)
                    
        elif team == "two":
            if doc.exists:
                data = doc.to_dict()

                if "team1" in data:
                    team1 = data["team1"]
                    if not set(members).isdisjoint(team1):
                        #Removes members in team 1 who are being added to team 2.
                        team1 = list(set(team1) - set(members))
                        team1Data = {"team1" : team1}
                        docRef.set(team1Data, merge = True)
                        await ctx.send("Note: some members have been moved from team 2 to team 1.")
            
            
            
            data = {"team2" : members}
            docRef.set(data, merge = True)

        await ctx.send("Teams successfully updated!")
        await printTeams(ctx)
        
    client.run(config.token)

if __name__ == "__main__":
    main()