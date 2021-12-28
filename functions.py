import discord
from discord.ext import commands
import asyncio

async def addToLogFile(text, guild):
  with open('chat_logs_' + str(guild.id) + '.txt', 'a+') as writer:
    textToLog = '[' + datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + '] ' + text
    writer.seek(0)
    data = writer.read()
    if len(data) > 0:
      writer.write('\n')
    writer.write(textToLog)
    print(textToLog)