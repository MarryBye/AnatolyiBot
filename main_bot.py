import discord
from discord.ext import commands
import asyncio

import functions as fnc

intents = discord.Intents.all()
client = discord.Client(intents=intents)

prefix = '>'
kostil = {}

@client.event
async def on_ready():
    
    print('Я гей')

@client.event
async def on_message(msg):
  
  # Vars
  
  if kostil == {}:

    # Add embeds here
    helpEmb = discord.Embed(title='Помощь (префикс - ">")', description='Ниже приведены все команды этого бота', color=0xFF5733)
    
    # Add commands here
    await fnc.createCommand('help', 'Получить справку.', fnc.cmd_help, [msg, helpEmb])
    await fnc.createCommand('ping', 'Проверить жив ли бот.', fnc.cmd_ping, [msg])
    
    # Do not touch!!!
    for cmd in fnc.cmds:
      helpEmb.add_field(name=cmd, value=fnc.cmds[cmd][0], inline=False)
    
    kostil[1] = 1 # жесточайший костыль в истории человечества т.к. я не хочу
                       # чтобы каждый раз команды делались, а переменная не работает 
                       # или у меня мозг оффнулся кто хочет исправляйте мне лень
  
  user = msg.author
  channel = msg.channel
  messageIsPrivate = (str(channel.type) == 'private')
  guild = msg.guild
  content = msg.content
  
  # Not commands
  
  if msg.author.bot:
    return

  if messageIsPrivate and content != '':
    await fnc.addToLogFile('[PRIVATE] {0}: {1}'.format(user.name, content), 'private')
    return

  if content[0] != '>':
    await fnc.addToLogFile('[{0}] {1}: {2}'.format(channel.name, user.name, content), guild.id)
    
  # Commands
  
  for cmd in fnc.cmds:
    command = prefix + cmd
    if command == content[0:len(command)]:
        await fnc.cmds[cmd][1](*fnc.cmds[cmd][2])
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

client.run('')
