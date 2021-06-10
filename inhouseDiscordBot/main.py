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
        print("Bot is ready")
        print("----------------")


    @client.command()
    async def moveChat(ctx):
        await ctx.send("Feature currently under development.")


    
    client.run(config.token)


if __name__ == "__main__":
    main()