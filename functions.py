import discord
from discord.ext import commands
import asyncio
import os
import random
import aiohttp
import pickle

from datetime import datetime

cmds = {}

def readToken():
  with open('token', 'r') as fl:
    return fl.read()

async def createCommand(cmd, desc, func, forAdm, t, *args):
    cmds[cmd] = [desc, func, forAdm, t, *args]
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
  
async def savePickle(guildID, fname, arg):
  fl = open('data/{0}/{1}.pkl'.format(guildID, fname), 'wb')
  pickle.dump(arg, fl)

async def loadPickle(guildID, fname):
  fl = open('data/{0}/{1}.pkl'.format(guildID, fname), 'rb')
  content = pickle.load(fl)
  fl.close()
  return content

async def cmd_setAdminRole(m):
  
  arg = await getNumbers(m.content)
  
  oldTable = await loadPickle(m.guild.id, 'guildSettings')
  oldTable['adminRole'] = arg

  await savePickle(m.guild.id, 'guildSettings', oldTable)
  await m.channel.send('Установил <@&{0}> как **роль администратора**!'.format(arg))
  await m.delete()
  
async def cmd_setNewsChannel(m):
  
  arg = await getNumbers(m.content)
  
  oldTable = await loadPickle(m.guild.id, 'guildSettings')
  oldTable['newsChannel'] = arg

  await savePickle(m.guild.id, 'guildSettings', oldTable)
  await m.channel.send('Установил <#{0}> как **новостной канал**!'.format(arg))
  await m.delete()
  
async def cmd_setWelcomeChannel(m):
  
  arg = await getNumbers(m.content)
  
  oldTable = await loadPickle(m.guild.id, 'guildSettings')
  oldTable['welcomeChannel'] = arg

  await savePickle(m.guild.id, 'guildSettings', oldTable)
  await m.channel.send('Установил <#{0}> как **канал приветствий**!'.format(arg))
  await m.delete()
  
async def cmd_setLogsChannel(m):
  
  arg = await getNumbers(m.content)
  
  oldTable = await loadPickle(m.guild.id, 'guildSettings')
  oldTable['logsChannel'] = arg

  await savePickle(m.guild.id, 'guildSettings', oldTable)
  await m.channel.send('Установил <#{0}> как **канал логов**!'.format(arg))
  await m.delete()
  
async def cmd_setNewsRole(m):
  
  arg = await getNumbers(m.content)
  
  oldTable = await loadPickle(m.guild.id, 'guildSettings')
  oldTable['newsRole'] = arg

  await savePickle(m.guild.id, 'guildSettings', oldTable)
  await m.channel.send('Установил <@&{0}> как **роль для рассылки**!'.format(arg))
  await m.delete()
  
async def cmd_setReportChannel(m):
  
  arg = await getNumbers(m.content)
  
  oldTable = await loadPickle(m.guild.id, 'guildSettings')
  oldTable['reportChannel'] = arg

  await savePickle(m.guild.id, 'guildSettings', oldTable)
  await m.channel.send('Установил <#{0}> как **канал для репортов**!'.format(arg))
  await m.delete()
  
async def cmd_setRolesOnStart(m):
  
  argNotFormatted = m.content[len('_setrolesonstart '):]
  arg = ''
  
  for w in argNotFormatted:
    if w.isnumeric() or w == ' ':
      arg = arg + w
      
  arg = arg.split(' ')
  
  oldTable = await loadPickle(m.guild.id, 'guildSettings')
  oldTable['rolesOnStart'] = arg

  await savePickle(m.guild.id, 'guildSettings', oldTable)
  await m.channel.send('Установил {0} как **стартовые роли**!'.format(argNotFormatted))
  await m.delete()

async def getAdminRole(guildID):
  arg = await loadPickle(guildID, 'guildSettings')
  return int(arg['adminRole'])

async def getNewsChannel(guildID):
  arg = await loadPickle(guildID, 'guildSettings')
  return int(arg['newsChannel'])

async def getWelcomeChannel(guildID):
  arg = await loadPickle(guildID, 'guildSettings')
  return int(arg['welcomeChannel'])

async def getLogsChannel(guildID):
  arg = await loadPickle(guildID, 'guildSettings')
  return int(arg['logsChannel'])

async def getNewsRole(guildID):
  arg = await loadPickle(guildID, 'guildSettings')
  return int(arg['newsRole'])

async def getRolesOnStart(guildID):
  arg = await loadPickle(guildID, 'guildSettings')
  return arg['rolesOnStart']

async def getReportChannel(guildID):
  arg = await loadPickle(guildID, 'guildSettings')
  return int(arg['reportChannel'])

