'''
Code written by Ryan Helgoth, references I used have been cited in the comments.

This is file contains code for commands used by the bot.
'''

''' 
Link: https://stackoverflow.com/a/27365730
Author: Kevin
Date: Dec 8 '14 at 19:50
License: SA 3.0

I used this post to help fix an issue 
I had with importing "commandHelpers".
'''
from . import commandHelpers as ch
import discord 
import random

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
    userID = ctx.message.author.id
    teams = {"team1" : [], "team2" : []} #Keys are db vars and values are for holding user ids.
    docRef = ch.getDocRef(ctx, db)
    doc = docRef.get()

    if doc.exists:
        data = doc.to_dict()
        for team in teams:
            error = False
            teamName = "T" + team[1:4] + " " + team[-1] #Gets "Team X" string from "teamX" string.
            if team in data:
                teamMembers = data[team]
                for memberID in teamMembers:
                    try:
                        memberID = int(memberID) 
                    except ValueError:
                        await ctx.send("Error: <@{0}>'s {1} is corrupted, please make your {1} again.".format(userID, teamName.lower())) 
                        error = True
                        break #Trys to show team 2 even if there is an error with team 1
                    
                    member = ctx.guild.get_member(memberID)
                    if member is None:
                        await ctx.send("Error: could not find one or more users in <@{0}>'s {1}, please make your {1} again.".format(userID, teamName.lower()))
                        error = True
                        break #Trys to show team 2 even if there is an error with team 1
                    else:
                        teams[team].append("<@" + str(memberID) + ">")
            if not error:
                await ctx.send("<@{0}>'s :video_game: {1}: {2}".format(userID, teamName, ", ".join(map(str, teams[team]))))
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
    userID = ctx.message.author.id
    docRef = ch.getDocRef(ctx, db)
    doc = docRef.get()

    if doc.exists:
        data = doc.to_dict()
        if "voiceMain" in data:
            try:
                channelID = int(data["voiceMain"]) 
            except ValueError:
                await ctx.send("Error: <@{}>'s main channel preference was corrupted, please set it again.".format(userID)) 
                return
            
            mainChannel = discord.utils.get(ctx.guild.channels, id = channelID) 
            if mainChannel is None:
                await ctx.send("Error: couldn't find <@{}>'s main channel, please try setting it again.".format(userID)) 
            else:
                members = mainChannel.members
                memberIDS = [str(member.id) for member in members]
                if len(memberIDS) > 1: 
                    random.shuffle(memberIDS)
                    half = len(memberIDS) // 2
                    team1 = memberIDS[0:half]
                    team2 = memberIDS[half:len(memberIDS)]
                    data = {"team1" : team1, "team2" : team2}
                    docRef.set(data, merge = True)
                    await ctx.send("Random teams were made from users in <#{}>:".format(channelID))  
                    await printTeams(ctx, db)
                else:
                    await ctx.send("There must be 2 or more people in the <#{}> channel to use this command.".format(channelID)) 
        else:
            await ctx.send("You must first set your main channel preference before using this command.") 
    else:
        await ctx.send("You must first set your main channel preference before using this command.")

'''
This function lets the user pick a preference for their main
channel and then saves it in the database. 
'''
async def setChannel(ctx, db, args, chat):
    userID = ctx.message.author.id
    channelName = " ".join(args)
    docRef = ch.getDocRef(ctx, db)
    chats = {"Team 1" : "voice1", "Team 2" : "voice2", "Main" : "voiceMain"} #Values are the variable names in the db.
    channel = discord.utils.get(ctx.guild.channels, name = channelName)

    if channel is None:
        await ctx.send("Could not find a channel named \"{}\" please try again.".format(channelName))
    elif str(channel.type) != "voice":
        await ctx.send("<#{}> is not a voice channel, you can only set voice channels.".format(channel.id))
    else:
        data = {chats[chat] : str(channel.id)}
        docRef.set(data, merge = True)
        await ctx.send("<@{}>'s {} channel set to <#{}>".format(userID, chat.lower(), channel.id))

'''
This function lets the user make a team and then then saves the team 
in the database.
'''
async def makeTeam(ctx, db, args, teamName):
    userID = ctx.message.author.id
    docRef = ch.getDocRef(ctx, db)
    doc = docRef.get()
    members = [] #NOTE this list now contains user id strings and not member objects.
    teams = {"Team 1" : "team1", "Team 2" : "team2"}
    teamRef = teams[teamName]

    #Populates members list with user id's 
    for arg in args:
        try:
            memberID = int(arg[3:-1]) #Strips away characters to get id from <@id>
        except ValueError:
            await ctx.send("Error: you entered an invalid user. Please tag users you want to add by typing \"@\" and selecting users.")
            return
        
        member = ctx.guild.get_member(memberID)
        if member is None:
            await ctx.send("Error: could not find one or more selected users. Please tag users you want to add, " + 
            "by typing \"@\" and selecting users. Please also seperate each tagged user with 1 space.")
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
                await ctx.send("Note: some members have been moved from <@{0}>'s {1} to <@{0}>'s {2}.".format(userID, opposingTeamName.lower(), teamName.lower())) 
    
    data = {teamRef : members}
    docRef.set(data, merge = True)
    await ctx.send("Teams successfully updated to: ")
    await printTeams(ctx, db)

'''
Moves users to a voice channel set by the user.
'''
async def moveToChannel(ctx, db, location):
    docRef = ch.getDocRef(ctx, db)
    doc = docRef.get()
    teams = {"team1" : "voice1", "team2" : "voice2"} #Keys are db var names for lists of member ids and values are db vars for channel ids.

    if location == "teams":
        await ch.sendToTeams(ctx, doc, teams)
    elif location == "main":
        await ch.sendToMain(ctx, doc, teams)
