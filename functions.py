import discord
from discord.ext import commands
import asyncio
import os

from datetime import datetime

cmds = {}

async def createCommand(cmd, desc, func, forAdm, *args):
    cmds[cmd] = [desc, func, forAdm, *args]
    return

async def addToLogFile(text, name):
  try:
    os.mkdir('data/' + name)
  except:
    pass
  with open('data/' + str(name) + '/chat_logs.txt', mode='a+', encoding='utf-8') as writer:
    textToLog = '[' + datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + '] ' + text
    writer.seek(0)
    data = writer.read()
    if len(data) > 0:
      writer.write('\n')
    writer.write(textToLog)
    print(textToLog)
    
async def getFuncName(f):
  return f.__name__[len('cmd_'):]

async def getNumbers(txt):
  id = ''
  for w in txt:
    if w.isnumeric():
      id = id + w
  return id

async def save(fname, arg):
  fl = open(fname, 'w')
  fl.write(str(arg))
  fl.close()

async def load(fname):
  fl = open('data/' + fname, 'r')
  return int(fl.read('data/' + fname))
  
async def cmd_help(m, emb):
  await m.reply(embed=emb)

async def cmd_ping(m):
  await m.reply('Pong!')
  
async def cmd_clear(m):
  arg = m.content[len('_clear '):]
  await m.channel.purge(limit=int(arg))
  await m.channel.send('**{0}** очистил **{1}** последних сообщений в канале!'.format(m.author.name, arg))

async def cmd_setAdminRole(m):
  guild = m.guild
  arg = await getNumbers(m.content)
  adminRole = guild.get_role(int(arg))
  path = 'data/' + str(guild.id)
  try:
    os.mkdir(path)
  except:
    pass
  await save(path + '/settings_adminRole.txt', arg)
  await m.channel.send('Установил ' + adminRole.name + ' как **роль администратора**!')
  await m.delete()
  
async def cmd_setNewsChannel(m):
  guild = m.guild
  arg = await getNumbers(m.content)
  newsChannel = guild.get_channel(int(arg))
  path = 'data/' + str(guild.id)
  try:
    os.mkdir(path)
  except:
    pass
  await save(path + '/settings_newsChannel.txt', arg)
  await m.channel.send('Установил ' + newsChannel.name + ' как **новостной канал**!')
  await m.delete()
  
async def cmd_setWelcomeChannel(m):
  guild = m.guild
  arg = await getNumbers(m.content)
  welcomeChannel = guild.get_channel(int(arg))
  path = 'data/' + str(guild.id)
  try:
    os.mkdir(path)
  except:
    pass
  await save(path + '/settings_welcomeChannel.txt', arg)
  await m.channel.send('Установил ' + welcomeChannel.name + ' как **приветственный канал**!')
  await m.delete()
  
async def getAdminRole(m):
  guild = m.guild
  path = 'data/' + str(guild.id)
  fl = open(path + '/settings_adminRole.txt', 'r')
  content = int(fl.read())
  fl.close()
  return content

async def getNewsChannel(m):
  guild = m.guild
  path = 'data/' + str(guild.id)
  fl = open(path + '/settings_newsChannel.txt', 'r')
  content = int(fl.read())
  fl.close()
  return content

async def getWelcomeChannel(m):
  guild = m.guild
  path = 'data/' + str(guild.id)
  fl = open(path + '/settings_welcomeChannel.txt', 'r')
  content = int(fl.read())
  fl.close()
  return content