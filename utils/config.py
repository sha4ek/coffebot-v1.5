import os
from pymongo import MongoClient


MongoConfig = {
    # База данных серверов
    'GuildsData': MongoClient(f'mongodb+srv://{os.environ.get("MongoKey")}.mongodb.net/CoffeeBase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE').CoffeeBase.guildsdata,
}


BotConfig = {
    # Основной префикс бота
    'MainPrefix': 'c.',
    # Токен бота
    'Token': os.environ.get('TokenKey'),
    # Токен мониторинга Blist
    'Blist': os.environ.get('BlistKey'),
    # Токен мониторинга Boticord
    'Boticord': os.environ.get('BoticordKey'),
    # Цвет эмбеда в обычных ситуациях
    'OrangeColor': 0xffa500,
    # Цвет эмбеда в ошибочных ситуациях
    'RedColor': 0xe32636,
    # Цвет эмбеда в успешных ситуациях
    'GreenColor': 0x90ee90,
    # Версия бота
    'BotVersion': '1.5',
    # Ссылка на приглашение бота
    'BotInvite': 'https://discord.com/api/oauth2/authorize?client_id=875927971649712148&permissions=92167&scope=bot',
    # Канал аудита неизвестных ошибок
    'ErrorsLogChannel': 896215788455886849,
    # Канал аудита серверов
    'GuildsLogChannel': 896215771347320872,
    # Канал аудита личных сообщений
    'PrivateMessagesLogChannel': 896546624615088130,
    # Канал аудита использованных команд
    'UsingCommandsLogChannel': 896546682068693002,
    # ID разработчика
    'DeveloperID': 546502974499717122
}
