import discord
from discord.ext import commands
import asyncio

from datetime import datetime

cmds = {}

async def createCommand(cmd, desc, func, *args):
    cmds[cmd] = [desc, func, *args]
    return

async def addToLogFile(text, name):
  with open('chat_logs_' + str(name) + '.txt', 'a+') as writer:
    textToLog = '[' + datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + '] ' + text
    writer.seek(0)
    data = writer.read()
    if len(data) > 0:
      writer.write('\n')
    writer.write(textToLog)
    print(textToLog)
    
  
async def cmd_help(m, emb):
  await m.reply(embed=emb)

async def cmd_ping(m):
  await m.reply('Pong!')