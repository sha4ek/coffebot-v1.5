import discord
from discord.ext import commands
from Cybernator import Paginator # импортируем подмодуль для страниц (pip install Cybernator)
from utils.config import BotSettings # импортируем конфиг бота


class Help(commands.Cog): # создаём класс модуля команды помощи
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, read_message_history=True,
        add_reactions=True)
    async def help(self, ctx): # создаём команду помощи
        emb1 = discord.Embed(title='Информационные команды:',
            description=f'**:chart_with_upwards_trend: {ctx.prefix}stats** - немного статистики бота\n'
                        f'**:scroll: {ctx.prefix}user [участник]** - информация об участнике\n'
                        f'**:page_facing_up: {ctx.prefix}channel [канал]** - информация о канале\n',
            color=BotSettings['Bot']['BasicColor'])
        emb2 = discord.Embed(title='Фановые команды:',
            description=f'**:video_game: {ctx.prefix}activity [ytt/chess/poker]** - активности в голосовом канале\n'
                        f'**:cat: {ctx.prefix}cat** - картинки котиков') # делаем эмбеды
        emb3 = discord.Embed(title='Модерационые команды:',
            description=f'**:broom: {ctx.prefix}clear <кол-во>** - очистка чата\n'
                        f'**:heavy_plus_sign: {ctx.prefix}addrole <участник> <роль>** - добавление роли участнику\n'
                        f'**:hammer: {ctx.prefix}ban <участник> [причина]** - бан участника\n'
                        f'**:mute: {ctx.prefix}mute <участник>** - мьют участника\n'
                        f'**:sound: {ctx.prefix}unmute <участник>** - размьют участника\n'
                        f'**:flashlight: {ctx.prefix}prefix <префикс>** - установка префикса для сервера\n')
        emb4 = discord.Embed(title='Музыкальные команды:',
            description=f'**:notes: {ctx.prefix}lyrics <песня>** - поиск текста песни\n')
        emb5 = discord.Embed(title='Команды разработчика:',
            description=f'**:grey_exclamation: {ctx.prefix}modules [load/unload/reload]** - управление модулями бота\n'
                        f'**:gear: {ctx.prefix}jsk <функция> <код>** - исполнение кода ботом вне редактора')
        
        if ctx.author.id == BotSettings['Bot']['OwnerID']: # проверка на создателя бота
            embs = [emb1, emb2, emb3, emb4, emb5] # объединяем эмбеды
        else:
            embs = [emb1, emb2, emb3, emb4] # объединяем эмбеды
        message = await ctx.send(embed=emb1)
        pages = Paginator(self.Bot, message, embeds=embs, timeout=60, only=ctx.author, footer=False,
            color=BotSettings['Bot']['BasicColor'], use_remove_reaction=False) # выставляем настройки страниц (Документация: https://github.com/RuCybernetic/Cybernator/blob/master/README_Ru.md)
        await pages.start() # запускаем страницы


def setup(Bot):  # подключаем класс к основному файлу 
    Bot.add_cog(Help(Bot))
    print(f'[MODULES] Help\'s load!') # принтуем
