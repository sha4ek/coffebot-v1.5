import disnake, os
from disnake.ext import commands

from utils.functions import BotPrefix
from utils.config import BotSettings


Token = BotSettings['Token'] # переменная с токеном бота
OrangeColor = BotSettings['OrangeColor'] # переменная с цветом эмбеда
RedColor = BotSettings['RedColor'] # переменная с цветом эмбеда
GreenColor = BotSettings['GreenColor'] # переменная с цветом эмбеда


Bot = commands.Bot(command_prefix=BotPrefix, intents=disnake.Intents.all(), case_insensitive=True)
Bot.remove_command('help')


for file in os.listdir('./modules'):
    if file.endswith('.py'):
        Bot.load_extension(f'modules.{file[:-3]}')


@Bot.group(case_insensitive=True, invoke_without_command=True)
@commands.cooldown(1, 2.0, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@commands.is_owner()
async def modules(ctx):
    emb = disnake.Embed(
        title=f'Помощь по команде:',
        description=f'> **{ctx.prefix}modules load <модуль>** - подключить модуль\n'
                    f'> **{ctx.prefix}modules unload <модуль>** - отключить модуль\n'
                    f'> **{ctx.prefix}modules reload <модуль>** - перезагрузить модуль\n'
                    f'> **{ctx.prefix}modules info** - информация о модулях бота\n',
        color=OrangeColor
        )
    await ctx.send(embed=emb)


@modules.command()
@commands.cooldown(1, 2.0, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@commands.is_owner()
async def load(ctx, module = None):
    if module == None:
        emb = disnake.Embed(
            title='Ошибка:',
            description='> **Вы не указали модуль для подключения!**',
            color=RedColor
            )

    else:
        try:
            Bot.load_extension(f'modules.{module}')

            emb = disnake.Embed(
                title='Подключение модуля:',
                description=f'> **Модуль "{module}" успешно подключен!**',
                color=GreenColor
            )

        except commands.ExtensionNotFound:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы указали несуществующий модуль!**',
                color=RedColor
            )

        except commands.ExtensionAlreadyLoaded:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Указанный модуль уже подключен!**',
                color=RedColor
            )

    await ctx.send(embed=emb)


@modules.command()
@commands.cooldown(1, 2.0, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@commands.is_owner()
async def unload(ctx, module = None):
    if module == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не указали модуль для отключения!**',
                color=RedColor
            )
    
    else:
        try:
            Bot.unload_extension(f'modules.{module}')

            emb = disnake.Embed(
                title='Отключение модуля:',
                description=f'> **Модуль "{module}" успешно отключен!**',
                color=GreenColor
            )

        except commands.ExtensionNotFound:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы указали несуществующий модуль!**',
                color=RedColor
            )

        except commands.ExtensionNotLoaded:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Указанный модуль уже отключен!**',
                color=RedColor
            )

    await ctx.send(embed=emb)


@modules.command()
@commands.cooldown(1, 2.0, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@commands.is_owner()
async def reload(ctx, module = None):
    if module == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не указали модуль для переподключения!**',
                color=RedColor
            )

    else:
        try:
            Bot.reload_extension(f'modules.{module}')

            emb = disnake.Embed(
                title='Отключение модуля:',
                description=f'> **Модуль "{module}" успешно переподключен!**',
                color=GreenColor
            )

        except commands.ExtensionNotFound:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы указали несуществующий модуль!**',
                color=RedColor
            )

    await ctx.send(embed=emb)


@modules.command()
@commands.cooldown(1, 2.0, commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@commands.is_owner()
async def info(ctx):
    modules=''
    for file in os.listdir('./modules'):
        if file.endswith('.py'):
            if f'modules.{file[:-3]}' in Bot.extensions:
                modules += f'> **Модуль "{file[:-3]}":** подключен\n'
            else:
                modules += f'> **Модуль "{file[:-3]}":** отключен\n'

    emb = disnake.Embed(
        title='Информация о модулях:',
        description=f'{modules}',
        color=OrangeColor
    )

    await ctx.send(embed=emb)


Bot.run(Token)
