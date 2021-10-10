import disnake


DiscordPermissions = {
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
    'send_messages_in_threads': 'отправлять сообщения в ветки',
    'create_public_threads': 'создать публичные ветки',
    'create_private_threads': 'создание приватных веток',
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
    'use_application_commands': 'использовать команды приложения',
    'connect': 'подключаться',
    'speak': 'говорить',
    'video': 'видео',
    'use_voice_activity': 'использовать режим активации по голосу',
    'priority_speaker': 'приоритетный режим',
    'mute_members': 'отключать участникам микрофон',
    'deafen_members': 'отключать участникам звук',
    'move_members': 'перемещать участников',
    'administrator': 'администратор'
}


DiscordStatuses = {
    disnake.Status.online: 'в сети',
    disnake.Status.idle: 'неактивен',
    disnake.Status.dnd: 'не беспокоить',
    disnake.Status.offline: 'не в сети'
}


DiscordSlowmods = {
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
}


DiscordVerificationLevel = {
    disnake.VerificationLevel.low: 'низкий',
    disnake.VerificationLevel.medium: 'средний',
    disnake.VerificationLevel.high: 'высокий',
    disnake.VerificationLevel.highest: 'очень высокий'
}
