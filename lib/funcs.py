import discord

import os
import pickle
import youtube_dl
import re

from datetime import *

def readToken():
  with open('token', 'r') as fl:
    return fl.read()

async def addToLogFile(guildID, text):
  try:
    os.mkdir('data/' + str(guildID))
  except:
    pass
  with open('data/' + str(guildID) + '/chat_logs.txt', mode='a+', encoding='utf-8') as writer:
    textToLog = '[{0}] {1}'.format(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"), text)
    writer.seek(0)
    data = writer.read()
    if len(data) > 0:
      writer.write('\n')
    writer.write(textToLog)
    print(textToLog)
    
async def getStringArgs(txt, needNumbers = False):

    argsNotFormatted = txt.split(' ')[1:]
    
    if needNumbers:
      argsFormatted = []
      for arg in argsNotFormatted:
          id = int(re.sub('[^0-9]', '', arg))
          if not id is None and not id == '':
            argsFormatted.append(id)
      return argsFormatted
    else:
      return argsNotFormatted
    
async def getNumbers(txt):
  return int(re.sub('[^0-9]', '', txt))
    
async def getTimeBySeconds(secs):
  return timedelta(seconds=secs)
    
async def savePickle(guildID, fname, arg):
  fl = open('data/{0}/{1}.pkl'.format(guildID, fname), 'wb')
  pickle.dump(arg, fl)

async def loadPickle(guildID, fname):
  fl = open('data/{0}/{1}.pkl'.format(guildID, fname), 'rb')
  content = pickle.load(fl)
  fl.close()
  return content

async def repairFilesForGuild(guild):
  
  settingsStartTable = {}
  settingsStartTable['adminRole'] = -1
  settingsStartTable['newsRole'] = -1
  settingsStartTable['welcomeChannel'] = -1
  settingsStartTable['newsChannel'] = -1
  settingsStartTable['logsChannel'] = -1
  settingsStartTable['reportChannel'] = -1
  settingsStartTable['rolesOnStart'] = [-1]
  
  membersStartTable = {}

  try:
    os.mkdir('data/{0}'.format(guild.id))
    await savePickle(guild.id, 'guildSettings', settingsStartTable)
    await savePickle(guild.id, 'membersStats', membersStartTable)
    print('Восстановил файлы для сервера «{0}»'.format(guild.name))
  except:
    print('Файлы не нуждаются в восстановлении!')
    pass

async def loadAndPlayMusic(v, u):
  v.stop()
  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  YDL_OPTIONS = {'format': 'bestaudio'}
  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    if u.startswith('https://www.youtube.com/watch'):
      info = ydl.extract_info(u, download=False)
      u2 = info['formats'][0]['url']
      source = await discord.FFmpegOpusAudio.from_probe(u2, executable='ffmpeg', **FFMPEG_OPTIONS)
      v.play(source)
    else:
      info = ydl.extract_info('ytsearch:{0}'.format(u), download=False)['entries'][0]
      u2 = info['formats'][0]['url']
      source = await discord.FFmpegOpusAudio.from_probe(u2, executable='ffmpeg', **FFMPEG_OPTIONS)
      v.play(source)
      
    if not info is None:
      return {
        'title': info['title'], 
        'video_url': info['webpage_url'], 
        'author': info['uploader'], 
        'author_url': info['uploader_url'], 
        'date': info['upload_date'], 
        'time': info['duration']}
      
async def checkIsAdmin(ctx):
  
  if ctx.guild.owner.id == ctx.author.id:
    return True
  
  if ctx.author.guild_permissions.administrator:
    return True
  
  adminRole = ctx.guild.get_role(await getSettingsForGuild(ctx.guild.id, 'adminRole'))
        
  if not adminRole is None and adminRole in ctx.author.roles:
    return True
  
  return False
      
async def setSettingsForGuild(guildID, arg, setting):
  
  oldTable = await loadPickle(guildID, 'guildSettings')
  oldTable[setting] = arg

  await savePickle(guildID, 'guildSettings', oldTable)
  
async def getSettingsForGuild(guildID, setting):
  
  arg = await loadPickle(guildID, 'guildSettings')
  
  return arg[setting]

async def getMembersStatsTable(guildID):
  
  oldTable = await loadPickle(guildID, 'membersStats')
  
  return oldTable

async def memberHasStats(guildID, userID):
  
  oldTable = await loadPickle(guildID, 'membersStats')
  
  return str(userID) in oldTable

async def memberSetStartStats(guildID, userID):
  
  oldTable = await loadPickle(guildID, 'membersStats')
  oldTable[str(userID)] = {}
  oldTable[str(userID)]['msg'] = 0
  oldTable[str(userID)]['exp'] = 0
  oldTable[str(userID)]['lvl'] = 0
  oldTable[str(userID)]['expToNextLvl'] = 50
  
  await savePickle(guildID, 'membersStats', oldTable)

async def setMemberStat(guildID, userID, stat, arg):
  
  oldTable = await loadPickle(guildID, 'membersStats')
  oldTable[str(userID)][stat] = arg

  await savePickle(guildID, 'membersStats', oldTable)
  
async def addMemberStat(guildID, userID, stat, arg):
  
  oldTable = await loadPickle(guildID, 'membersStats')
  oldTable[str(userID)][stat] += arg

  await savePickle(guildID, 'membersStats', oldTable)

async def getMemberStat(guildID, userID, stat):
  
  arg = await loadPickle(guildID, 'membersStats')
  
  return arg[str(userID)][stat]
