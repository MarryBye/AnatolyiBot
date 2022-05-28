import discord
from discord.ext import commands
from discord import Color
import sys, os, aiohttp, random

sys.path.insert(1, os.path.abspath(".."))

from lib.funcs import *

class fun_cmd(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.category = 'Развлекательные'
        self.adminOnly = False
        
    @commands.command()
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                memeEmb = discord.Embed(title='Мем', color=Color.from_rgb(54, 57, 63))
                memeEmb.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.reply(embed=memeEmb, mention_author=False)
        
    @commands.command()
    async def tof(self, ctx):
        await ctx.reply('Я думаю... {0}'.format(random.choice(['Да', 'Нет', 'возможно частично', 'Затрудняюсь в ответе.'])), mention_author=False)
        
    @commands.command()
    async def roll(self, ctx, max = 100, min = 0):
        if min > max:
            await ctx.reply('Ваше случайное число: {0}'.format(random.randint(max, min)), mention_author=False)
        else:
            await ctx.reply('Ваше случайное число: {0}'.format(random.randint(min, max)), mention_author=False)
        
def setup(bot):
    bot.add_cog(fun_cmd(bot))