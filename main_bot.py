import discord
from discord.ext import commands
import asyncio
import os

import functions as fnc

intents = discord.Intents.all()
client = discord.Client(intents=intents)

prefix = '>'

@client.event
async def on_ready():

  print('Бот готов к использованию.')

  print('Проверка данных...')
  
  try:
    os.mkdir('data')
    print('Восстановил папку data!')
  except:
    print('Папка data не нуждается в восстановлении!')
    pass
  
  for guild in client.guilds:
    print('Загрузка | Сервер «{0}»...'.format(guild.name))
    await fnc.repairFilesForGuild(guild)

  
  
@client.event
async def on_guild_join(guild):
  
  print('Загрузка | Сервер «{0}»...'.format(guild.name))
  await fnc.repairFilesForGuild(guild)

@client.event
async def on_message(msg):

  # Add embeds here
  helpEmb = discord.Embed(title='Помощь (префикс - ">")', description='Ниже приведены все команды этого бота', color=0xFF5733)
  memeEmb = discord.Embed(title='Мем', color=0xFF5733)
  newsEmb = discord.Embed(description='*{0}*'.format(msg.content), color=0xFF5733)
  newsEmbCMD = discord.Embed(description='*{0}*'.format(msg.content[len(prefix + 'news '):]), color=0xFF5733)
  banEmb = discord.Embed(title='Информация про бан', color=0xFF5733)
  kickEmb = discord.Embed(title='Информация про кик', color=0xFF5733)
  clearEmb = discord.Embed(title='Информация про чистку', color=0xFF5733)
  reportEmb = discord.Embed(title='Жалоба', color=0xFF5733)
  infoEmb = discord.Embed(title='Информация', color=0xFF5733)
    
  # Add commands here
  
  # User commands
  
  await fnc.createCommand('help', 'Получить справку.', fnc.cmd_help, False, 'Пользовательские', [msg, helpEmb])
  await fnc.createCommand('report', 'Отправить жалобу на человека.', fnc.cmd_report, False, 'Пользовательские', [msg, reportEmb])
  await fnc.createCommand('onls', 'Подписаться на рассылку.', fnc.cmd_onls, False, 'Пользовательские', [msg])
  await fnc.createCommand('offls', 'Отписаться от рассылки.', fnc.cmd_offls, False, 'Пользовательские', [msg])
  await fnc.createCommand('ping', 'Проверить жив ли бот.', fnc.cmd_ping, False, 'Пользовательские', [msg])
  await fnc.createCommand('info', 'Информация про вас.', fnc.cmd_info, False, 'Пользовательские', [msg, infoEmb])
  
  # Fun commands
  await fnc.createCommand('roll', 'Получить случайное число.', fnc.cmd_roll, False, 'Развлечение', [msg])
  await fnc.createCommand('tof', 'Получить случайный ответ на вопрос.', fnc.cmd_tof, False, 'Развлечение', [msg])
  await fnc.createCommand('meme', 'Получить смешной мем.', fnc.cmd_meme, False, 'Развлечение', [msg, memeEmb])
  
  # Admin commands
  await fnc.createCommand('clear', 'Очистить последние сообщения в чате.', fnc.cmd_clear, True, 'Администраторские', [msg, clearEmb])
  await fnc.createCommand('news', 'Отправить новость с рассылкой.', fnc.cmd_news, True, 'Администраторские', [msg, newsEmbCMD])
  await fnc.createCommand('ban', 'Забанить участника.', fnc.cmd_ban, True, 'Администраторские', [msg, banEmb])
  await fnc.createCommand('kick', 'Кикнуть участника.', fnc.cmd_kick, True, 'Администраторские', [msg, kickEmb])
  
  # Settings commands
  await fnc.createCommand('setAdminRole', 'Установить роль администратора.', fnc.cmd_setAdminRole, True, 'Настройки', [msg])
  await fnc.createCommand('setNewsRole', 'Установить роль для рассылки новостей.', fnc.cmd_setNewsRole, True, 'Настройки', [msg])
  await fnc.createCommand('setRolesOnStart', 'Установить стартовые роли.', fnc.cmd_setRolesOnStart, True, 'Настройки', [msg])
  await fnc.createCommand('setNewsChannel', 'Установить новостной канал.', fnc.cmd_setNewsChannel, True, 'Настройки', [msg])
  await fnc.createCommand('setWelcomeChannel', 'Установить канал входов.', fnc.cmd_setWelcomeChannel, True, 'Настройки', [msg])
  await fnc.createCommand('setLogsChannel', 'Установить канал для логов.', fnc.cmd_setLogsChannel, True, 'Настройки', [msg])
  await fnc.createCommand('setReportChannel', 'Установить канал для репортов.', fnc.cmd_setReportChannel, True, 'Настройки', [msg])
  
  # Do not touch!!!
  cmd_sorted = {}

  for cmd in fnc.cmds:
    try:
      cmd_sorted[fnc.cmds[cmd][3]].insert(0, '`` ' + prefix + cmd + ' ``')
    except:
      cmd_sorted[fnc.cmds[cmd][3]] = []
      cmd_sorted[fnc.cmds[cmd][3]].insert(0, '`` ' + prefix + cmd + ' ``')
      
  for cat in cmd_sorted:
    helpEmb.add_field(name=cat, value=' '.join(cmd_sorted[cat]), inline=False)
  
  user = msg.author
  channel = msg.channel
  messageIsPrivate = str(channel.type) == 'private'
  guild = msg.guild
  content = msg.content
  
  userInfo = await fnc.loadPickle(guild.id, 'membersStats')
  
  if str(user.id) in userInfo:
    userInfo[str(user.id)]['msgs'] += 1
    userInfo[str(user.id)]['exp'] += round((0.1 + len(content) / 10), 3)
    if userInfo[str(user.id)]['exp'] >= userInfo[str(user.id)]['expToNextLvl']:
      userInfo[str(user.id)]['lvl'] += 1
      userInfo[str(user.id)]['expToNextLvl'] = round(userInfo[str(user.id)]['expToNextLvl'] * 2.5, 3)
      userInfo[str(user.id)]['exp'] = 0
      await msg.channel.send('{0}, поздравляю с достижением {1} уровня!'.format(msg.author.mention, userInfo[str(user.id)]['lvl']))
    await fnc.savePickle(guild.id, 'membersStats', userInfo)
  else:
    userInfo[str(user.id)] = {}
    userInfo[str(user.id)]['lvl'] = 0
    userInfo[str(user.id)]['exp'] = 0
    userInfo[str(user.id)]['expToNextLvl'] = 100
    userInfo[str(user.id)]['msgs'] = 0
    await fnc.savePickle(guild.id, 'membersStats', userInfo)
  
  # Not commands
  
  if messageIsPrivate:
    await fnc.addToLogFile('[PRIVATE] {0}: {1}'.format(user.name, content), 'PRIVATE_LOGS')
    return
  
  adminRoleID = await fnc.getAdminRole(guild.id)
  adminRole = guild.get_role(adminRoleID)
  
  newsChannelID = await fnc.getNewsChannel(guild.id)
  newsChannel = guild.get_channel(newsChannelID)
  
  await fnc.addToLogFile('[{0}] {1}: {2}'.format(channel.name, user.name, content), guild.id)
  
  if msg.author.bot:
    return
  
  if content != '' and content[0] != prefix:
    if channel.id == newsChannelID:
      if adminRole in user.roles or user.id == guild.owner.id or user.guild_permissions.administrator:
        newsEmb.set_author(name=user.name, url=user.avatar_url, icon_url=user.avatar_url)
        try:
          await newsChannel.send(embed = newsEmb)
        except:
          pass
        await msg.delete()
    return
    
  # Commands
  
  for cmd in fnc.cmds:
    command = prefix + cmd
    if command.lower() == content.split(' ')[0]:
      if fnc.cmds[cmd][2]:
        if adminRole in user.roles or user.id == guild.owner.id or user.guild_permissions.administrator:
          try:
            await fnc.cmds[cmd][1](*fnc.cmds[cmd][4])
          except:
            await msg.reply('Аргументы команды введены неверно или кодер без мозга!')
          return
        else:
          await msg.reply('У вас нет доступа к этой команде!')
          return
      else:
        try:
          await fnc.cmds[cmd][1](*fnc.cmds[cmd][4])
        except:
          await msg.reply('Аргументы команды введены неверно или кодер без мозга!')
        return
    
  await msg.reply('Такой команды не существует!')
  return
    
