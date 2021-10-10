from disnake.ext import commands
from utils.config import MongoSettings, BotSettings


def BotPrefix(Bot, message):
    """Взятие префикса бота из базы данных"""

    GuildsData = MongoSettings['GuildsData'] # переменная с дата-базой монги
    MainPrefix = BotSettings['MainPrefix'] # переменная основного префикса

    if GuildsData.count_documents({'GuildID': message.guild.id}) == 0:
        GuildsData.insert_one({
            'GuildID': message.guild.id,
            'GuildPrefix': MainPrefix
            })

    GetPrefix = GuildsData.find_one({'GuildID': message.guild.id})

    return commands.when_mentioned_or(GetPrefix['GuildPrefix'])(Bot, message)


def BotPostfix(number: int, first_ending: str = 'день', second_ending: str = 'дня', third_ending: str = 'дней'):
    """Добавление постфикса к числам"""

    number = number % 10 if number > 20 else number
    return first_ending if number == 1 else second_ending if 1 < number < 5 else third_ending
