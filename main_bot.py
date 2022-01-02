import discord
from discord.ext import commands
import asyncio
import os

import functions as fnc

intents = discord.Intents.all()
client = discord.Client(intents=intents)

prefix = '>'

@client.event
async def on_ready():
  
  try:
    os.mkdir('data')
  except:
    pass
  
  print('Я гей')
  
@client.event
async def on_guild_join(guild):
  
  settingsStartTable = {}
  settingsStartTable['adminRole'] = -1
  settingsStartTable['newsRole'] = -1
  settingsStartTable['welcomeChannel'] = -1
  settingsStartTable['newsChannel'] = -1
  settingsStartTable['rolesOnStart'] = ['']
  
  try:
    os.mkdir('data/{0}'.format(guild.id))
    await fnc.savePickle(guild.id, settingsStartTable)
  except:
    pass
  

@client.event
async def on_message(msg):

  # Add embeds here
  helpEmb = discord.Embed(title='Помощь (префикс - ">")', description='Ниже приведены все команды этого бота', color=0xFF5733)
  newsEmb = discord.Embed(description='*{0}*'.format(msg.content), color=0xFF5733)
  newsEmbCMD = discord.Embed(description='*{0}*'.format(msg.content[len(prefix + 'news '):]), color=0xFF5733)
  memeEmb = discord.Embed(title='Мем', color=0xFF5733)
    
  # Add commands here
  await fnc.createCommand('help', 'Получить справку.', fnc.cmd_help, False, [msg, helpEmb])
  await fnc.createCommand('onls', 'Подписаться на рассылку.', fnc.cmd_onls, False, [msg])
  await fnc.createCommand('offls', 'Отписаться от рассылки.', fnc.cmd_offls, False, [msg])
  await fnc.createCommand('ping', 'Проверить жив ли бот.', fnc.cmd_ping, False, [msg])
  await fnc.createCommand('roll', 'Получить случайное число.', fnc.cmd_roll, False, [msg])
  await fnc.createCommand('tof', 'Получить случайный ответ на вопрос.', fnc.cmd_tof, False, [msg])
  await fnc.createCommand('meme', 'Получить смешной мем.', fnc.cmd_meme, False, [msg, memeEmb])
  await fnc.createCommand('clear', 'Очистить последние сообщения в чате.', fnc.cmd_clear, True, [msg])
  await fnc.createCommand('news', 'Отправить новость с рассылкой.', fnc.cmd_news, True, [msg, newsEmbCMD])
  await fnc.createCommand('setAdminRole', 'Установить роль администратора.', fnc.cmd_setAdminRole, True, [msg])
  await fnc.createCommand('setNewsChannel', 'Установить новостной канал.', fnc.cmd_setNewsChannel, True, [msg])
  await fnc.createCommand('setWelcomeChannel', 'Установить канал входов.', fnc.cmd_setWelcomeChannel, True, [msg])
  await fnc.createCommand('setNewsRole', 'Установить роль для рассылки новостей.', fnc.cmd_setNewsRole, True, [msg])
  await fnc.createCommand('setRolesOnStart', 'Установить стартовые роли.', fnc.cmd_setRolesOnStart, True, [msg])
  
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
  
  adminRoleID = await fnc.getAdminRole(guild.id)
  adminRole = guild.get_role(adminRoleID)
  
  newsChannelID = await fnc.getNewsChannel(guild.id)
  newsChannel = guild.get_channel(newsChannelID)
  
  newsRoleID = await fnc.getNewsRole(guild.id)
  newsRole = guild.get_role(newsRoleID)
  
  await fnc.addToLogFile('[{0}] {1}: {2}'.format(channel.name, user.name, content), guild.id)
  
  if msg.author.bot:
    return
  
  if content[0] != prefix:
    if channel.id == newsChannelID:
      if adminRole in user.roles or user.id == guild.owner.id:
        newsEmb.set_author(name=user.name, url=user.avatar_url, icon_url=user.avatar_url)
        await newsChannel.send(embed = newsEmb)
        await msg.delete()
    return
    
  # Commands
  
  for cmd in fnc.cmds:
    command = prefix + cmd
    if command.lower() == content[0:len(command)].lower():
      if fnc.cmds[cmd][2]:
        if adminRole in user.roles or user.id == guild.owner.id:
          try:
            await fnc.cmds[cmd][1](*fnc.cmds[cmd][3])
          except:
            await msg.reply('Аргументы команды введены неверно или кодер без мозга!')
          return
        else:
          await msg.reply('У вас нет доступа к этой команде!')
          return
      else:
        try:
          await fnc.cmds[cmd][1](*fnc.cmds[cmd][3])
        except:
          await msg.reply('Аргументы команды введены неверно или кодер без мозга!')
        return
    
  await msg.reply('Такой команды не существует!')
  return
    
@client.event
async def on_member_join(member):
  
  guild = member.guild
  welcomeChannelID = await fnc.getWelcomeChannel(guild.id)
  welcomeChannel = guild.get_channel(welcomeChannelID)
  
  await welcomeChannel.send('**{0}** зашел на сервер. Аккаунт создан: **{1}**. ({2})'.format(member.name, member.created_at.strftime("[%d/%m/%Y - %H:%M:%S]"), member.mention))

  if member.bot:
    return
  
  rolesOnStart = await fnc.getRolesOnStart(guild.id)
  for role in rolesOnStart:
    r = guild.get_role(int(role))
    await member.add_roles(r)
    
@client.event
async def on_member_remove(member):
  
  guild = member.guild
  welcomeChannelID = await fnc.getWelcomeChannel(guild.id)
  welcomeChannel = guild.get_channel(welcomeChannelID)
  
  await welcomeChannel.send('**{0}** вышел с сервера. Вход был: **{1}**.'.format(member.name, member.joined_at.strftime("[%d/%m/%Y - %H:%M:%S]"), member.mention))

client.run('')
