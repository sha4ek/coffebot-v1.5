from disnake.ext import commands
from utils.config import BotConfig, MongoConfig


def BotPrefix(bot, message):
    if not message.guild:
        return

    elif 'GuildPrefix' not in MongoConfig['GuildsData'].find_one({'GuildID': message.guild.id}):
        prefix = BotConfig['MainPrefix']
    
    else:
        prefix = MongoConfig['GuildsData'].find_one({'GuildID': message.guild.id})['GuildPrefix']

    return commands.when_mentioned_or(prefix)(bot, message)


def BotPostfix(number: int, first_ending: str='час', second_ending: str='часа', third_ending: str='часов'):
    number = number % 10 if number > 20 else number

    return first_ending if number == 1 else second_ending if 1 < number < 5 else third_ending
