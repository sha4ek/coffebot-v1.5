import os, time
from pymongo import MongoClient


BotSettings = {
    'Bot': {
        'Token': os.environ.get('AppToken'), # токен бота
        'MainPrefix': 'c.', # префикс бота
        'BasicColor': 0xdc9f56, # обычный цвет рамки
        'ErrorColor': 0xcf080f, # цвет рамки при ошибке
        'NormalColor': 0x80d7a4, # цвет рамки при верном решении
        'OwnerID': 546502974499717122, # ID разработчика бота
        'ErrorsLogChannel': 880968020980273173,
        'GuildsLogChannel': 883974406446149633
    },
    'Mongo': {
        'Collection': MongoClient(os.environ.get('MongoToken')).Coffeebase
    },
    'Permissions': {
        'view_channel': 'просматривать каналы',
        'manage_channels': 'управлять каналами',
        'manage_roles': 'управлять ролями',
        'manage_emojis_and_stickers': 'управлять эмодзи и стикерами',
        'view_audit_log': 'просматривать журнала аудита',
        'view_guild_insinghts': 'просмотр аналитики сервера',
        'manage_webhooks': 'управлять вебхуками (webhooks)',
        'manage_guild': 'управлять сервером',
        'create_instant_invite': 'создание приглашения',
        'change_nickname': 'изменить никнейм',
        'manage_nicknames': 'управлять никнеймами',
        'kick_members': 'выгонять участников',
        'ban_members': 'банить участников',
        'send_messages': 'отправлять сообщения',
        'send_messages_in_threads': 'send messages in threads (coming soon)',
        'use_public_threads': 'use public threads',
        'use_private_threads': 'use private threads',
        'embed_links': 'встраивать ссылки',
        'attach_files': 'прикреплять файлы',
        'add_reactions': 'добавлять реакции',
        'use_external_emojis': 'использовать внешние эмодзи',
        'use_external_stickers': 'использовать внешние стикеры',
        'mention_everyone': 'упоминание @everyone, @here и всех ролей',
        'manage_messages': 'управлять сообщениями',
        'manage_threads': 'управление ветками',
        'read_message_history': 'читать историю сообщений',
        'send_tts_messages': 'отправка сообщений text-to-speech',
        'use_application_commands': 'use application commands',
        'connect': 'подключаться',
        'speak': 'говорить',
        'video': 'видео',
        'use_voice_activity': 'использовать режим активации по голосу',
        'priority_speaker': 'приоритетный режим',
        'mute_members': 'отключать участникам микрофон',
        'deafen_members': 'отключать участникам звук',
        'move_members': 'перемещать участников',
        'request_to_speak': 'попросить выступить',
        'administrator': 'администратор'
    },
    'ChannelSlowmode': {
        5: '5 секунд',
        10: '10 секунд',
        15: '15 секунд',
        30: '30 секунд',
        60: '1 минута',
        120: '2 минуты',
        300: '5 минут',
        600: '10 минут',
        900: '15 минут',
        1800: '30 минут',
        3600: '1 час',
        7200: '2 часа',
        21600: '6 часов'
    },
    'BoticordToken': os.environ.get('BoticordToken')
}


def BotPostfix(num: int, end_1: str='год', end_2: str='года', end_3: str='лет'): # функция постфикса
    num = num % 10 if num > 20 else num
    return end_1 if num == 1 else end_2 if 1 < num < 5 else end_3


def BotUptime():
    seconds = 0
    minutes = 0
    hours = 0
    days = 0 # стандартные переменные времени

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
            file = open('uptime.txt', 'w')
            file.write(f'{seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
            file.close()

        if minutes != 0:
            file = open('uptime.txt', 'w')
            file.write(f'{minutes} {BotPostfix(minutes, "минута", "минуты", "минут")} {seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
            file.close()

        if hours != 0:
            file = open('uptime.txt', 'w')
            file.write(f'{hours} {BotPostfix(hours, "час", "часа", "часов")} {minutes} {BotPostfix(minutes, "минута", "минуты", "минут")} {seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
            file.close()

        if days != 0:
            file = open('uptime.txt', 'w')
            file.write(f'{days} {BotPostfix(days, "день", "дня", "дней")} {hours} {BotPostfix(hours, "час", "часа", "часов")} {minutes} {BotPostfix(minutes, "минута", "минуты", "минут")} {seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
            file.close()
        time.sleep(1)
        
        
def GetPrefix(Bot, message):
    collection = BotSettings['Mongo']['Collection'].custom_prefix

    if collection.count_documents({'guild_id': message.guild.id}) == 0: # проверка на присутствие сервера в базе
        collection.insert_one({
            'guild_name': message.guild.name,
            'guild_id': message.guild.id,
            'guild_owner_name': f'{message.guild.owner.name}#{message.guild.owner.discriminator}',
            'guild_owner_id': message.guild.owner.id,
            'guild_prefix': BotSettings['Bot']['MainPrefix']
            })
        
        prefix = collection.find_one({'guild_id': message.guild.id})
        return prefix['guild_prefix']
    else:
        prefix = collection.find_one({'guild_id': message.guild.id}) # если есть то берем его оттуда
        return prefix['guild_prefix']
