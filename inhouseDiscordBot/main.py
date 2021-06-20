'''
Code written by Ryan Helgoth


'''

import discord 
from discord.ext import commands
import config


def main():
    client = commands.Bot(command_prefix = "!")

    #using global varibles for now until I set up a database
    client.mainChannel = None
    client.team1Channel = None
    client.team2Channel = None


    @client.event
    async def on_ready():
        print("Bot has come online")

    


    @client.command()
    async def moveToTeams(ctx):
        #TODO need to assign users to teams
        print(client.team1Channel)
        if not None in (client.team1Channel, client.team2Channel, client.mainChannel):
            members = client.mainChannel.members
            for member in members:
                await member.move_to(client.team1Channel)
                await ctx.send("Moved " + member.name + " from " + client.mainChannel.name + " to " + client.team1Channel.name)
        else:
            await ctx.send("You must first set team and main channels before using this command")

    @client.command()
    async def moveToMain(ctx):
        
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
    
    client.run(config.token)


if __name__ == "__main__":
    main()