async def getMemberLevel(guildID, userID):
  arg = await loadPickle(guildID, 'membersStats')
  return arg[str(userID)]['lvl']

async def getMemberExperience(guildID, userID):
  arg = await loadPickle(guildID, 'membersStats')
  return arg[str(userID)]['exp']

async def getMemberExperienceToNextLvl(guildID, userID):
  arg = await loadPickle(guildID, 'membersStats')
  return arg[str(userID)]['expToNextLvl']

async def getMemberMessages(guildID, userID):
  arg = await loadPickle(guildID, 'membersStats')
  return arg[str(userID)]['msgs']
  
async def cmd_help(m, emb):
  await m.reply(embed=emb)

async def cmd_ping(m):
  await m.reply('Pong!')
  
async def cmd_info(m, emb):
  
  msgs = await getMemberMessages(m.guild.id, m.author.id)
  lvl = await getMemberLevel(m.guild.id, m.author.id)
  exp = await getMemberExperience(m.guild.id, m.author.id)
  exptonextlvl = await getMemberExperienceToNextLvl(m.guild.id, m.author.id)
  
  percentsHas = 100 * exp / exptonextlvl
  percentGraph = ''
  
  for i in range(100)[::5]:
    if percentsHas > i:
      percentGraph = percentGraph + '/'
    else:
      percentGraph = percentGraph + ' .'
  
  emb.add_field(name='Участник: ', value=m.author.mention, inline=False)
  emb.add_field(name='Всего сообщений: ', value=str(msgs), inline=False)
  emb.add_field(name='Уровень: ', value=str(lvl), inline=False)
  emb.add_field(name='Опыт: ', value='{0} / {1} EXP\n[{2}]'.format(exp, exptonextlvl, percentGraph), inline=False)
  
  await m.reply(embed=emb) 
  
async def cmd_clear(m, emb):
  args = m.content.split(' ')
  messageCount = args[1]
  
  emb.add_field(name='Участник: ', value=m.author.mention, inline=False)
  emb.add_field(name='Очистил: ', value=messageCount + ' собщений!', inline=False)
  
  await m.channel.purge(limit=int(messageCount))
  await m.channel.send(embed=emb)
  
async def cmd_news(m, emb):
  guild = m.guild
  newsChannel = guild.get_channel(await getNewsChannel(guild.id))
  newsRole = guild.get_role(await getNewsRole(guild.id))
  emb.set_author(name=m.author.name, url=m.author.avatar_url, icon_url=m.author.avatar_url)
  await newsChannel.send(embed = emb)
  for member in guild.members:
    if newsRole in member.roles:
      try:
        await member.send(embed = emb)
      except:
        pass
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
        
async def cmd_report(m, emb):
  
  guild = m.guild
  reportChannel = guild.get_channel(await getReportChannel(guild.id))
  
  args = m.content.split(' ')
  userID = await getNumbers(args[1])
  user = guild.get_member(int(userID))
  reason = '** **'
  
  for word in args[2:]:
    reason = reason + word + ' '
  
  emb.add_field(name='Жалоба на: ', value=user.mention, inline=False)
  emb.add_field(name='Пожаловался: ', value=m.author.mention, inline=False)
  emb.add_field(name='Причина: ', value=reason, inline=False)
  
  await m.channel.send('{0}, ваша жалоба отправлена и будет рассмотрена администраторами!'.format(m.author.mention))
  await reportChannel.send(embed=emb)
  await m.delete()
        
async def cmd_ban(m, emb):
  
  guild = m.guild
  args = m.content.split(' ')
  userID = await getNumbers(args[1])
  user = guild.get_member(int(userID))
  reason = '** **'
  
  for word in args[2:]:
    reason = reason + word + ' '
    
  emb.add_field(name='Участник: ', value=user.name + '#' + user.discriminator, inline=False)
  emb.add_field(name='Забанил: ', value=m.author.mention, inline=False)
  emb.add_field(name='Причина: ', value=reason, inline=False)
  
  await m.channel.send(embed=emb)
  await guild.ban(user, reason=reason, delete_message_days=0)
  await m.delete()
  
async def cmd_kick(m, emb):
  
  guild = m.guild
  args = m.content.split(' ')
  userID = await getNumbers(args[1])
  user = guild.get_member(int(userID))
  reason = '** **'
  
  for word in args[2:]:
    reason = reason + word + ' '
    
  emb.add_field(name='Участник: ', value=user.name + '#' + user.discriminator, inline=False)
  emb.add_field(name='Кикнул: ', value=m.author.mention, inline=False)
  emb.add_field(name='Причина: ', value=reason, inline=False)
  
  await guild.kick(user, reason=reason)
  await m.channel.send(embed=emb)
  await m.delete()
  
