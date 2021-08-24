import asyncio
from discord.ext import commands
from utils.config import BotPostfix # импортируем конфиг бота


class Events(commands.Cog): # создаём класс модуля с ивентами
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.Cog.listener()
    async def on_ready(self): # создаём ивент запуска бота
        print(f'[SYSTEM] {self.Bot.user.name}\'s online!') # выводим событие в консоль

        seconds=0
        minutes=0
        hours=0
        days=0 # стандартные переменные времени

        while True: # создаём цикл
            seconds += 1 

            if seconds == 60:
                minutes += 1
                seconds = 0
            if minutes == 60:
                hours += 1
                minutes = 0
            if hours == 24:
                days += 1
                hours = 0

            if seconds != 0:
                file = open("uptime.txt", "w")
                file.write(f'{seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
                file.close()
            if minutes != 0:
                file = open("uptime.txt", "w")
                file.write(f'{minutes} {BotPostfix(minutes, "минута", "минуты", "минут")} {seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
                file.close()
            if hours != 0:
                file = open("uptime.txt", "w")
                file.write(f'{hours} {BotPostfix(hours, "час", "часа", "часов")} {minutes} {BotPostfix(minutes, "минута", "минуты", "минут")} {seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
                file.close()
            if days != 0:
                file = open("uptime.txt", "w")
                file.write(f'{days} {BotPostfix(days, "день", "дня", "дней")} {hours} {BotPostfix(hours, "час", "часа", "часов")} {minutes} {BotPostfix(minutes, "минута", "минуты", "минут")} {seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
                file.close()
            await asyncio.sleep(1)


def setup(Bot): # подключаем класс к основному файлу 
    Bot.add_cog(Events(Bot))
    print(f'[MODULES] Events\'s load!') # принтуем