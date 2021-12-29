import discord
from discord.ext import commands
import asyncio
import os

import functions as fnc

intents = discord.Intents.all()
client = discord.Client(intents=intents)

prefix = '>'
kostil = {}

@client.event
async def on_ready():
  try:
    os.mkdir('data')
  except:
    pass
  print('Я гей')
  
@client.event
async def on_guild_join(guild):
  path = 'data/' + str(guild.id)
  try:
    os.mkdir(path)
    await fnc.save(path + '/settings_adminRole.txt', -1)
    await fnc.save(path + '/settings_newsChannel.txt', -1)
    await fnc.save(path + '/settings_welcomeChannel.txt', -1)
  except:
    pass

@client.event
async def on_message(msg):

  # Add embeds here
  helpEmb = discord.Embed(title='Помощь (префикс - ">")', description='Ниже приведены все команды этого бота', color=0xFF5733)
    
  # Add commands here
  await fnc.createCommand('help', 'Получить справку.', fnc.cmd_help, False, [msg, helpEmb])
  await fnc.createCommand('ping', 'Проверить жив ли бот.', fnc.cmd_ping, False, [msg])
  await fnc.createCommand('clear', 'Очистить последние сообщения в чате.', fnc.cmd_clear, True, [msg])
  await fnc.createCommand('setAdminRole', 'Установить роль администратора.', fnc.cmd_setAdminRole, True, [msg])
  await fnc.createCommand('setNewsChannel', 'Установить новостной канал.', fnc.cmd_setNewsChannel, True, [msg])
  await fnc.createCommand('setWelcomeChannel', 'Установить канал входов.', fnc.cmd_setWelcomeChannel, True, [msg])
    
    # Do not touch!!!
  for cmd in fnc.cmds:
    helpEmb.add_field(name=cmd, value=fnc.cmds[cmd][0], inline=False)
  
  user = msg.author
  channel = msg.channel
  messageIsPrivate = str(channel.type) == 'private'
  guild = msg.guild
  content = msg.content
  
  # Not commands
  
  if messageIsPrivate:
    await fnc.addToLogFile('[PRIVATE] {0}: {1}'.format(user.name, content), 'PRIVATE_LOGS')
    return
  
  adminRoleID = await fnc.getAdminRole(msg)
  adminRole = guild.get_role(adminRoleID)
  
  newsChannelID = await fnc.getNewsChannel(msg)
  newsChannel = guild.get_role(newsChannelID)
  
  welcomeChannelID = await fnc.getWelcomeChannel(msg)
  welcomeChannel = guild.get_role(welcomeChannelID)
  
  await fnc.addToLogFile('[{0}] {1}: {2}'.format(channel.name, user.name, content), guild.id)
  
  if msg.author.bot:
    return
  
  if content[0] != '>':
    if channel.id == newsChannelID:
      await msg.reply('News')
      return
    
  # Commands
  
  for cmd in fnc.cmds:
    command = prefix + cmd
    if command == content[0:len(command)]:
      if fnc.cmds[cmd][2]:
        if adminRole in user.roles or user.id == guild.owner.id:
          await fnc.cmds[cmd][1](*fnc.cmds[cmd][3])
          return
        else:
          await msg.reply('У вас нет доступа к этой команде!')
          return
      else:
        await fnc.cmds[cmd][1](*fnc.cmds[cmd][3])
        return
    
  await msg.reply('Такой команды не существует!')
  return
    
@client.event
async def on_member_join(member):
    pass

@client.event
async def on_member_remove(member):
    pass

client.run('OTI1MzMxNDg3MDUyNjg5NDM5.YcrkGg.5CUAzUv3ERJCJTwRdDIWyk_pBXk')