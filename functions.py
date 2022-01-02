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
  
async def savePickle(guildID, arg):
  fl = open('data/{0}/settings_{0}.pkl'.format(guildID), 'wb')
  pickle.dump(arg, fl)

async def loadPickle(guildID):
  fl = open('data/{0}/settings_{0}.pkl'.format(guildID), 'rb')
  content = pickle.load(fl)
  fl.close()
  return content

async def cmd_setAdminRole(m):
  
  arg = await getNumbers(m.content)
  
  oldTable = await loadPickle(m.guild.id)
  oldTable['adminRole'] = arg

  await savePickle(m.guild.id, oldTable)
  await m.channel.send('Установил <@&{0}> как **роль администратора**!'.format(arg))
  await m.delete()
  
async def cmd_setNewsChannel(m):
  
  arg = await getNumbers(m.content)
  
  oldTable = await loadPickle(m.guild.id)
  oldTable['newsChannel'] = arg

  await savePickle(m.guild.id, oldTable)
  await m.channel.send('Установил <#{0}> как **новостной канал**!'.format(arg))
  await m.delete()
  
async def cmd_setWelcomeChannel(m):
  
  arg = await getNumbers(m.content)
  
  oldTable = await loadPickle(m.guild.id)
  oldTable['welcomeChannel'] = arg

  await savePickle(m.guild.id, oldTable)
  await m.channel.send('Установил <#{0}> как **канал приветствий**!'.format(arg))
  await m.delete()
  
async def cmd_setNewsRole(m):
  
  arg = await getNumbers(m.content)
  
  oldTable = await loadPickle(m.guild.id)
  oldTable['newsRole'] = arg

  await savePickle(m.guild.id, oldTable)
  await m.channel.send('Установил <@&{0}> как **роль для рассылки**!'.format(arg))
  await m.delete()
  
async def cmd_setRolesOnStart(m):
  
  argNotFormatted = m.content[len('_setrolesonstart '):]
  arg = ''
  
  for w in argNotFormatted:
    if w.isnumeric() or w == ' ':
      arg = arg + w
      
  arg = arg.split(' ')
  
  oldTable = await loadPickle(m.guild.id)
  oldTable['rolesOnStart'] = arg

  await savePickle(m.guild.id, oldTable)
  await m.channel.send('Установил {0} как **стартовые роли**!'.format(argNotFormatted))
  await m.delete()

async def getAdminRole(guildID):
  arg = await loadPickle(guildID)
  return int(arg['adminRole'])

async def getNewsChannel(guildID):
  arg = await loadPickle(guildID)
  return int(arg['newsChannel'])

async def getWelcomeChannel(guildID):
  arg = await loadPickle(guildID)
  return int(arg['welcomeChannel'])

async def getNewsRole(guildID):
  arg = await loadPickle(guildID)
  return int(arg['newsRole'])

async def getRolesOnStart(guildID):
  arg = await loadPickle(guildID)
  return arg['rolesOnStart']
  
async def cmd_help(m, emb):
  await m.reply(embed=emb)

async def cmd_ping(m):
  await m.reply('Pong!')
  
async def cmd_clear(m):
  arg = m.content[len('_clear '):]
  await m.channel.purge(limit=int(arg))
  await m.channel.send('**{0}** очистил **{1}** последних сообщений в канале!'.format(m.author.name, arg))
  
async def cmd_news(m, emb):
  guild = m.guild
  arg = m.content[len('_news '):]
  newsChannel = guild.get_channel(await getNewsChannel(guild.id))
  newsRole = guild.get_role(await getNewsRole(guild.id))
  emb.set_author(name=m.author.name, url=m.author.avatar_url, icon_url=m.author.avatar_url)
  await newsChannel.send(embed = emb)
  for member in guild.members:
    if newsRole in member.roles:
      await member.send(embed = emb)
      await m.delete()
      
async def cmd_onls(m):
  guild = m.guild
  newsRole = guild.get_role(await getNewsRole(guild.id))
  try:
    await m.author.add_roles(newsRole)
  except:
    pass
  await m.reply('Вы подписались на рассылку!')
      
async def cmd_offls(m):
  guild = m.guild
  newsRole = guild.get_role(await getNewsRole(guild.id))
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
