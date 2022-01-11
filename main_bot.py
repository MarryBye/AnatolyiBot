import discord
from discord.ext import commands
import os

from lib.funcs import *
import main.user_cmd, main.fun_cmd, main.music_cmd, main.admin_cmd, main.settings_cmd

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all(), help_command=None)

cogs = [main.user_cmd, main.fun_cmd, main.music_cmd, main.admin_cmd, main.settings_cmd]

for i in range(len(cogs)):
  cogs[i].setup(bot)
  
@bot.command()
async def help(ctx):
  
  cmds = {}
  
  helpEmb = discord.Embed(title='Помощь (префикс - ">")', description='Ниже приведены все команды этого бота', color=0xFF5733)
  
  for cog in bot.cogs:
    for cmd in bot.cogs[cog].get_commands():
      print(cmd.name, bot.cogs[cog].category)
      if not bot.cogs[cog].category in cmds:
        cmds[bot.cogs[cog].category] = []
      cmds[bot.cogs[cog].category].append(f'``>{cmd.name}``')
  
  for category in cmds:
    helpEmb.add_field(name=category, value=' '.join(cmds[category]), inline=False)
    
  await ctx.reply(embed=helpEmb)

@bot.event
async def on_ready():

  print('Бот готов к использованию.')

  print('Проверка данных...')
  
  try:
    os.mkdir('data')
    print('Восстановил папку data!')
  except:
    print('Папка data не нуждается в восстановлении!')
    pass
  
  for guild in bot.guilds:
    print('Загрузка | Сервер «{0}»...'.format(guild.name))
    await repairFilesForGuild(guild)
    
@bot.event
async def on_guild_join(guild):

  print('Зашел в сервер «{0}»'.format(guild.name))
  
  print('Загрузка | Сервер «{0}»...'.format(guild.name))
  await repairFilesForGuild(guild)
  
@bot.event
async def on_command_error(ctx, error):
  await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')

@bot.event
async def on_message(msg):
  
  if str(msg.channel.type) == 'private':
    await addToLogFile('PRIVATE_LOGS', f'["PRIVATE"] {msg.author.name}#{msg.author.discriminator}: {msg.content}')
    pass
  
  if msg.content == '' or msg.content is None:
    pass
  
  if not msg.author.bot:
    newsChannelID = await getSettingsForGuild(msg.guild.id, 'newsChannel')
    if msg.channel.id == newsChannelID:
      newsEmb = discord.Embed(description='*{0}*'.format(msg.content), color=0xFF5733)
      adminRole = msg.guild.get_role(await getSettingsForGuild(msg.guild.id, 'adminRole'))
      if adminRole is None:
        return
      if adminRole in msg.author.roles or msg.author.id == msg.guild.owner.id or msg.author.guild_permissions.administrator:
        newsEmb.set_author(name=msg.author.name, url=msg.author.avatar_url, icon_url=msg.author.avatar_url)
        try:
          await msg.channel.send(embed = newsEmb)
        except:
          pass
        await msg.delete()
    
    if await memberHasStats(msg.guild.id, msg.author.id):
      nextLvlExp = await getMemberStat(msg.guild.id, msg.author.id, 'expToNextLvl')
      await addMemberStat(msg.guild.id, msg.author.id, 'msg', 1)
      await addMemberStat(msg.guild.id, msg.author.id, 'exp', round(0.1 + (len(msg.content) / 10)))
      if await getMemberStat(msg.guild.id, msg.author.id, 'exp') >= nextLvlExp:
        await addMemberStat(msg.guild.id, msg.author.id, 'lvl', 1)
        await setMemberStat(msg.guild.id, msg.author.id, 'exp', 0)
        await setMemberStat(msg.guild.id, msg.author.id, 'expToNextLvl', round(nextLvlExp * 2.5))
        await msg.add_reaction('🆙')
    else:
      await memberSetStartStats(msg.guild.id, msg.author.id)
      
  await addToLogFile(msg.guild.id, f'[{msg.channel.name}] {msg.author.name}#{msg.author.discriminator}: {msg.content}')
  await bot.process_commands(msg)
  
@bot.event
async def on_member_join(member):
  
  guild = member.guild
  
  welcomeChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'welcomeChannel')))
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if welcomeChannel is None:
    return
  
  if logsChannel is None:
    return
  
  await welcomeChannel.send('**{0}** зашел на сервер. Аккаунт создан: **{1}**. ({2})'.format(member.name, member.created_at.strftime("[%d/%m/%Y - %H:%M:%S]"), member.mention))
  
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
  
  rolesOnStart = await getSettingsForGuild(guild.id, 'rolesOnStart')
  for role in rolesOnStart:
    r = guild.get_role(role)
    await member.add_roles(r)
    
