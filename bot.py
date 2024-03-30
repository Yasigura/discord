import contextlib
import asyncio
import discord
from discord.ext import commands

config = {
    'token':'~',
    'id': '~',
    'prefix': '!'
}
notification_message_id = None

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.reactions = True
intents.messages = True

bot = commands.Bot(command_prefix=config['prefix'],
                   intents=intents,
                   help_command=None)



@bot.command(name='say')
async def say(ctx, *, say: str):
  await ctx.message.delete()
  permissions = True
  if permissions == True:
    required_roles = ["СОЗДАТЕЛЬ", "Helper"]
    if any(role.name in required_roles for role in ctx.author.roles):
      await ctx.send(say)
    else:
      with contextlib.suppress(discord.HTTPException):
        await ctx.author.send(
            'У вас нет необходимой роли для использования этой команды.')
  if permissions == False:
    await ctx.send(say)

@bot.event
async def on_message(say):
  if say.author == bot.user:
    return
  await bot.process_commands(say)



@bot.command(name='mute')
@commands.has_permissions(manage_roles=True)
@commands.has_any_role('СОЗДАТЕЛЬ', 'Helper')
async def mute(ctx, member: discord.Member, *, reason=None):
  reason = reason or "не указана"
  mute_role = discord.utils.get(ctx.guild.roles, name="мут")
  if not mute_role:
        mute_role = await ctx.guild.create_role(name="мут")
    
  if mute_role not in member.roles:
    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f'{member.mention} был замьючен по причине: {reason}')
    await member.send('Вас замьютил ' + ctx.author.mention + ' по причине: ' +  reason + ', на сервере : ' + ctx.guild.name)
  else:
    await ctx.send(f'{member.mention} уже замьючен.')

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  await bot.process_commands(message)



@bot.command(name='unmute')
@commands.has_permissions(manage_roles=True)
@commands.has_any_role('СОЗДАТЕЛЬ', 'Helper')
async def unmute(ctx, member: discord.Member):
  mute_role = discord.utils.get(ctx.guild.roles, name="мут")
  if mute_role in member.roles:
    await member.remove_roles(mute_role)
    await ctx.send(f'{member.mention} был размьючен.')
    await member.send('Вас размьютил ' + ctx.author.mention + ', на сервере : ' + ctx.guild.name)
  else:
    await ctx.send(f'{member.mention} не в муте.')

@bot.event
async def on_message_unmute(unmute):
  if unmute.author == bot.user:
    return
  await bot.process_commands(unmute)


@bot.command(name='help')
@commands.has_any_role('СОЗДАТЕЛЬ', 'Helper')
async def custom_help_mod(ctx):
  embed = discord.Embed(title=f'Привет {ctx.author.mention}!',
                        color=discord.Color.green())
  embed.add_field(name='Комнады для модераторов:', value=
                   '!help - помощь в использовании команд бота\n' \
                   '!unmute - размьютить пользователя\n' \
                   '!mute @user - замьютить пользователя\n' \
                   '!say - сказать от имени бота (иногда разрешено только для '
                   'административным ролей)\n' \
                   '!notif - уведомления по играм\n' \
                   '!clear число - очистить число сообщений', inline=False)
  await ctx.channel.send(embed=embed)



@bot.event
async def on_member_join(member):
  try:
    channel = bot.get_channel(1217918087249002516)
    if channel:
      await channel.send(f"К нам присоединился {member.mention}!")
  except Exception as e:
    print(f'Произошла ошибка: {e}')

  

@bot.command(name='notif')
@commands.has_any_role('СОЗДАТЕЛЬ', 'Helper')
async def notif(ctx):
    notif_role = discord.utils.get(ctx.guild.roles, name="Уведомления")
    if not notif_role:
        notif_role = await ctx.guild.create_role(name="Уведомления")
    
    if notif_role not in ctx.author.roles:
      await ctx.author.add_roles(notif_role)
      await ctx.send(f'{ctx.author.mention} вы получили роль {notif_role.mention} и теперь вы будете получать уведомления по поводу игровых событий.')
    else:
      await ctx.send(f'{ctx.author.mention} вы сняли с себя роль {notif_role.mention} и теперь вы не будете получать уведомления по поводу игровых событий.')


@bot.command(name='clear')
@commands.has_any_role('СОЗДАТЕЛЬ', 'Helper')
@commands.has_permissions(manage_messages=True)
async def delete(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)



bot.run(config['token'])
