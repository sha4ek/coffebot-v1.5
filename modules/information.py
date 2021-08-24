import discord
from discord.ext import commands
from utils.config import BotBasicColor # импортируем конфиг бота


class Information(commands.Cog): # создаём класс модуля информации
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    async def stats(self, ctx): # создаём команду статистики
        file = open("uptime.txt", "r") # открываем файл аптайма
        uptime = file.read() # читаем его
        file.close() # закрываем

        emb = discord.Embed(title='Статистика бота:',
            description=f'**:books: Всего серверов:** {len(self.Bot.guilds)}\n'
                        f'**:busts_in_silhouette: Всего пользователей:** {len(self.Bot.users)}\n'
                        f'**:satellite_orbital: Время работы:** {uptime}', color=BotBasicColor) # создаём эмбед
        await ctx.send(embed=emb)


def setup(Bot): # подключаем класс к основному файлу 
    Bot.add_cog(Information(Bot))
    print(f'[MODULES] Information\'s load!') # принтуем