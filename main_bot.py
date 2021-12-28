import discord
from discord.ext import commands
import asyncio

import functions as fnc

intents = discord.Intents.all()
client = discord.Client(intents=intents)

prefix = '>'

@client.event
async def on_ready():
    print('Я гей')

@client.event
async def on_message(msg):
  
  # Vars

  user = msg.author
  channel = msg.channel
  messageIsPrivate = (str(channel.type) == 'private')
  guild = msg.guild
  content = msg.content
  
  # Embed forms
  
  helpEmb = discord.Embed(title='Помощь (префикс - ">")', description='Ниже приведены все команды этого бота', color=0xFF5733)
  
  # Not commands
  
  if msg.author.bot:
    return

  if messageIsPrivate and content != '':
    await fnc.addToLogFile('[PRIVATE] {0}: {1}'.format(user.name, content), 'private')
    return

  if content[0] != '>':
    await fnc.addToLogFile('[{0}] {1}: {2}'.format(channel.name, user.name, content), guild.id)
    
  # Commands
  
  helpEmb.add_field(name='ping', value='Проверить бота на жизнь.', inline=False)
  if prefix + 'ping' in content:
    await fnc.cmd_ping(msg)
    return
  
  # COMMAND HELP MUST BE LAST!!!
  helpEmb.add_field(name='help', value='Помощь', inline=False)
  if prefix + 'help' in content:
    await fnc.cmd_help(msg, helpEmb)
    return
  
  # Error no command
  await msg.reply('Такой команды не существует!')
  return
    
@client.event
async def on_member_join(member):
    pass

@client.event
async def on_member_remove(member):
    pass

client.run('OTI1MzMxNDg3MDUyNjg5NDM5' + '.YcrkGg.pVgr0ymuGtk7PJ' + 'HxegenmdhVCFA')