import discord
from discord.ext import commands
import sys, os

sys.path.insert(1, os.path.abspath(".."))

from lib.funcs import *

class user_cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = 'Пользовательские'
        self.adminOnly = False
        
    @commands.command()
    async def ping(self, ctx):
        await ctx.reply('Pong!')
        
    @commands.command()
    async def info(self, ctx):
        
        msgs =              await getMemberStat(ctx.guild.id, ctx.author.id, 'msg')
        lvl =               await getMemberStat(ctx.guild.id, ctx.author.id, 'lvl')
        exp =               await getMemberStat(ctx.guild.id, ctx.author.id, 'exp')
        exptonextlvl =      await getMemberStat(ctx.guild.id, ctx.author.id, 'expToNextLvl')
        
        percentsHas = 100 * exp / exptonextlvl
        percentGraph = ''
        
        for i in range(100)[::5]:
            if percentsHas > i:
                percentGraph = percentGraph + '+'
            else:
                percentGraph = percentGraph + '-'
        
        infoEmb = discord.Embed(title='Информация', color=0xFF5733)
        infoEmb.add_field(name='Участник: ', value=ctx.author.mention, inline=False)
        infoEmb.add_field(name='Всего сообщений: ', value=str(msgs), inline=False)
        infoEmb.add_field(name='Уровень: ', value=str(lvl), inline=False)
        infoEmb.add_field(name='Опыт: ', value='{0} / {1} EXP\n[{2}]'.format(exp, exptonextlvl, percentGraph), inline=False)
        
        await ctx.channel.send(embed=infoEmb)
        await ctx.message.delete()
        
    @commands.command()
    async def onls(self, ctx):
        
        guild = ctx.guild
        newsRole = guild.get_role(await getSettingsForGuild(guild.id, 'newsRole'))
        
        try:
            await ctx.author.add_roles(newsRole)
        except:
            pass
        
        await ctx.channel.send(f'{ctx.author.mention} подписался на рассылку новостей в ЛС!')
        await ctx.message.delete()
        
    @commands.command()
    async def offls(self, ctx):
        
        guild = ctx.guild
        newsRole = guild.get_role(await getSettingsForGuild(guild.id, 'newsRole'))
        
        try:
            await ctx.author.remove_roles(newsRole)
        except:
            pass
        
        await ctx.channel.send(f'{ctx.author.mention} отписался от рассылки новостей в ЛС!')
        await ctx.message.delete()
        
    @commands.command()
    async def report(self, ctx, member: discord.Member, *reason):
        
        guild = ctx.guild
        reportChannel = guild.get_channel(await getSettingsForGuild(guild.id, 'reportChannel'))
        
        if reportChannel is None:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
        reportEmb = discord.Embed(title='Жалоба', color=0xFF5733)
        reportEmb.add_field(name='Жалоба на: ', value=member.mention, inline=False)
        reportEmb.add_field(name='Пожаловался: ', value=ctx.author.mention, inline=False)
        reportEmb.add_field(name='Причина: ', value=' '.join(reason), inline=False)
        
        try:
            await reportChannel.send(embed=reportEmb)
            await ctx.channel.send('{0}, ваша жалоба отправлена и будет рассмотрена администраторами!'.format(ctx.author.mention))
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def top(self, ctx):
        
        guild = ctx.guild
        
        topEmb = discord.Embed(title='Рейтинг самых активных', color=0xFF5733)
        oldTable = await getMembersStatsTable(guild.id)
        
        sortedTopTable = sorted(oldTable.items(), key = lambda kv:(kv[1]['msg'], kv[0]), reverse=True)

        for k,v in sortedTopTable[0:10]:
          try:
            memb = guild.get_member(int(k))
            print(memb.name)
            msg = v['msg']
            lvl = v['lvl']
            exp = v['exp']
            expToNextLvl = v['expToNextLvl']
            
            topEmb.add_field(name=f'{memb.name}#{memb.discriminator}', value=f'Сообщения: {msg}\nУровень: {lvl}\nОпыт: {exp} / {expToNextLvl}', inline=False)
          except:
            continue
            
        await ctx.channel.send(embed=topEmb)
        await ctx.message.delete()
        
def setup(bot):
    bot.add_cog(user_cmd(bot))
