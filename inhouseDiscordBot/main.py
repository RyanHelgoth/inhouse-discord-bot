'''
Code written by Ryan Helgoth


'''

import discord 
from discord.ext import commands
import config
import random


def main():
    client = commands.Bot(command_prefix = "!")

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



    @client.command()
    async def moveToTeams(ctx):
        print(client.team1Channel)
        if not None in (client.team1Channel, client.team2Channel, client.mainChannel):
            if len(client.team1) > 0 and len(client.team2) > 0:
                for member in client.team1:
                    await member.move_to(client.team1Channel)
                    await ctx.send("Moved " + member.name + " from " + client.mainChannel.name + " to " + client.team1Channel.name)
                for member in client.team2:
                    await member.move_to(client.team2Channel)
                    await ctx.send("Moved " + member.name + " from " + client.mainChannel.name + " to " + client.team2Channel.name)
            else:
                await ctx.send("Please populate teams before using this command.")
        else:
            await ctx.send("You must first set team and main channels before using this command")

    @client.command()
    async def moveToMain(ctx):
        
        # Checks that channels have been set 
        if not None in (client.team1Channel, client.team2Channel, client.mainChannel):
            team1Members = client.team1Channel.members
            team2Members = client.team1Channel.members
            for member in team1Members:
                await member.move_to(client.mainChannel)
            for member in team2Members:
                await member.move_to(client.mainChannel)
            await ctx.send("Moved all users from " + client.team1Channel.name + " and " + client.team2Channel.name + " to " + client.mainChannel.name)
        else:
            await ctx.send("You must first set team and main channels before using this command")

    @client.command()
    async def setTeam1(ctx, channelName):
        client.team1Channel = discord.utils.get(ctx.guild.channels, name = channelName)
        

    @client.command()
    async def setTeam2(ctx, channelName):
        client.team2Channel = discord.utils.get(ctx.guild.channels, name = channelName)

    @client.command()
    async def setMain(ctx, channelName):
        client.mainChannel = discord.utils.get(ctx.guild.channels, name = channelName)

    @client.command()
    async def randomize(ctx):
        if not None in (client.team1Channel, client.team2Channel, client.mainChannel):
            members = client.mainChannel.members
            if len(members) > 1:
                random.shuffle(members)
                half = len(members)//2
                client.team1 = members[0:half]
                client.team2 = members[half:len(members)]
                '''
                print("Left list: " + str(team1))
                print("Right list: " + str(team2))
                '''
            else:
                await ctx.send("There must be 2 or more people in the " + client.mainChannel.name + " channel to use this command.")
        else:
            await ctx.send("You must first set team and main channels before using this command")
    
    client.run(config.token)


if __name__ == "__main__":
    main()