from socket import timeout
import discord
from discord.ext import commands
from discord import Color
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

        rsn = "- "
        if not (reason == None):
            rsn += ' '.join(reason)
        
        kickEmb = discord.Embed(title='Информация про кик', color=Color.from_rgb(54, 57, 63))
        kickEmb.add_field(name='Участник: ', value=member.name + '#' + member.discriminator, inline=False)
        kickEmb.add_field(name='Кикнул: ', value=ctx.author.name + '#' + member.discriminator, inline=False)
        kickEmb.add_field(name='Причина: ', value=rsn, inline=False)
        
        try:
            await guild.kick(member, reason=rsn)
            await ctx.channel.send(embed=kickEmb)
            await addToLogFile(ctx.guild.id, f'[KICK] Участник {ctx.author.name}#{ctx.author.discriminator} кикнул {member.name}#{member.discriminator}. Причина: {rsn}')
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
        
        rsn = "- "
        if not (reason == None):
            rsn += ' '.join(reason)

        banEmb = discord.Embed(title='Информация про бан', color=Color.from_rgb(54, 57, 63))
        banEmb.add_field(name='Участник: ', value=member.name + '#' + member.discriminator, inline=False)
        banEmb.add_field(name='Забанил: ', value=ctx.author.name + '#' + ctx.author.discriminator, inline=False)
        banEmb.add_field(name='Причина: ', value=rsn, inline=False)
        
        try:
            await guild.ban(member, reason=rsn, delete_message_days=0)
            await ctx.channel.send(embed=banEmb)
            await addToLogFile(ctx.guild.id, f'[BAN] Участник {ctx.author.name}#{ctx.author.discriminator} забанил {member.name}#{member.discriminator}. Причина: {rsn}')
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

        txt = "- "
        if not (text == None):
            txt += ' '.join(text)
        
        newsEmb = discord.Embed(description=txt, color=Color.from_rgb(54, 57, 63))
        newsEmb.set_author(name=ctx.author.name, url=ctx.author.avatar_url, icon_url=ctx.author.avatar_url)
        
        if not newsChannel is None:
            await newsChannel.send(embed = newsEmb)
            
        for member in guild.members:
            if newsRole is None:
                break
            if newsRole in member.roles:
                print(f'Отправляю сообщение: {member.name}')
                await member.send(embed = newsEmb)
        
        await addToLogFile(ctx.guild.id, f'[NEWS] Участник {ctx.author.name}#{ctx.author.discriminator} отправил новость с рассылкой. Текст: {txt}')
        await ctx.message.delete()
        
    @commands.command()
    async def clear(self, ctx, count):
        
        if not (await checkIsAdmin(ctx)):
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        clearEmb = discord.Embed(title='Информация про чистку', color=Color.from_rgb(54, 57, 63))
        clearEmb.add_field(name='Участник: ', value=ctx.author.name + '#' + ctx.author.discriminator, inline=False)
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
        
        await ctx.reply(f'newsRole: **{newsRole}**, \nadminRole: **{adminRole}**, \nrolesOnStart: **{rolesOnStart}**, \nnewsChannel: **{newsChannel}**, \nwelcomeChannel: **{welcomeChannel}**, \nlogsChannel: **{logsChannel}**, \nreportChannel: **{reportChannel}**', mention_author=False)
        
    @commands.command()
    async def reacs4Roles(self, ctx):

        if not (await checkIsAdmin(ctx)):
          await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
          return

        def check_msg_reac(reaction, user):
            return user == ctx.author

        def check_msg_msg(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        messageContent = ctx.message.content[len(ctx.invoked_with) + 2:]

        msg_reply_1 = await ctx.reply(f'**Текст будущего сообщения:**\n*{messageContent}*.\nЕсли хотите продолжить настройку сообщения, нажмите \N{THUMBS UP SIGN}, если нет, то \N{THUMBS DOWN SIGN}', mention_author=False)
        await msg_reply_1.add_reaction('\N{THUMBS UP SIGN}')
        await msg_reply_1.add_reaction('\N{THUMBS DOWN SIGN}')

        reaction, user = await ctx.bot.wait_for('reaction_add', check=check_msg_reac)
        if reaction == "\N{THUMBS DOWN SIGN}":
            return
        
        msg_reply_2 = await msg_reply_1.reply(f"**Вы решили продолжить настройку!**\nЧтобы установить роли и соответствующие реакции, вводите поочередно их по шаблону ниже:\n*\N{THUMBS DOWN SIGN} : @Роль1 | \N{THUMBS UP SIGN} : @Роль2 | ...*", mention_author=False)
        msgUserAnswer = await ctx.bot.wait_for('message', check=check_msg_msg)
        messageArgs = msgUserAnswer.content.replace(" ", "").split("|")
        msg_reply_3 = await msg_reply_2.reply(f"**Вы установили реакции и роли для них!**\nПроверьте, все ли верно и нажмите \N{THUMBS UP SIGN} и сообщение с реакциями будет создано, в ином случае нажмите \N{THUMBS DOWN SIGN}! Неправильно введенные реакции не будут добавлены в сообщение.\n**Текст сообщения:** \n*{messageContent}*\n**Реакции и роли:** \n{messageArgs[0:]}")
        await msg_reply_3.add_reaction('\N{THUMBS UP SIGN}')
        await msg_reply_3.add_reaction('\N{THUMBS DOWN SIGN}')
        reaction, user = await ctx.bot.wait_for('reaction_add', check=check_msg_reac)
        if reaction == "\N{THUMBS DOWN SIGN}":
            return
        await msg_reply_1.delete()
        await msg_reply_2.delete()
        await msg_reply_3.delete()
        await msgUserAnswer.delete()

        botMessage = await ctx.channel.send(f"{messageContent}")

        oldTable = await loadPickle(ctx.guild.id, 'reactionMessagesWithRoles')
        oldTable[botMessage.id] = []

        for reac in messageArgs:
            try:
                emojiString = reac.split(":")[0]
                roleID = reac.split(":")[1].replace("<", "").replace(">", "").replace("&", "").replace("@", "")
                channelID = str(ctx.channel.id)
                checkIsValid = ctx.guild.get_role(int(roleID))
                if checkIsValid is None:
                    continue
                await botMessage.add_reaction(reac.split(":")[0])
                oldTable[botMessage.id].append([emojiString, roleID, channelID])
            except:
                continue
        
        if not (oldTable[botMessage.id] == []):
            await savePickle(ctx.guild.id, 'reactionMessagesWithRoles', oldTable)
        else:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            await botMessage.delete()

def setup(bot):
    bot.add_cog(admin_cmd(bot))