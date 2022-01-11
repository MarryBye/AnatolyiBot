import discord
from discord.ext import commands
import sys, os

sys.path.insert(1, os.path.abspath(".."))

from lib.funcs import *

class music_cmd(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.category = 'Проигрыватель'
        self.adminOnly = False
        
    @commands.command()
    async def j(self, ctx):
        
        if ctx.author.voice is None:
            return
        
        channel = ctx.author.voice.channel
        
        if ctx.voice_client is None:
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)
            
        await ctx.message.delete()
            
    @commands.command()
    async def l(self, ctx):
        
        if ctx.author.voice is None:
            return
        
        channel = ctx.author.voice.channel
        
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        
        await ctx.message.delete()
            
    @commands.command()
    async def p(self, ctx, *urlArg):
        
        url = ''
        
        if urlArg[0].startswith('https://www.youtube.com/watch'):
            url = urlArg[0]
        else:
            for w in urlArg[0:]:
                url += f'{w} '
            
        if ctx.author.voice is None:
            return
        
        channel = ctx.author.voice.channel
        
        if ctx.voice_client is None:
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)
        
        try:
            videoTable = await loadAndPlayMusic(ctx.voice_client, url)
        
            musicEmb = discord.Embed(title='Информация про видео', color=0xFF5733)
            musicEmb.add_field(name='Участник: ', value=ctx.author.mention, inline=False)
            musicEmb.add_field(name='Канал: ', value='[{0}]({1})'.format(videoTable['author'], videoTable['author_url']), inline=False)
            musicEmb.add_field(name='Видео: ', value='[{0}]({1})'.format(videoTable['title'], videoTable['video_url']), inline=False)
            musicEmb.add_field(name='Длительность: ', value=await getTimeBySeconds(int(videoTable['time'])), inline=False)
                
            await ctx.channel.send(embed=musicEmb)
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def s(self, ctx):
        
        if ctx.author.voice is None:
            return
        
        if ctx.voice_client is None:
            return
        else:
            ctx.voice_client.pause()
            
        await ctx.message.delete()
        
    @commands.command()
    async def r(self, ctx):
        
        if ctx.author.voice is None:
            return
        
        if ctx.voice_client is None:
            return
        else:
            ctx.voice_client.resume()
            
        await ctx.message.delete()
        
def setup(bot):
    bot.add_cog(music_cmd(bot))