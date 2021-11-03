import disnake, psutil, os, math, platform, sys
from disnake.ext import commands

from utils.config import BotSettings
from utils.translations import DiscordStatuses, DiscordSlowmods


OrangeColor = BotSettings['OrangeColor'] # переменная с цветом эмбеда


class Information(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def stats(self, ctx):
        size_name = ('б', 'кб', 'мб', 'гб', 'тб')
        disnake_version = f'v{disnake.version_info[0]}.{disnake.version_info[1]}.{disnake.version_info[2]}'
        python_version = f'v{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}'
        platform_bit = 'x64' if '64bit' in platform.architecture(bits='') else 'x86'

        used = psutil.Process(os.getpid()).memory_info().rss
        i = int(math.floor(math.log(used, 1024)))
        p = math.pow(1024, i)
        s = round(used / p, 2)
        used_bot = '%s%s' % (s, size_name[i])

        total = psutil.virtual_memory().total
        i = int(math.floor(math.log(total, 1024)))
        p = math.pow(1024, i)
        s = round(total / p, 2)
        total_bot = '%s%s' % (s, size_name[i])

        emb = disnake.Embed(
            title='Статистика бота:',
            description=f'> **Количество серверов:** {len(self.Bot.guilds)}\n'
                        f'> **Количество пользователей:** {len(self.Bot.users)}\n'
                        f'> **Количество команд:** {len(self.Bot.commands)}\n'
                        f'> **Текущая задержка:** {self.Bot.ws.latency * 1000:.0f}мс\n'
                        f'> **Версия бота:** {BotSettings["BotVersion"]}\n'
                        f'> **Версия Disnake:** {disnake_version}\n'
                        f'> **Версия Python:** {python_version}\n'
                        f'> **Система:** {platform.system()} {platform.release()} ({platform_bit})\n'
                        f'> **Использованно ОЗУ:** {used_bot}/{total_bot}',
            color=OrangeColor
        )

        await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def user(self, ctx, member: disnake.Member = None):
        user = ctx.author if member == None else member

        activities = ''
        for i in user.activities:
            if i.type == disnake.ActivityType.custom:
                activities += f'> **Пользовательский статус:** {i.name}\n'

            if i.type == disnake.ActivityType.playing:
                activities += f'> **Играет в:** {i.name}\n'

            if i.type == disnake.ActivityType.listening:
                artist = ''
                for artists in i.artists:
                    	artist += f'{artists}'

                activities += f'> **Слушает:** {i.title} ({", ".join(i.artists)})\n'

        emb = disnake.Embed(
            title='Информация об участнике:',
            description=f'> **Никнейм:** {user.name}\n'
                        f'> **Идентификатор:** {user.id}\n'
                        f'> **Создал аккаунт Discord:** <t:{int(user.created_at.timestamp())}:D>\n'
                        f'> **Присоединился к серверу:** <t:{int(user.joined_at.timestamp())}:D>\n'
                        f'> **Наивысшая роль:** {user.top_role.mention}\n'
                        f'> **Статус:** {DiscordStatuses[user.status]}\n'
                        f'{activities}',
            color=OrangeColor
        )
        emb.set_thumbnail(url=user.avatar)

        await ctx.send(embed=emb)

    
    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def server(self, ctx):

        emb = disnake.Embed(
            title='Информация о сервере:',
            description=f'> **Название:** {ctx.guild}\n'
                        f'> **Владелец:** {ctx.guild.owner.mention}\n'
                        f'> **Создан:** <t:{int(ctx.guild.created_at.timestamp())}:D>\n'
                        f'> **Количество каналов:** {len(ctx.guild.channels)}\n'
                        f'> **Количество ролей:** {len(ctx.guild.roles)}\n'
                        f'> **Количество участников:** {ctx.guild.member_count}\n',
            color=OrangeColor
        )
        emb.set_thumbnail(url=ctx.guild.icon)
        
        if ctx.guild.banner:
            emb.set_image(url=ctx.guild.banner)

        await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def channel(self, ctx, text_channel: disnake.TextChannel = None):
        channel = ctx.channel if text_channel == None else text_channel

        if channel.slowmode_delay == 0: slowmode = ''
        else: slowmode = f'> **Задержка:** {DiscordSlowmods[channel.slowmode_delay]}\n'

        if channel.category == None: category = ''
        else: category = f'> **Категория:** {channel.category}\n'

        if channel.topic == None: topic = ''
        else: topic = f'> **Описание:** {channel.topic}\n'

        emb = disnake.Embed(
            title='Информация о канале:',
            description=f'> **Название:** {channel}\n'
                        f'> **Идентификатор:** {channel.id}\n'
                        f'{slowmode}{category}{topic}'
                        f'> **Создан:** <t:{int(channel.created_at.timestamp())}:D>',
            color=OrangeColor
        )

        await ctx.send(embed=emb)


def setup(Bot):
    Bot.add_cog(Information(Bot))
    print(f'[MODULES] Module "Information" is loaded!')
