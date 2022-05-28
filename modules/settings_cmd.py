import discord
from discord.ext import commands
from discord import Color
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
            
            await ctx.reply(f'Установил {channel.id} как **канал для репортов**!', mention_author=False)
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил канал для репортов.')
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
            
            await ctx.reply(f'Установил {channel.id} как **канал логов**!', mention_author=False)
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил канал для логов.')
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
            
            await ctx.reply(f'Установил {channel.id} как **канал приветствий**!', mention_author=False)
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил приветственный канал.')
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
            
            await ctx.reply(f'Установил {channel.id} как **новостной канал**!', mention_author=False)
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил новостной канал.')
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
            
            await ctx.reply(f'Установил {arg} как **стартовые роли**!', mention_author=False)
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил стартовые роли.')
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
            
            await ctx.reply(f'Установил {role.id} как **роль для рассылки**!', mention_author=False)
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил новостные роли.')
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
            
            await ctx.reply(f'Установил {role.id} как **роль администратора**!', mention_author=False)
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} изменил админские роли.')
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def setNoneValueFor(self, ctx, value):
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        validValues = ['newsRole', 'adminRole', 'rolesOnStart', 'newsChannel', 'welcomeChannel', 'logsChannel', 'reportChannel']
        
        if not (value in validValues):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        try:
            await setSettingsForGuild(ctx.guild.id, -1, value)
            await ctx.reply(f'Обнулил значение {value}! Теперь эта настройка неактивна.', mention_author=False)
            await addToLogFile(ctx.guild.id, f'[SETTINGS] Участник {ctx.author.name}#{ctx.author.discriminator} сбросил значение {value}.')
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
def setup(bot):
    bot.add_cog(settings_cmd(bot))