@bot.event
async def on_member_remove(member):
  
  guild = member.guild
  welcomeChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'welcomeChannel')))
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if welcomeChannel is None:
    return
  
  if logsChannel is None:
    return
  
  await welcomeChannel.send('**{0}** вышел с сервера. Вход был: **{1}**.'.format(member.name, member.joined_at.strftime("[%d/%m/%Y - %H:%M:%S]"), member.mention))
  
  logsEmb = discord.Embed(title='Участник вышел', color=0xe74c3c)
  logsEmb.add_field(name='Участник: ', value=member.name + '#' + member.discriminator, inline=False)
  logsEmb.add_field(name='Аккаунт создан: : ', value=member.created_at.strftime("[%d/%m/%Y - %H:%M:%S]"), inline=False)
  logsEmb.add_field(name='Последний вход: : ', value=member.joined_at.strftime("[%d/%m/%Y - %H:%M:%S]"), inline=False)
  logsEmb.add_field(name='Бот: ', value=member.bot, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass
  
@bot.event
async def on_member_update(bef, aft):
  
  if bef.roles == aft.roles and bef.display_name == aft.display_name:
    return
  
  guild = bef.guild
  
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
  if bef.roles != aft.roles:
    async for log in guild.audit_logs(action=discord.AuditLogAction.member_role_update):
      userEditor = log.user
    
  if bef.display_name != aft.display_name:
    async for log in guild.audit_logs(action=discord.AuditLogAction.member_update):
      userEditor = log.user
  
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

@bot.event
async def on_member_ban(guild, user):
  
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
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

@bot.event
async def on_member_unban(guild, user):
  
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
    userUnbanner = str(log.user)
  
  logsEmb = discord.Embed(title='Разбан участника', color=0x2ecc71)
  logsEmb.add_field(name='Участник: ', value=user.name + '#' + user.discriminator, inline=False)
  logsEmb.add_field(name='Разбанил: ', value=userUnbanner, inline=False)

  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@bot.event
async def on_message_delete(msg):
  
  guild = msg.guild
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
  #async for log in guild.audit_logs(limit=None):
    #print(log)
  
  logsEmb = discord.Embed(title='Удалено сообщение', color=0xe74c3c)
  logsEmb.add_field(name='Автор: ', value=msg.author.mention, inline=False)
  #logsEmb.add_field(name='Удалил: ', value=userDeleter, inline=False)
  logsEmb.add_field(name='Канал: ', value=msg.channel.mention, inline=False)
  logsEmb.add_field(name='Содержание: ', value=msg.content, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass
  

@bot.event
async def on_message_edit(bef, aft):
  
  guild = bef.guild
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
  logsEmb = discord.Embed(title='Отредактировано сообщение', color=0xf1c40f)
  logsEmb.add_field(name='Автор: ', value=bef.author.mention, inline=False)
  logsEmb.add_field(name='Канал: ', value=bef.channel.mention, inline=False)
  logsEmb.add_field(name='Содержание до: ', value=bef.content, inline=False)
  logsEmb.add_field(name='Содержание после: ', value=aft.content, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@bot.event
async def on_reaction_add(react, member):
  
  guild = react.message.guild
  msg = react.message
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
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

@bot.event
async def on_reaction_remove(react, member):
  
  guild = react.message.guild
  msg = react.message
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
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

@bot.event
async def on_reaction_clear(msg, react):
  
  guild = msg.guild
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
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

@bot.event
async def on_guild_channel_delete(channel):
  
  guild = channel.guild
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
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

@bot.event
async def on_guild_channel_create(channel):
  
  guild = channel.guild
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
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

@bot.event
async def on_guild_channel_update(bef, aft):
  
  if bef.name == aft.name and bef.category == aft.category:
    return
  
  guild = bef.guild
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
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

@bot.event
async def on_guild_role_create(role):
  
  guild = role.guild
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
    userCreator = str(log.user)
    
  logsEmb = discord.Embed(title='Создана роль', color=0x2ecc71)
  logsEmb.add_field(name='Роль: ', value=role.mention, inline=False)
  logsEmb.add_field(name='Создал: ', value=userCreator, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@bot.event
async def on_guild_role_delete(role):
  
  guild = role.guild
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
  async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
    userDeleter = str(log.user)
    
  logsEmb = discord.Embed(title='Удалена роль', color=0xe74c3c)
  logsEmb.add_field(name='Роль: ', value=role.name, inline=False)
  logsEmb.add_field(name='Удалил: ', value=userDeleter, inline=False)
  
  try:
    await logsChannel.send(embed=logsEmb)
  except:
    pass

@bot.event
async def on_guild_role_update(bef, aft):
  
  if bef.permissions == aft.permissions and bef.name == aft.name:
    return
  
  guild = bef.guild
  logsChannel = guild.get_channel((await getSettingsForGuild(guild.id, 'logsChannel')))
  
  if logsChannel is None:
    return
  
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

bot.run(readToken())