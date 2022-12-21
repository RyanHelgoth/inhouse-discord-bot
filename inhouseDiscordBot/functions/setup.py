'''
Code written by Ryan Helgoth, references I used have been cited in the comments.

This is file contains functions used for setup of the bot and the database.
'''

import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials 
from firebase_admin import firestore
import os

'''
This function sets up the bot and returns the bot client.
'''
def getClient():
    ''' 
    Link: https://stackoverflow.com/a/65368556
    Author: kubaki18
    Date: Dec 19 '20 at 9:54
    License: SA 4.0

    I used this post to help fix a bug in which members
    were not found in voice channels due to not having the 
    members intent enabled.
    '''
    intents = discord.Intents().all()
    intents.members = True
    botInfo = discord.Activity(type=discord.ActivityType.watching, name = "for !inhousehelp command")
    client = commands.Bot(command_prefix = "!", activity = botInfo, help_command = None, intents = intents, reconnect = True)
    return client

'''
This object sets up the db and returns the db object.
'''
def getDB():
    keyPath = os.path.join("tokens", "firebaseKey.json")
    cred = credentials.Certificate(keyPath)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db