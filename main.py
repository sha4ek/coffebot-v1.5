import discord, os, time, re
from discord.ext import commands
from config import Prefix


print(f'[{time.strftime("%H:%M")}] System: Connecting to Discord...')


Bot = commands.Bot(command_prefix=Prefix, intents=discord.Intents.all())
Bot.remove_command('help')
Bot.load_extension("jishaku")


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        Bot.load_extension(f'cogs.{file[:-3]}')


@Bot.command(
    aliases=['модуль', 'cogs', 'коги'],
    brief='Управление модулями бота',
    usage=f'{Prefix}module [функция] (модуль)')
@commands.is_owner()
async def module(ctx, func, module=None):
    loadfunc = ['load', 'загрузить', 'on', 'включить']
    unloadfunc = ['unload', 'выгрузить', 'off', 'выключить']
    reloadfunc = ['reload', 'перезагрузить', 're']
    listfunc = ['list', 'список']

    if func in loadfunc:
        if module==None:
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Ты не указал модуль**',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        else:
            try:
                Bot.load_extension(f'cogs.{module}')

                emb = discord.Embed(
                    title='Включение модуля:',
                    description=f'**⚠ Модуль {module} подключен**',
                    color=ctx.author.color)
                await ctx.send(embed=emb)
            except commands.ExtensionAlreadyLoaded:
                emb = discord.Embed(
                    title='Ошибка:',
                    description='**💢 Данный модуль уже подключен**',
                    color=ctx.author.color)
                await ctx.send(embed=emb)
            except commands.ExtensionNotFound:
                emb = discord.Embed(
                    title='Ошибка:',
                    description='**💢 Данного модуля не существует**',
                    color=ctx.author.color)
                await ctx.send(embed=emb)
    
    elif func in unloadfunc:
        if module==None:
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Ты не указал модуль**',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        else:
            try:
                Bot.unload_extension(f'cogs.{module}')

                emb = discord.Embed(
                    title='Выключение модуля:',
                    description=f'**⚠ Модуль {module} отключен**',
                    color=ctx.author.color)
                await ctx.send(embed=emb)
            except commands.ExtensionNotLoaded:
                emb = discord.Embed(
                    title='Ошибка:',
                    description='**💢 Данный модуль уже отключен или же его не существует**',
                    color=ctx.author.color)
                await ctx.send(embed=emb)

    elif func in reloadfunc:
        if module==None:
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Ты не указал модуль**',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        else:
            try:
                Bot.reload_extension(f'cogs.{module}')
    
                emb = discord.Embed(
                    title='Перезагрузка модуля:',
                    description=f'**⚠ Модуль {module} перезагружен**',
                    color=ctx.author.color)
                await ctx.send(embed=emb)
            except commands.ExtensionNotLoaded:
                emb = discord.Embed(
                    title='Ошибка:',
                    description='**💢 Данного модуля не существует**',
                    color=ctx.author.color)
                await ctx.send(embed=emb)

    elif func in listfunc:
        maintext = ''.join(Bot.extensions)
        midtext = re.sub(r'jishakucogs.', '', maintext)
        featext = re.sub(r'cogs.', '\n🗂 ', midtext)

        emb = discord.Embed(
            title='Модули бота:',
            description=f'**🗂 {featext}**',
            color=ctx.author.color)
        await ctx.send(embed=emb)


token = os.environ.get('Token')
Bot.run(token)
