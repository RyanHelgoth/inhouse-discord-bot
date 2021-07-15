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
    userID = ctx.message.author.id
    if doc.exists:
        data = doc.to_dict()
        if "voice1" in data and "voice2" in data and "team1" in data and "team2" in data:
            for team in teams:
                channelRef = teams[team]
                teamName = team[:4] + " " + team[-1] #Gets "team X" string from "teamX" string. 
                try:
                    channelID = int(data[channelRef]) 
                except ValueError:
                    await ctx.send("Error: <@{}>'s {} channel preference was corrupted, please set it again.".format(userID, teamName)) 
                    continue #Trys move team 2 to their channel even if the team 1 has a corrupt channel id.

                teamChannel = discord.utils.get(ctx.guild.channels, id = channelID) 
                if teamChannel is None:
                    await ctx.send("Error: couldn't find <@{}>'s {} channel, please try setting it again.".format(userID, teamName)) 
                else:
                    teamMembers = data[team]
                    await moveUsers(ctx, teamMembers, teamName, teamChannel, channelID)
        else:
            await ctx.send("You must first set your team 1, team 2, team 1 channel and team 2 channel before using this command.")
    else:
        await ctx.send("You must first set team 1, team 2, team 1 channel and team 2 channel before using this command.")

'''
Moves team members to the main channel.
'''
async def sendToMain(ctx, doc, teams):
    userID = ctx.message.author.id
    if doc.exists:
        data = doc.to_dict()
        if "voiceMain" in data and "team1" in data and "team2" in data:
            try:
                channelID = int(data["voiceMain"]) 
            except ValueError:
                await ctx.send("Error: <@{}>'s main channel preference was corrupted, please set it again.".format(userID)) 
                return
            
            mainChannel = discord.utils.get(ctx.guild.channels, id = channelID) 
            if mainChannel is None:
                await ctx.send("Error: couldn't find <@{}>'s main channel, please try setting it again.".format(userID)) 
            else:
                for team in teams:
                    teamMembers = data[team]
                    teamName = team[0:4] + " " + team[-1] #Gets "Team X" string from "teamX" string. 
                    await moveUsers(ctx, teamMembers, teamName, mainChannel, channelID)
        else:
            await ctx.send("You must first set your team 1, team 2 and main channel before using this command.")
    else:
        await ctx.send("You must first set your team 1, team 2 and main channel before using this command.")

'''
Moves given users to the given channel.
'''
async def moveUsers(ctx, teamMembers, teamName, channel, channelID):
    userID = ctx.message.author.id
    for memberID in teamMembers:
        try:
            memberID = int(memberID) 
        except ValueError:
            await ctx.send("Error: a user's id on <@{0}>'s {1} is corrupted and they could not be moved to <#{2}>, please make {1} again.".format(userID, teamName, channelID)) 
            continue #Trys to move other users to a channel even if some user's ids are corrupt.

        member = ctx.guild.get_member(memberID)
        if member is None:
            await ctx.send("Error: a user in <@{0}>'s {1} could not be found and was not be moved to <#{2}>, please make {1} again.".format(userID, teamName, channelID))
            continue #Trys to move other users to a channel even if some users can't be found.
        else:
            try:
                await member.move_to(channel)
                await ctx.send("Moved <@{}> to <#{}>".format(memberID, channelID))
            except discord.HTTPException:
                await ctx.send("Error: Unable to move <@{}> to <#{}>".format(memberID, channelID)) 