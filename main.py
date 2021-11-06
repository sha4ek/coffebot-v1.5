import disnake as discord
import os
from disnake.ext import commands
from utils.functions import BotPrefix
from utils.config import BotConfig

BotIntents = discord.Intents.default()
BotIntents.members = True
BotIntents.presences = True

bot = commands.Bot(command_prefix=BotPrefix, intents=BotIntents, case_insensitive=True)
bot.remove_command('help')


for file in os.listdir('./modules'):
    if file.endswith('.py'):
        try:
            bot.load_extension(f'modules.{file[:-3]}')
        except Exception as exception:
            print(f'[ERROR] Module "{file[:-3]}" wasn\'t loaded! {exception.original}')


@bot.group(case_insensitive=True, invoke_without_command=True)
@commands.cooldown(1, 2.0, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@commands.is_owner()
async def modules(ctx):
    emb = discord.Embed(title=f'Помощь по команде:',
        description=f'> **{BotPrefix(bot, ctx.message)[2]}modules load <модуль>** - подключить модуль\n'
                    f'> **{BotPrefix(bot, ctx.message)[2]}modules unload <модуль>** - отключить модуль\n'
                    f'> **{BotPrefix(bot, ctx.message)[2]}modules reload <модуль>** - переподключить модуль\n'
                    f'> **{BotPrefix(bot, ctx.message)[2]}modules info** - информация о модулях бота',
        color=BotConfig['OrangeColor'])
    await ctx.send(embed=emb)


@modules.command()
@commands.cooldown(1, 2.0, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@commands.is_owner()
async def load(ctx, module=None):
    if not module:
        emb = discord.Embed(title='Ошибка:',
            description='> **Вы не указали модуль для подключения!**',
            color=BotConfig['RedColor'])

    else:
        try:
            bot.load_extension(f'modules.{module}')

            emb = discord.Embed(title='Подключение модуля:',
                description=f'> **Модуль "{module}" успешно подключен!**',
                color=BotConfig['GreenColor'])

        except commands.ExtensionNotFound:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы указали несуществующий модуль!**',
                color=BotConfig['RedColor'])

        except commands.ExtensionAlreadyLoaded:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы указали уже подключенный модуль!**',
                color=BotConfig['RedColor'])

        except commands.ExtensionFailed as ExtensionFailed:
            emb = discord.Embed(title='Ошибка:',
                description='> **Произошла ошибка при загрузке модуля!**\n'
                            f'```py\n{ExtensionFailed.original}\n```',
                color=BotConfig['RedColor'])

    await ctx.send(embed=emb)


@modules.command()
@commands.cooldown(1, 2.0, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@commands.is_owner()
async def unload(ctx, module=None):
    if not module:
        emb = discord.Embed(title='Ошибка:',
            description='> **Вы не указали модуль для отключения!**',
            color=BotConfig['RedColor'])
    
    else:
        try:
            bot.unload_extension(f'modules.{module}')

            emb = discord.Embed(title='Отключение модуля:',
                description=f'> **Модуль "{module}" успешно отключен!**',
                color=BotConfig['GreenColor'])

        except commands.ExtensionNotLoaded:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы указали несуществующий или уже отключенный модуль!**',
                color=BotConfig['RedColor'])

    await ctx.send(embed=emb)


@modules.command()
@commands.cooldown(1, 2.0, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@commands.is_owner()
async def reload(ctx, module=None):
    if not module:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не указали модуль для переподключения!**',
                color=BotConfig['RedColor'])

    else:
        try:
            bot.reload_extension(f'modules.{module}')

            emb = discord.Embed(title='Переподключение модуля:',
                description=f'> **Модуль "{module}" успешно переподключен!**',
                color=BotConfig['GreenColor'])

        except commands.ExtensionNotLoaded:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы указали несуществующий или отключенный модуль!**',
                color=BotConfig['RedColor'])

    await ctx.send(embed=emb)


@modules.command()
@commands.cooldown(1, 2.0, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@commands.is_owner()
async def info(ctx):
    modules = ''
    for file in os.listdir('./modules'):
        if file.endswith('.py'):
            if f'modules.{file[:-3]}' in bot.extensions:
                modules += f'> **Модуль "{file[:-3]}"** - подключен\n'
            else:
                modules += f'> **Модуль "{file[:-3]}"** - отключен\n'

    emb = discord.Embed(title='Информация о модулях:',
        description=f'{modules}',
        color=BotConfig['OrangeColor'])
    await ctx.send(embed=emb)


bot.run(BotConfig['Token'])
