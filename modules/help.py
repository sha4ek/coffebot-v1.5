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
        add_reactions=True, manage_messages=True)
    async def help(self, ctx): # создаём команду помощи
        emb1 = discord.Embed(title='Информационные команды:',
            description=f'**:chart_with_upwards_trend: {BotSettings["Bot"]["Prefix"][0]}stats** - немного статистики бота\n'
                        f'**:scroll: {BotSettings["Bot"]["Prefix"][0]}user [участник]** - информация об участнике\n'
                        f'**:page_facing_up: {BotSettings["Bot"]["Prefix"][0]}channel [канал]** - информация о канале\n'
                        f'**:notes: {BotSettings["Bot"]["Prefix"][0]}lyrics <песня>** - поиск текста песни\n',
            color=BotSettings['Bot']['BasicColor'])
        emb2 = discord.Embed(title='Фановые команды:',
            description=f'**:video_game: {BotSettings["Bot"]["Prefix"][0]}activity [ytt/chess/poker]** - активности в голосовом канале\n'
                        f'**:cat: {BotSettings["Bot"]["Prefix"][0]}cat** - картинки котиков') # делаем эмбеды
        emb3 = discord.Embed(title='Модерационые команды:',
            description=f'**:broom: {BotSettings["Bot"]["Prefix"][0]}clear <кол-во>** - очистка чата\n'
                        f'**:heavy_plus_sign: {BotSettings["Bot"]["Prefix"][0]}addrole <участник> <роль>** - добавление роли участнику\n'
                        f'**:hammer: {BotSettings["Bot"]["Prefix"][0]}ban <участник> [причина]** - бан участника\n'
                        f'**:mute: {BotSettings["Bot"]["Prefix"][0]}mute <участник>** - мьют участника\n'
                        f'**:sound: {BotSettings["Bot"]["Prefix"][0]}unmute <участник>** - размьют участника\n')
        emb4 = discord.Embed(title='Команды разработчика:',
            description=f'**:grey_exclamation: {BotSettings["Bot"]["Prefix"][0]}modules [load/unload/reload]** - управление модулями бота\n'
                        f'**:gear: {BotSettings["Bot"]["Prefix"][0]}jsk <функция> <код>** - исполнение кода ботом вне редактора')
        
        if ctx.author.id == BotSettings['Bot']['OwnerID']: # проверка на создателя бота
            embs = [emb1, emb2, emb3, emb4] # объединяем эмбеды
        else:
            embs = [emb1, emb2, emb3] # объединяем эмбеды
        message = await ctx.send(embed=emb1)
        pages = Paginator(self.Bot, message, embeds=embs, timeout=60, only=ctx.author, footer=False,
            color=BotSettings['Bot']['BasicColor']) # выставляем настройки страниц (Документация: https://github.com/RuCybernetic/Cybernator/blob/master/README_Ru.md)
        await pages.start() # запускаем страницы


def setup(Bot):  # подключаем класс к основному файлу 
    Bot.add_cog(Help(Bot))
    print(f'[MODULES] Help\'s load!') # принтуем
