'''
Code written by Ryan Helgoth, references I used have been cited in the comments.

This is file contains code for commands used by the bot.
'''

#TODO remove later
''' 
Link: https://stackoverflow.com/a/27365730
Author: Kevin
Date: Dec 8 '14 at 19:50
License: SA 3.0

I used this post to help fix an issue 
I had with importing "setup".
'''
import discord 
import random

#TODO
'''
-Move helperFunctions to new file called helperFunctions.py
-rename folder from helperFunctions to code
-split repeated parts into helper functions and put them in helperFunctions.py
-add comments
-change value from 0 to 1
-use format on strings
'''

def getDocRef(ctx, db):
    serverID = str(ctx.guild.id)
    userID = str(ctx.message.author.id)
    docRef = db.collection("servers").document(serverID).collection("users").document(userID)
    return docRef

'''
Displays help embed which contains a link explaining how to use the bot's commands.
'''
async def help(ctx):
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
This function displays the members in team 1 and 2.
'''
async def printTeams(ctx, db):
    teams = {"team1" : [], "team2" : []} #Keys are db vars and values are for holding user ids.
    docRef = getDocRef(ctx, db)
    doc = docRef.get()

    if doc.exists:
        data = doc.to_dict()
        for team in teams:
            teamName = "T" + team[1:4] + " " + team[-1] #Gets "Team X" string from "teamX" string.
            if team in data:
                teamMembers = data[team]
                for memberID in teamMembers:
                    try:
                        memberID = int(memberID) 
                    except ValueError:
                        await ctx.send("Error: {} is corrupted, please make {} again.".format(teamName)) 
                        return
                    
                    member = ctx.guild.get_member(memberID)
                    if member is None:
                        await ctx.send("Error: could not find one or more users, please make {} again.".format(teamName))
                        return
                    else:
                        teams[team].append("<@" + str(memberID) + ">")
            await ctx.send(":video_game: {}: {}".format(teamName, ", ".join(map(str, teams[team]))))
    else:
        await ctx.send("Could not find any saved teams, please create teams.")

'''
Randomly splits users from the main channel into 2 teams and saves them
in the database for the user who entered the command.
'''
async def randomizeMain(ctx, db):
    '''
    Randomization is done by shuffling the members in the main channel
    and then spliting the list of members in half to form two teams.
    '''
    docRef = getDocRef(ctx, db)
    doc = docRef.get()

    if doc.exists:
        data = doc.to_dict()
        if "voiceMain" in data:
            try:
                channelID = int(data["voiceMain"]) 
            except ValueError:
                await ctx.send("Error: main channel preference was corrupted, please set it again.") 
                return
            
            mainChannel = discord.utils.get(ctx.guild.channels, id = channelID) 
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
                    await printTeams(ctx, db)
                else:
                    await ctx.send("There must be 2 or more people in the " + "<#" 
                    + str(channelID) + ">" + " channel to use this command.") 
        else:
            await ctx.send("You must first set the main channel before using this command") 
    else:
        await ctx.send("You must first set the main channel before using this command")

'''
This function lets the user pick a preference for their main
channel and then saves it in the database. 
'''
async def setChannel(ctx, db, args, chat):
    channelName = " ".join(args)
    docRef = getDocRef(ctx, db)
    chats = {"Team 1" : "voice1", "Team 2" : "voice2", "Main" : "voiceMain"} #Values are the variable names in the db.
    channel = discord.utils.get(ctx.guild.channels, name = channelName)

    if channel is None:
        await ctx.send("Could not find a channel named \"" + channelName + "\" please try again.")
    elif str(channel.type) != "voice":
        await ctx.send("<#" + str(channel.id) + ">" + " is not a voice channel, you can only set voice channels.")
    else:
        data = {chats[chat] : str(channel.id)}
        docRef.set(data, merge = True)
        await ctx.send("{} channel set to ".format(chat) + "<#" + str(channel.id) + ">")

'''
This function lets the user make a team and then then saves the team 
in the database.
'''
async def makeTeam(ctx, db, args, teamName):
    docRef = getDocRef(ctx, db)
    doc = docRef.get()
    members = [] #NOTE this list now contains user id strings and not member objects.
    teams = {"Team 1" : "team1", "Team 2" : "team2"}
    teamRef = teams[teamName]

    #Populates members list with user id's 
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

    #Saves team to db
    if doc.exists:
        data = doc.to_dict()
        if teamRef in data:
            opposingTeamNum = str((int(teamRef[-1]) % 2) + 1) #Gets number of opposing team.
            opposingTeamName = "Team " + opposingTeamNum 
            opposingTeamRef = teams[opposingTeamName] #Gets db var name for opposing team
            opposingTeam = data[opposingTeamRef]
            if not set(members).isdisjoint(opposingTeam):
                #Removes members in the opposing team who are being added to team choosen by the user.
                opposingTeam = list(set(opposingTeam) - set(members))
                data = {opposingTeamRef : opposingTeam}
                docRef.set(data, merge = True)
                await ctx.send("Note: some members have been moved from {} to {}.".format(opposingTeamName.lower(), teamName.lower())) 
    
    data = {teamRef : members}
    docRef.set(data, merge = True)
    await ctx.send("Teams successfully updated to: ")
    await printTeams(ctx, db)

'''
Moves users to a voice channel set by the user.
'''
async def moveUsers(ctx, db, location):
    docRef = getDocRef(ctx, db)
    doc = docRef.get()

    if location == "teams":
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
                
                team1Channel = discord.utils.get(ctx.guild.channels, id = team1ID) 
                team2Channel = discord.utils.get(ctx.guild.channels, id = team2ID) 
                
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
    
    elif location == "main":
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