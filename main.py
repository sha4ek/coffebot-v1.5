import discord
import os
from discord.ext import commands
from utils.config import BotPrefix, BotToken # импортируем конфиг бота


BotIntents = discord.Intents.default()
BotIntents.members = True
Bot = commands.Bot(command_prefix=BotPrefix, intents=BotIntents)
Bot.remove_command('help') # убираем стандартный help
Bot.load_extension('jishaku') # добавляем модуль jishaku для самописных команд


for file in os.listdir('./modules'): # открываем папку с модулями
    if file.endswith('.py'): # ищем файлы с расширением .py
        Bot.load_extension(f'modules.{file[:-3]}') # загружаем их, убирая расширение .py


Bot.run(BotToken)
