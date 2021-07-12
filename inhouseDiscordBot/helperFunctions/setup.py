
import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials 
from firebase_admin import firestore




def getClient():
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
    return client

def getDB():
    cred = credentials.Certificate("tokens\\firebaseKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db