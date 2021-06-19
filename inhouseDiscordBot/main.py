'''
Code written by Ryan Helgoth


'''

import discord 
from discord.ext import commands
import config


def main():
    client = commands.Bot(command_prefix = "!")

    @client.event
    async def on_ready():
        print("Bot has come online")



    @client.command()
    async def moveToTeams(ctx):
        mainChannel = discord.utils.get(ctx.guild.channels, name="Main")
        teamChannel = discord.utils.get(ctx.guild.channels, name="team-a")
        members = mainChannel.members
        for member in members:
            await member.move_to(teamChannel)
            await ctx.send("Moved " + member.name + " from " + mainChannel.name + " to " + teamChannel.name)

    @client.command()
    async def moveToMain(ctx):
        mainChannel = discord.utils.get(ctx.guild.channels, name="Main")
        teamAChannel = discord.utils.get(ctx.guild.channels, name="team-a")
        teamBChannel = discord.utils.get(ctx.guild.channels, name="team-b")
        aMembers = teamAChannel.members
        bMembers = teamBChannel.members
        for member in aMembers:
            await member.move_to(mainChannel)
        for member in bMembers:
            await member.move_to(mainChannel)
        await ctx.send("Moved all users from " + teamAChannel.name + " and " + teamBChannel.name + " to " + mainChannel.name)
    
    client.run(config.token)


if __name__ == "__main__":
    main()