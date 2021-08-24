import discord
from discord.ext import commands
from Cybernator import Paginator # импортируем подмодуль для страниц (pip install Cybernator)
from utils.config import BotBasicColor, BotPrefix # импортируем конфиг бота


class Help(commands.Cog): # создаём класс модуля команды помощи
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    async def help(self, ctx): # создаём команду помощи
        reacts = ['<a:left_arrow:879595659261513728>', '<a:right_arrow:879595659253149726>'] # делаем список пользовательских реакций

        emb1 = discord.Embed(title='Информационные команды:',
            description=f'**:chart_with_upwards_trend: {BotPrefix}stats** - немного статистики бота',
            color=BotBasicColor)
        emb2 = discord.Embed(title='Фановые команды:',
            description=f'**:video_game: {BotPrefix}activity [ytt/chess/poker]** - активности в голосовом канале') # делаем эмбеды
        embs = [emb1, emb2] # объединяем эмбеды
        message = await ctx.send(embed=emb1)
        pages = Paginator(self.Bot, message, embeds=embs, timeout=60, only=ctx.author, footer=False, reactions=reacts,
            color=BotBasicColor, use_remove_reaction=False) # выставляем настройки страниц (Документация: https://github.com/RuCybernetic/Cybernator/blob/master/README_Ru.md)
        await pages.start() # запускаем страницы


def setup(Bot):  # подключаем класс к основному файлу 
    Bot.add_cog(Help(Bot))
    print(f'[MODULES] Help\'s load!') # принтуем