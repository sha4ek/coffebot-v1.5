import discord, datetime, requests
from discord.ext import commands
from utils.config import BotSettings, BotPostfix # импортируем конфиг бота


class Information(commands.Cog): # создаём класс модуля информации
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def stats(self, ctx): # создаём команду статистики
        file = open("uptime.txt", "r") # открываем файл аптайма
        uptime = file.read() # читаем его
        file.close() # закрываем

        emb = discord.Embed(title='Статистика бота:',
            description=f'**:books: Всего серверов:** {len(self.Bot.guilds)}\n'
                        f'**:busts_in_silhouette: Всего пользователей:** {len(self.Bot.users)}\n'
                        f'**:ping_pong: Текущая задержка:** {self.Bot.ws.latency * 1000:.0f}мс\n'
                        f'**:satellite_orbital: Время работы:** {uptime}', color=BotSettings['Bot']['BasicColor']) # создаём эмбед
        await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def user(self, ctx, member: discord.Member=None):
        if member == None: user = ctx.author
        else: user = member # проверка на участника

        create_time = (datetime.datetime.today()-user.created_at).days # узнаём дату регистрации участника
        join_time = (datetime.datetime.today()-user.joined_at).days # узнаём дату входа на сервер участника

        if create_time == 0:
            create_day = f'{user.created_at.strftime("%d.%m.%Y")} (Меньше дня назад)'
        else:
            create_day = f'{user.created_at.strftime("%d.%m.%Y")} ({create_time} {BotPostfix(create_time, "день", "дня", "дней")} назад)'

        if join_time == 0:
            join_day = f'{user.joined_at.strftime("%d.%m.%Y")} (Меньше дня назад)'
        else:
            join_day = f'{user.joined_at.strftime("%d.%m.%Y")} ({join_time} {BotPostfix(join_time, "день", "дня", "дней")} назад)'

        if user.status == discord.Status.online: status = '**:green_circle: Статус:** В сети'
        elif user.status == discord.Status.offline: status = '**:black_circle: Статус:** Не в сети'
        elif user.status == discord.Status.idle: status = '**:orange_circle: Статус:** Неактивен'
        elif user.status == discord.Status.dnd: status = '**:red_circle: Статус:** Не беспокоить'

        activity = ''
        for i in user.activities:
            if i.type == discord.ActivityType.custom:
                activity += f'**:sparkles: Пользовательский статус:** {i.name}\n'
            if i.type == discord.ActivityType.playing:
                activity += f'**:video_game: Играет в:** {i.name}\n'
            if i.type == discord.ActivityType.listening:
                artists = ''
                for j in i.artists:
                    	artists += f'{j}'
                activity += f'**:musical_note: Слушает:** {i.title} ({", ".join(i.artists)})\n'

        emb = discord.Embed(title=f'Информация об участнике:',
            description=f'**:pencil: Никнейм:** {user.name}\n'
                        f'**:id: Идентификатор:** {user.id}\n'
                        f'**:notebook_with_decorative_cover: Создал аккаунт Discord:** {create_day}\n'
                        f'**:door: Присоединился к серверу:** {join_day}\n'
                        f'**:arrow_up: Наивысшая роль:** <@&{user.top_role.id}>\n'
                        f'{status}\n'
                        f'{activity}', color=user.color)
        emb.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def channel(self, ctx, text_channel: discord.TextChannel=None):
        if text_channel == None: channel = ctx.channel
        else: channel = text_channel

        create_time = (datetime.datetime.now() - channel.created_at).days

        if channel.slowmode_delay == 0: slowmode=''
        else: slowmode=f'**:sleeping_accommodation: Задержка:** {BotSettings["ChannelSlowmode"][channel.slowmode_delay]}\n'

        if channel.category == None: category=''
        else: category=f'**:beginner: Категория:** {channel.category}\n'

        if channel.topic == None: topic=''
        else: topic=f'**:page_facing_up: Описание:** {channel.topic}\n'

        if create_time == 0:
            create_day = f'{channel.created_at.strftime("%d.%m.%Y")} (Меньше дня назад)'
        else:
            create_day = f'{channel.created_at.strftime("%d.%m.%Y")} ({create_time} {BotPostfix(create_time, "день", "дня", "дней")} назад)'

        emb = discord.Embed(title='Информация о канале:',
            description=f'**:pencil: Название:** {channel.name}\n'
                        f'**:id: Идентификатор:** {channel.id}\n'
                        f'{slowmode}'
                        f'{category}'
                        f'{topic}'
                        f'**:notebook_with_decorative_cover: Создан:** {create_day}',
            color=BotSettings['Bot']['BasicColor'])
        await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def lyrics(self, ctx, *, music = None):
        if music == None:
            emb = discord.Embed(title='Ошибка:', description='**:anger: Вы не указали песню!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        else:
            response = requests.get(f'https://some-random-api.ml/lyrics?title={music}')
            lyric = response.json()

            emb = discord.Embed(title=f'{lyric["title"]} ({lyric["author"]})',
                description=f'**:link: Ссылка:** {lyric["links"]["genius"]}\n'
                            f'**:page_facing_up: Текст:** {lyric["lyrics"]}',
                color=BotSettings['Bot']['BasicColor'])
            emb.set_thumbnail(url=lyric['thumbnail']['genius'])
            await ctx.send(embed=emb)



def setup(Bot): # подключаем класс к основному файлу 
    Bot.add_cog(Information(Bot))
    print(f'[MODULES] Information\'s load!') # принтуем
