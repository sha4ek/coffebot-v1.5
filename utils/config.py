import os

BotPrefix = 'c.'
BotToken = os.environ.get('AppToken')
BotBasicColor = 0xdc9f56
BotErrorColor = 0xcf080f

def BotPostfix(num:int, end_1:str='год', end_2:str='года', end_3:str='лет'):
    num = num % 10 if num > 20 else num
    return end_1 if num == 1 else end_2 if 1 < num < 5 else end_3
