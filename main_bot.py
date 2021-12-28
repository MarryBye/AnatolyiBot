import discord
from discord.ext import commands
import asyncio

import functions as fnc

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Я гей')

@client.event
async def on_message(msg):

  user = msg.author
  channel = msg.channel
  messageIsPrivate = (str(channel.type) == 'private')
  guild = msg.guild
  content = msg.content
  
  if msg.author.bot:
    return

  if messageIsPrivate and content != '':
    await fnc.addToLogFile("[PRIVATE] {0}: {1}".format(user.name, content), 'private')
    return

  await fnc.addToLogFile('[{0}] {1}: {2}'.format(channel.name, user.name, content))

@client.event
async def on_member_join(member):
    pass

@client.event
async def on_member_remove(member):
    pass

client.run('OTI1MzMxNDg3MDUyNjg5NDM5' + '.YcrkGg.pVgr0ymuGtk7PJ' + 'HxegenmdhVCFA')
