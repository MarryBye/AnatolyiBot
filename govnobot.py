import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Я гей')

@client.event
async def on_message(msg):
  
  if msg.author.bot:
    return

  await msg.reply('Ты гей.')

@client.event
async def on_member_join(member):
    pass

@client.event
async def on_member_remove(member):
    pass

client.run('OTI1MzMxNDg3MDUyNjg5NDM5.YcrkGg.bl7OkpbKOzPaO4cIWU6vAsG6yfU')
