'''
Code written by Ryan Helgoth, references I used have been cited in the comments.

This is file contains helper functions used by commands.py.
'''

import discord

'''
Gets the doc ref to a user's data.
'''
def getDocRef(ctx, db):
    serverID = str(ctx.guild.id)
    userID = str(ctx.message.author.id)
    docRef = db.collection("servers").document(serverID).collection("users").document(userID)
    return docRef

'''
Moves team members to their corresponding team channels.
'''
async def sendToTeams(ctx, doc, teams):
    if doc.exists:
        data = doc.to_dict()
        if "voice1" in data and "voice2" in data and "team1" in data and "team2" in data:
            for team in teams:
                channelRef = teams[team]
                teamName = team[0:4] + " " + team[-1] #Gets "Team X" string from "teamX" string. 
                try:
                    channelID = int(data[channelRef]) 
                except ValueError:
                    await ctx.send("Error: {} channel preference was corrupted, please set it again.".format(teamName)) 
                    continue #Trys move team 2 to their channel even if the team 1 has a corrupt channel id.

                teamChannel = discord.utils.get(ctx.guild.channels, id = channelID) 
                if teamChannel is None:
                    await ctx.send("Error: couldn't find {} channel, please try setting it again.".format(teamName)) 
                else:
                    teamMembers = data[team]
                    await moveUsers(ctx, teamMembers, teamName, teamChannel, channelID)
        else:
            await ctx.send("You must first set team 1, team 2, team 1 channel and team 2 channel before using this command.")
    else:
        await ctx.send("You must first set team 1, team 2, team 1 channel and team 2 channel before using this command.")

'''
Moves team members to the main channel.
'''
async def sendToMain(ctx, doc, teams):
    if doc.exists:
        data = doc.to_dict()
        if "voiceMain" in data and "team1" in data and "team2" in data:
            try:
                channelID = int(data["voiceMain"]) 
            except ValueError:
                await ctx.send("Error: main channel preference was corrupted, please set it again.") 
                return
            
            mainChannel = discord.utils.get(ctx.guild.channels, id = channelID) 
            if mainChannel is None:
                await ctx.send("Error: couldn't find mainChannel, please try setting it again.") 
            else:
                for team in teams:
                    teamMembers = data[team]
                    teamName = team[0:4] + " " + team[-1] #Gets "Team X" string from "teamX" string. 
                    await moveUsers(ctx, teamMembers, teamName, mainChannel, channelID)
        else:
            await ctx.send("You must first set team 1, team 2 and the main channel before using this command.")
    else:
        await ctx.send("You must first set team 1, team 2 and the main channel before using this command.")

'''
Moves given users to the given channel.
'''
async def moveUsers(ctx, teamMembers, teamName, channel, channelID):
    for memberID in teamMembers:
        try:
            memberID = int(memberID) 
        except ValueError:
            await ctx.send("Error: a user's id on {} is corrupted and they could not be moved to <#{}>, please make {} again.".format(teamName, channelID, teamName)) 
            continue #Trys to move other users to a channel even if some user's ids are corrupt.

        member = ctx.guild.get_member(memberID)
        if member is None:
            await ctx.send("Error: a user in {} could not be found and was not be moved to <#{}>".format(teamName, channelID))
            continue #Trys to move other users to a channel even if some users can't be found.
        else:
            try:
                await member.move_to(channel)
                await ctx.send("Moved " + "<@" + str(memberID) + ">" + " to " + "<#" + str(channelID) + ">")
            except discord.HTTPException:
                await ctx.send("Error: Unable to move " + "<@" + str(memberID) + ">" + " to " + "<#" + str(channelID) + ">") 