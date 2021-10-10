import os
from pymongo import MongoClient


MongoSettings = {
    # База данных серверов
    'GuildsData': MongoClient(f'mongodb+srv://{os.environ.get("MongoKey")}/TestCoffeebase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE').Coffeebase.guilds_data
}


BotSettings = {
    # Основной префикс бота
    'MainPrefix': 'cb.',
    # Токен бота
    'Token': os.environ.get('TokenKey'),
    # Цвет эмбеда в обычных ситуациях
    'OrangeColor': 0xffa500,
    # Цвет эмбеда в ошибочных ситуациях
    'RedColor': 0xe32636,
    # Цвет эмбеда в успешных ситуациях
    'GreenColor': 0x90ee90,
    # Версия бота
    'BotVersion': 'v1.4',
    # Ссылка на сервер поддержки
    'SupportGuild': 'https://discord.gg/7Ja4JNcqUB',
    # Ссылка на приглашение бота
    'BotInvite': 'https://discord.com/api/oauth2/authorize?client_id=875927971649712148&permissions=268528647&scope=bot',
    # Канал аудита неизвестных ошибок бота
    'ErrorsLogChannel': 896215788455886849,
    # Канал аудита серверов бота
    'GuildsLogChannel': 896215771347320872,
    # Канал аудита личных сообщений бота
    'PrivateMessagesLogChannel': 896546624615088130,
    # Канал аудита использованных команд бота
    'CommandsLogChannel': 896546682068693002
}
