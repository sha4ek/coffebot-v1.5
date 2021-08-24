import os

BotPrefix = 'c.' # префикс бота
BotToken = os.environ.get('AppToken') # токен бота
BotBasicColor = 0xdc9f56 # обычный цвет рамки
BotErrorColor = 0xcf080f # цвет рамки при ошибке
BotNormalColor = 0x80d7a4 # цвет рамки при верном решении


def BotPostfix(num: int, end_1: str='год', end_2: str='года', end_3: str='лет'): # функция постфикса
    num = num % 10 if num > 20 else num
    return end_1 if num == 1 else end_2 if 1 < num < 5 else end_3
