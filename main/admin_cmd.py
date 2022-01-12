import discord
from discord.ext import commands
import sys, os, re

sys.path.insert(1, os.path.abspath(".."))

from lib.funcs import *

class admin_cmd(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.category = 'Администраторские'
        self.adminOnly = True
        
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *reason):

        guild = ctx.guild
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
        kickEmb = discord.Embed(title='Информация про кик', color=0xFF5733)
        kickEmb.add_field(name='Участник: ', value=member.name + '#' + member.discriminator, inline=False)
        kickEmb.add_field(name='Кикнул: ', value=ctx.author.mention, inline=False)
        kickEmb.add_field(name='Причина: ', value=' '.join(reason), inline=False)
        
        try:
            await guild.kick(member, reason=' '.join(reason))
            await ctx.channel.send(embed=kickEmb)
            await addToLogFile(ctx.guild.id, f'[KICK] Участник {ctx.author.name}#{ctx.author.discriminator} кикнул {member.name}#{member.discriminator}. Причина: {" ".join(reason)}')
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *reason):
        
        guild = ctx.guild
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
        banEmb = discord.Embed(title='Информация про бан', color=0xFF5733)
        banEmb.add_field(name='Участник: ', value=member.name + '#' + member.discriminator, inline=False)
        banEmb.add_field(name='Забанил: ', value=ctx.author.mention, inline=False)
        banEmb.add_field(name='Причина: ', value=' '.join(reason), inline=False)
        
        try:
            await guild.ban(member, reason=' '.join(reason), delete_message_days=0)
            await ctx.channel.send(embed=banEmb)
            await addToLogFile(ctx.guild.id, f'[BAN] Участник {ctx.author.name}#{ctx.author.discriminator} забанил {member.name}#{member.discriminator}. Причина: {" ".join(reason)}')
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def news(self, ctx, *text):
        
        guild = ctx.guild
        
        if not (await checkIsAdmin(ctx)):
            return
        
        newsChannel = guild.get_channel(await getSettingsForGuild(guild.id, 'newsChannel'))
        newsRole = guild.get_role(await getSettingsForGuild(guild.id, 'newsRole'))
        
        newsEmb = discord.Embed(description=' '.join(text), color=0xFF5733)
        newsEmb.set_author(name=ctx.author.name, url=ctx.author.avatar_url, icon_url=ctx.author.avatar_url)
        
        if not newsChannel is None:
            await newsChannel.send(embed = newsEmb)
            
        for member in guild.members:
            if newsRole is None:
                break
            if newsRole in member.roles:
                print(f'Отправляю сообщение: {member.name}')
                await member.send(embed = newsEmb)
        
        await addToLogFile(ctx.guild.id, f'[NEWS] Участник {ctx.author.name}#{ctx.author.discriminator} отправил новость с рассылкой. Текст: {" ".join(text)}')
        await ctx.message.delete()
        
    @commands.command()
    async def clear(self, ctx, count):
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        clearEmb = discord.Embed(title='Информация про чистку', color=0xFF5733)
        clearEmb.add_field(name='Участник: ', value=ctx.author.mention, inline=False)
        clearEmb.add_field(name='Очистил: ', value=f'{count} собщений!', inline=False)

        try:
            await ctx.channel.purge(limit=int(count) + 1)
            await ctx.channel.send(embed=clearEmb)
            await addToLogFile(ctx.guild.id, f'[CLEAR] Участник {ctx.author.name}#{ctx.author.discriminator} очистил в канале {ctx.channel.name} {count} сообщений.')
        except:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return
        
    @commands.command()
    async def getSettings(self, ctx):
        
        if not (await checkIsAdmin(ctx)):
          await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
          return
        
        newsRole = await getSettingsForGuild(ctx.guild.id, 'newsRole')
        adminRole = await getSettingsForGuild(ctx.guild.id, 'adminRole')
        rolesOnStart = await getSettingsForGuild(ctx.guild.id, 'rolesOnStart')
        newsChannel = await getSettingsForGuild(ctx.guild.id, 'newsChannel')
        welcomeChannel = await getSettingsForGuild(ctx.guild.id, 'welcomeChannel')
        logsChannel = await getSettingsForGuild(ctx.guild.id, 'logsChannel')
        reportChannel = await getSettingsForGuild(ctx.guild.id, 'reportChannel')
        
        await ctx.channel.send(f'Роль новостей: {newsRole}, Роль администратора: {adminRole}, Роли на старте: {rolesOnStart}, Новостной канал: {newsChannel}, Приветственный канал: {welcomeChannel}, Канал для логов: {logsChannel}, Канал для репортов: {reportChannel}')
        await ctx.message.delete()
        
def setup(bot):
    bot.add_cog(admin_cmd(bot))
