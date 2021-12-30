import discord
from discord.ext import commands
import asyncio
import os
import random
import aiohttp
import pickle

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
  fl = open(fname, 'r')
  return int(fl.read())
  
async def savePickle(fname, arg):
  fl = open(fname, 'wb')
  pickle.dump(arg, fl)

async def loadPickle(fname):
  fl = open(fname, 'rb')
  content = pickle.load(fl)
  fl.close()
  return content

async def getAdminRole(m):
  guild = m.guild
  path = 'data/' + str(guild.id)
  content = await load(path + '/settings_adminRole.txt')
  return content

async def getNewsChannel(m):
  guild = m.guild
  path = 'data/' + str(guild.id)
  content = await load(path + '/settings_newsChannel.txt')
  return content

async def getWelcomeChannel(m):
  guild = m.guild
  path = 'data/' + str(guild.id)
  content = await load(path + '/settings_welcomeChannel.txt')
  return content

async def getNewsRole(m):
  guild = m.guild
  path = 'data/' + str(guild.id)
  content = await load(path + '/settings_newsRole.txt')
  return content

async def getRolesOnStart(m):
  guild = m.guild
  path = 'data/' + str(guild.id)
  content = await loadPickle(path + '/settings_rolesOnStart.pkl')
  return content
  
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
  await m.channel.send('Установил {0} как **роль администратора**!'.format(adminRole.name))
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
  await m.channel.send('Установил {0} как **новостной канал**!'.format(newsChannel.name))
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
  await m.channel.send('Установил {0} как **приветственный канал**!'.format(welcomeChannel.name))
  await m.delete()
  
async def cmd_setNewsRole(m):
  guild = m.guild
  arg = await getNumbers(m.content)
  newsRole = guild.get_role(int(arg))
  path = 'data/' + str(guild.id)
  try:
    os.mkdir(path)
  except:
    pass
  await save(path + '/settings_newsRole.txt', arg)
  await m.channel.send('Установил {0} как **роль для рассылки**!'.format(newsRole.name))
  await m.delete()
  
async def cmd_setRolesOnStart(m):
  guild = m.guild
  arg = m.content[len('_setrolesonstart '):].split(' ')
  path = 'data/' + str(guild.id)
  try:
    os.mkdir(path)
  except:
    pass
  await savePickle(path + '/settings_rolesOnStart.pkl', arg)
  await m.channel.send('Установил указанные роли как **стартовые**!')
  await m.delete()
  
async def cmd_news(m, emb):
  guild = m.guild
  arg = m.content[len('_news '):]
  newsChannel = guild.get_channel(await getNewsChannel(m))
  newsRole = guild.get_role(await getNewsRole(m))
  for member in guild.members:
    if newsRole in member.roles:
      emb.set_author(name=m.author.name, url=m.author.avatar_url, icon_url=m.author.avatar_url)
      await member.send(embed = emb)
      await newsChannel.send(embed = emb)
      await m.delete()
      
async def cmd_onls(m):
  guild = m.guild
  newsRole = guild.get_role(await getNewsRole(m))
  try:
    await m.author.add_roles(newsRole)
  except:
    pass
  await m.reply('Вы подписались на рассылку!')
      
async def cmd_offls(m):
  guild = m.guild
  newsRole = guild.get_role(await getNewsRole(m))
  try:
    await m.author.remove_roles(newsRole)
  except:
    pass
  await m.reply('Вы отписали от рассылки!')
  
async def cmd_roll(m):
  await m.reply('Ваше случайное число: {0}'.format(random.randint(0, 100)))
  
async def cmd_tof(m):
  await m.reply('Я думаю... {0}'.format(random.choice(['Да', 'Нет', 'возможно частично', 'Затрудняюсь в ответе.'])))
  
async def cmd_meme(m, emb):
  async with aiohttp.ClientSession() as cs:
    async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
        res = await r.json()
        emb.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
        await m.channel.send(embed=emb)