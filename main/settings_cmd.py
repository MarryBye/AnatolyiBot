import discord
from discord.ext import commands
import sys, os, re

sys.path.insert(1, os.path.abspath(".."))

from lib.funcs import *

class settings_cmd(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.category = 'Настройки'
        self.adminOnly = True
        
    @commands.command()
    async def setReportChannel(self, ctx, channel: discord.TextChannel):
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        try:
            await setSettingsForGuild(ctx.guild.id, channel.id, 'reportChannel')
            
            await ctx.channel.send('Установил {0} как **канал для репортов**!'.format(channel.id))
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил канал для репортов.')
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
  
    @commands.command()
    async def setLogsChannel(self, ctx, channel: discord.TextChannel):
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        try:
            await setSettingsForGuild(ctx.guild.id, channel.id, 'logsChannel')
            
            await ctx.channel.send('Установил {0} как **канал логов**!'.format(channel.id))
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил канал для логов.')
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def setWelcomeChannel(self, ctx, channel: discord.TextChannel):
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
        try:
            await setSettingsForGuild(ctx.guild.id, channel.id, 'welcomeChannel')
            
            await ctx.channel.send('Установил {0} как **канал приветствий**!'.format(channel.id))
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил приветственный канал.')
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def setNewsChannel(self, ctx, channel: discord.TextChannel):
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        try:
            await setSettingsForGuild(ctx.guild.id, channel.id, 'newsChannel')
            
            await ctx.channel.send('Установил {0} как **новостной канал**!'.format(channel.id))
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил новостной канал.')
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def setRolesOnStart(self, ctx, *role: discord.Role):
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
        arg = []
        
        try:
            for r in role:
                arg.append(r.id)
                
            await setSettingsForGuild(ctx.guild.id, arg, 'rolesOnStart')
            
            await ctx.channel.send('Установил {0} как **стартовые роли**!'.format(arg))
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил стартовые роли.')
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def setNewsRole(self, ctx, role: discord.Role):
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        try:
            await setSettingsForGuild(ctx.guild.id, role.id, 'newsRole')
            
            await ctx.channel.send('Установил {0} как **роль для рассылки**!'.format(role.id))
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил новостные роли.')
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def setAdminRole(self, ctx, role: discord.Role):
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        try:
            await setSettingsForGuild(ctx.guild.id, role.id, 'adminRole')
            
            await ctx.channel.send('Установил {0} как **роль администратора**!'.format(role.id))
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил админские роли.')
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def setNoneValueFor(self, ctx, value):
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
        try:
            await setSettingsForGuild(ctx.guild.id, -1, value)
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} сбросил значение {value}.')
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
def setup(bot):
    bot.add_cog(settings_cmd(bot))