import discord, datetime, time, psutil, math, os
from discord.ext import commands
from config import Postfix, Prefix


class information(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    
    @commands.command(
        aliases=['ботинфо', 'bot', 'бот'],
        brief='Показать немного информации о боте',
        usage=f'{Prefix}botinfo')
    async def botinfo(self, ctx):
        size_bytes = psutil.Process(os.getpid()).memory_info().rss

        if size_bytes == 0:
            size_bot = '0б'

        size_name = ('б', 'кб', 'мб', 'гб', 'тб')
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        size_bot = '%s%s' % (s, size_name[i])

        if ctx.author.id != 546502974499717122:
            emb = discord.Embed(
                title='Информация о боте:',
                description=f'**⏱ Текущая задержка бота:** {self.Bot.ws.latency * 1000:.0f}мс\n'
                            f'**⛺ Количество серверов:** {len(self.Bot.guilds)}',
                color=ctx.author.color)
        else:
            emb = discord.Embed(
                title='Информация о боте:',
                description=f'**⏱ Текущая задержка бота:** {self.Bot.ws.latency * 1000:.0f}мс\n'
                            f'**⛺ Количество серверов:** {len(self.Bot.guilds)}\n'
                            f'**🎚 Количество занимаемой памяти:** {size_bot}',
                color=ctx.author.color)
        await ctx.send(embed=emb)


    @commands.command(
        aliases=['юзеринфо', 'user', 'юзер'],
        brief='Показать немного информации об участнике',
        usage=f'{Prefix}userinfo')
    async def userinfo(self, ctx, member: discord.Member=None):
        if member == None: user = ctx.author
        else: user = member

        create_time = (datetime.datetime.today()-user.created_at).days
        join_time = (datetime.datetime.today()-user.joined_at).days
        ServerSupport = [716566697930129448, 694438331622096908]

        if create_time == 0: create_day = f'{user.created_at.strftime("%d.%m.%Y")} (Меньше дня назад)'
        else: create_day = f'{user.created_at.strftime("%d.%m.%Y")} ({create_time} {Postfix(create_time, "день", "дня", "дней")} назад)'

        if join_time == 0: join_day = f'{user.joined_at.strftime("%d.%m.%Y")} (Меньше дня назад)'
        else: join_day = f'{user.joined_at.strftime("%d.%m.%Y")} ({join_time} {Postfix(join_time, "день", "дня", "дней")} назад)'

        if user.status == discord.Status.online: status = '**🟢 Статус:** В сети'
        elif user.status == discord.Status.offline: status = '**⚫ Статус:** Не в сети'
        elif user.status == discord.Status.idle: status = '**🟠 Статус:** Неактивен'
        elif user.status == discord.Status.dnd: status = '**🔴 Статус:** Не беспокоить'

        emb = discord.Embed(
            title=f'Информация об участнике:',
            description=f'**📝 Никнейм:** {user.name}\n'
                        f'**🆔 Идентификатор:** {user.id}\n'
                        f'**📔 Создал аккаунт Discord:** {create_day}\n'
                        f'**🚪 Присоединился к серверу:** {join_day}\n'
                        f'**⬆ Наивысшая роль:** <@&{user.top_role.id}>\n'
                        f'{status}',
            color=user.color)
        emb.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=emb)


    @commands.command(
        aliases=['серверинфо', 'server', 'сервер'],
        brief='Показать немного информации о сервере',
        usage=f'{Prefix}serverinfo')
    async def serverinfo(self, ctx):
        create_time = (datetime.datetime.today()-ctx.guild.created_at).days

        if create_time == 0: create_day = f'{ctx.guild.created_at.strftime("%d.%m.%Y")} (Меньше дня назад)'
        else: create_day = f'{ctx.guild.created_at.strftime("%d.%m.%Y")} ({create_time} {Postfix(create_time, "день", "дня", "дней")} назад)'

        emb = discord.Embed(
            title='Информация о сервере:',
            description=f'**📝 Название:** {ctx.guild.name}\n'
                        f'**🛎 Владелец:** {ctx.guild.owner.mention}\n'
                        f'**📔 Создан:** {create_day}\n'
                        f'**🛡 Уровень проверки:** {ctx.guild.verification_level}\n'
                        f'**🎹 Каналов:** {len(ctx.guild.channels)}\n'
                        f'**🏵 Ролей:** {len(ctx.guild.roles)}\n'
                        f'**😀 Участников:** {len(ctx.guild.members)}\n',
            color=ctx.author.color)
        emb.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=emb)


def setup(Bot):
    Bot.add_cog(information(Bot))
    print(f'[{time.strftime("%H:%M")}] Cogs: Information\'s load!')
