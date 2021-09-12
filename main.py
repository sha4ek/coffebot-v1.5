import discord, os # импортируем библиотеки
from discord.ext import commands
from utils.config import BotSettings, GetPrefix


BotIntents = discord.Intents.all()
Bot = commands.Bot(command_prefix=GetPrefix, intents=BotIntents, case_insensitive=True)
Bot.remove_command('help') # убираем стандартный help
Bot.load_extension('jishaku') # добавляем модуль jishaku для самописных команд


for file in os.listdir('./modules'): # открываем папку с модулями
    if file.endswith('.py'): # ищем файлы с расширением .py
        Bot.load_extension(f'modules.{file[:-3]}') # загружаем их, убирая расширение .py


@Bot.command()
@commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@commands.is_owner()
async def modules(ctx, func=None, module=None):
    if func == 'load':
        if module == None:
            emb = discord.Embed(title='Ошибка:', description='**:anger: Вы не указали модуль!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        else:
            Bot.load_extension(f'modules.{module}')

            emb = discord.Embed(title='Подключение модуля:',
                description=f'**:white_check_mark: Модуль {module} успешно подключен**',
                color=BotSettings['Bot']['NormalColor'])
            await ctx.send(embed=emb)
    
    elif func == 'unload':
        if module == None:
            emb = discord.Embed(title='Ошибка:', description='**:anger: Вы не указали модуль!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        else:
            Bot.unload_extension(f'modules.{module}')

            emb = discord.Embed(title='Отключение модуля:',
                description=f'**:white_check_mark: Модуль {module} успешно отключен**',
                color=BotSettings['Bot']['NormalColor'])
            await ctx.send(embed=emb)

    elif func == 'reload':
        if module == None:
            emb = discord.Embed(title='Ошибка:', description='**:anger: Вы не указали модуль!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        else:
            Bot.reload_extension(f'modules.{module}')

            emb = discord.Embed(title='Перезагрузка модуля:',
                description=f'**:white_check_mark: Модуль {module} успешно перезагружен**',
                color=BotSettings['Bot']['NormalColor'])
            await ctx.send(embed=emb)

    elif func == None:
        modules=''
        for file in os.listdir('./modules'):
            if file.endswith('.py'):
                if f'modules.{file[:-3]}' in Bot.extensions:
                    modules += f'**:green_circle: {file[:-3]}**\n'
                else:
                    modules += f'**:black_circle: {file[:-3]}**\n'

        emb = discord.Embed(title='Функции команды и модули бота:',
            description=f'**Функции:**\n'
                        f'**:inbox_tray: load <модуль>** - подключить модуль\n'
                        f'**:outbox_tray: unload <модуль>** - отключить модуль\n'
                        f'**:package: reload <модуль>** - перезагрузить модуль\n\n'
                        f'**Модули:**\n'
                        f'{modules}', color=BotSettings['Bot']['BasicColor'])
        await ctx.send(embed=emb)


Bot.run(BotSettings['Bot']['Token'])