@client.event
async def on_member_join(member):
  
  guild = member.guild
  welcomeChannelID = await fnc.getWelcomeChannel(guild.id)
  welcomeChannel = guild.get_channel(welcomeChannelID)
  
  await welcomeChannel.send('**{0}** зашел на сервер. Аккаунт создан: **{1}**. ({2})'.format(member.name, member.created_at.strftime("[%d/%m/%Y - %H:%M:%S]"), member.mention))

  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  logsEmb = discord.Embed(title='Участник вошел', color=0x2ecc71)
  logsEmb.add_field(name='Участник: ', value=member.mention, inline=False)
  logsEmb.add_field(name='Аккаунт создан: : ', value=member.created_at.strftime("[%d/%m/%Y - %H:%M:%S]"), inline=False)
  logsEmb.add_field(name='Бот: ', value=member.bot, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass
  
  if member.bot:
    return
  
  rolesOnStart = await fnc.getRolesOnStart(guild.id)
  for role in rolesOnStart:
    r = guild.get_role(int(role))
    await member.add_roles(r)
    
@client.event
async def on_member_remove(member):
  
  guild = member.guild
  welcomeChannelID = await fnc.getWelcomeChannel(guild.id)
  welcomeChannel = guild.get_channel(welcomeChannelID)
  
  await welcomeChannel.send('**{0}** вышел с сервера. Вход был: **{1}**.'.format(member.name, member.joined_at.strftime("[%d/%m/%Y - %H:%M:%S]"), member.mention))

  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  logsEmb = discord.Embed(title='Участник вышел', color=0xe74c3c)
  logsEmb.add_field(name='Участник: ', value=member.name + '#' + member.discriminator, inline=False)
  logsEmb.add_field(name='Аккаунт создан: : ', value=member.created_at.strftime("[%d/%m/%Y - %H:%M:%S]"), inline=False)
  logsEmb.add_field(name='Последний вход: : ', value=member.joined_at.strftime("[%d/%m/%Y - %H:%M:%S]"), inline=False)
  logsEmb.add_field(name='Бот: ', value=member.bot, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass
  
@client.event
async def on_member_update(bef, aft):
  
  if bef.roles == aft.roles and bef.display_name == aft.display_name:
    return
  
  guild = bef.guild
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  argBef = ''
  
  for role in bef.roles:
    if role.name == '@everyone':
      argBef = argBef + str(role)
      continue
    argBef = argBef + ' <@&' + str(role.id) + '>'
    
  argAft = ''
  
  for role in aft.roles:
    if role.name == '@everyone':
      argAft = argAft + str(role)
      continue
    argAft = argAft + ' <@&' + str(role.id) + '>'
    
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
    userEditor = str(log.user)
  
  logsEmb = discord.Embed(title='Изменения участника', color=0xf1c40f)
  logsEmb.add_field(name='Участник: ', value=bef.mention, inline=False)
  logsEmb.add_field(name='Изменил: ', value=userEditor, inline=False)
  logsEmb.add_field(name='Имя до: ', value=bef.display_name, inline=False)
  logsEmb.add_field(name='Роли до: ', value=argBef, inline=False)
  logsEmb.add_field(name='Имя после: ', value=aft.display_name, inline=False)
  logsEmb.add_field(name='Роли после: ', value=argAft, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_member_ban(guild, user):
  
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
    userBanner = str(log.user)
    reason = str(log.reason)
  
  logsEmb = discord.Embed(title='Бан участника', color=0xe74c3c)
  logsEmb.add_field(name='Участник: ', value=user.name + '#' + user.discriminator, inline=False)
  logsEmb.add_field(name='Забанил: ', value=userBanner, inline=False)
  logsEmb.add_field(name='Причина: ', value=reason, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_member_unban(guild, user):
  
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
    userUnbanner = str(log.user)
  
  logsEmb = discord.Embed(title='Разбан участника', color=0x2ecc71)
  logsEmb.add_field(name='Участник: ', value=user.name + '#' + user.discriminator, inline=False)
  logsEmb.add_field(name='Разбанил: ', value=userUnbanner, inline=False)

  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_message_delete(msg):
  
  guild = msg.guild
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
    userDeleter = str(log.user)
  
  logsEmb = discord.Embed(title='Удалено сообщение', color=0xe74c3c)
  logsEmb.add_field(name='Автор: ', value=msg.author.mention, inline=False)
  logsEmb.add_field(name='Удалил: ', value=userDeleter, inline=False)
  logsEmb.add_field(name='Канал: ', value=msg.channel.mention, inline=False)
  logsEmb.add_field(name='Содержание: ', value=msg.content, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass
  

@client.event
async def on_message_edit(bef, aft):
  
  guild = bef.guild
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  logsEmb = discord.Embed(title='Отредактировано сообщение', color=0xf1c40f)
  logsEmb.add_field(name='Автор: ', value=bef.author.mention, inline=False)
  logsEmb.add_field(name='Канал: ', value=bef.channel.mention, inline=False)
  logsEmb.add_field(name='Содержание до: ', value=bef.content, inline=False)
  logsEmb.add_field(name='Содержание после: ', value=aft.content, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_reaction_add(react, member):
  
  guild = react.message.guild
  msg = react.message
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  logsEmb = discord.Embed(title='Добавлена реакция', color=0x2ecc71)
  logsEmb.add_field(name='Автор: ', value=msg.author.mention, inline=False)
  logsEmb.add_field(name='Канал: ', value=msg.channel.mention, inline=False)
  logsEmb.add_field(name='Сообщение: ', value=msg.jump_url, inline=False)
  logsEmb.add_field(name='Добавил: ', value=member.mention, inline=False)
  logsEmb.add_field(name='Реакция: ', value=react.emoji, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_reaction_remove(react, member):
  
  guild = react.message.guild
  msg = react.message
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  logsEmb = discord.Embed(title='Удалена реакция', color=0xe74c3c)
  logsEmb.add_field(name='Автор: ', value=msg.author.mention, inline=False)
  logsEmb.add_field(name='Канал: ', value=msg.channel.mention, inline=False)
  logsEmb.add_field(name='Сообщение: ', value=msg.jump_url, inline=False)
  logsEmb.add_field(name='Удалил: ', value=member.mention, inline=False)
  logsEmb.add_field(name='Реакция: ', value=react.emoji, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_reaction_clear(msg, react):
  
  guild = msg.guild
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  arg = ''
  
  for r in react:
    arg = arg + ' ' + str(r)
  
  logsEmb = discord.Embed(title='Очищены реакции', color=0xe74c3c)
  logsEmb.add_field(name='Автор: ', value=msg.author.mention, inline=False)
  logsEmb.add_field(name='Канал: ', value=msg.channel.mention, inline=False)
  logsEmb.add_field(name='Сообщение: ', value=msg.jump_url, inline=False)
  logsEmb.add_field(name='Реакции: ', value=arg, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_guild_channel_delete(channel):
  
  guild = channel.guild
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
    userDeleter = str(log.user)
  
  logsEmb = discord.Embed(title='Удален канал', color=0xe74c3c)
  logsEmb.add_field(name='Канал: ', value=channel.name, inline=False)
  logsEmb.add_field(name='Категория: ', value=channel.category, inline=False)
  logsEmb.add_field(name='Удалил: ', value=userDeleter, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_guild_channel_create(channel):
  
  guild = channel.guild
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
    userCreator = str(log.user)
  
  logsEmb = discord.Embed(title='Создан канал', color=0x2ecc71)
  logsEmb.add_field(name='Канал: ', value=channel.mention, inline=False)
  logsEmb.add_field(name='Категория: ', value=channel.category, inline=False)
  logsEmb.add_field(name='Создал: ', value=userCreator, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_guild_channel_update(bef, aft):
  
  guild = bef.guild
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update):
    userEditor = str(log.user)
  
  logsEmb = discord.Embed(title='Отредактирован канал', color=0xf1c40f)
  logsEmb.add_field(name='Канал: ', value=bef.mention, inline=False)
  logsEmb.add_field(name='Название до: ', value=bef.name, inline=False)
  logsEmb.add_field(name='Категория до: ', value=bef.category, inline=False)
  logsEmb.add_field(name='Название после: ', value=aft.name, inline=False)
  logsEmb.add_field(name='Категория после: ', value=aft.category, inline=False)
  logsEmb.add_field(name='Отредактировал: ', value=userEditor, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_guild_role_create(role):
  
  guild = role.guild
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
    userCreator = str(log.user)
    
  logsEmb = discord.Embed(title='Создана роль', color=0x2ecc71)
  logsEmb.add_field(name='Роль: ', value=role.mention, inline=False)
  logsEmb.add_field(name='Создал: ', value=userCreator, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_guild_role_delete(role):
  
  guild = role.guild
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
    userDeleter = str(log.user)
    
  logsEmb = discord.Embed(title='Удалена роль', color=0xe74c3c)
  logsEmb.add_field(name='Роль: ', value=role.name, inline=False)
  logsEmb.add_field(name='Удалил: ', value=userDeleter, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@client.event
async def on_guild_role_update(bef, aft):
  
  if bef.permissions == aft.permissions and bef.name == aft.name:
    return
  
  guild = bef.guild
  logsChannel = guild.get_channel(await fnc.getLogsChannel(guild.id))
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update):
    userEditor = str(log.user)
    
  logsEmb = discord.Embed(title='Отредактирована роль', color=0xf1c40f)
  logsEmb.add_field(name='Роль: ', value=bef.mention, inline=False)
  logsEmb.add_field(name='Название до: ', value=bef.name, inline=False)
  logsEmb.add_field(name='Права до: ', value=bef.permissions.value, inline=False)
  logsEmb.add_field(name='Имя после: ', value=aft.name, inline=False)
  logsEmb.add_field(name='Права после: ', value=aft.permissions.value, inline=False)
  logsEmb.add_field(name='Отредактировал: ', value=userEditor, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

client.run(fnc.readToken())