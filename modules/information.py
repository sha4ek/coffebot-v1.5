import disnake as discord
import psutil
import os
import math
import sys
from disnake.ext import commands
from utils.config import BotConfig
from utils.translations import DiscordStatuses, DiscordSlowmods, DiscordVerificationLevel


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='bot-stats')
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def _botstats(self, ctx):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label='Перепригласить', url=BotConfig['BotInvite']))
        size_name = ('б', 'кб', 'мб', 'гб', 'тб')

        used = psutil.Process(os.getpid()).memory_info().rss
        i = int(math.floor(math.log(used, 1024)))
        p = math.pow(1024, i)
        s = round(used / p, 2)
        used_bot = '%s%s' % (s, size_name[i])

        emb = discord.Embed(title='Статистика бота:',
            description=f'> **Количество серверов** - {len(self.bot.guilds)}\n'
                        f'> **Количество пользователей** - {len(self.bot.users)}\n'
                        f'> **Количество команд** - {len(self.bot.commands)}\n'
                        f'> **Текущая задержка** - {self.bot.ws.latency * 1000:.0f}мс\n'
                        f'> **Версия бота** - {BotConfig["BotVersion"]}\n'
                        f'> **Версия Disnake** - {discord.version_info[0]}.{discord.version_info[1]}.{discord.version_info[2]}\n'
                        f'> **Версия Python** - {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}\n',
            color=BotConfig['OrangeColor'])

        if ctx.author.id == BotConfig['DeveloperID']:
            emb.description += f'> **Использованно ОЗУ** - {used_bot}'
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


    @commands.command(name='user-info')
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def _userinfo(self, ctx, member: discord.Member=None):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label='Перепригласить', url=BotConfig['BotInvite']))
        user = ctx.author if not member else member

        activities = ''
        for i in user.activities:
            if i.type == discord.ActivityType.custom:
                activities += f'> **Пользовательский статус** - {i.name}\n'

            if i.type == discord.ActivityType.playing:
                activities += f'> **Играет в** - {i.name}\n'

            if i.type == discord.ActivityType.listening:
                activities += f'> **Слушает** - {i.title} ({"; ".join(i.artists)})\n'

        emb = discord.Embed(title='Информация об участнике:',
            description=f'> **Никнейм** - {user.name}\n'
                        f'> **ID** - {user.id}\n'
                        f'> **Создал аккаунт Discord** - <t:{int(user.created_at.timestamp())}:D>\n'
                        f'> **Присоединился к серверу** - <t:{int(user.joined_at.timestamp())}:D>\n'
                        f'> **Наивысшая роль** - {user.top_role.mention}\n'
                        f'> **Статус** - {DiscordStatuses[str(user.status)]}\n'
                        f'{activities}',
            color=BotConfig['OrangeColor'])
        emb.set_thumbnail(url=user.avatar)
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)

    
    @commands.command(name='guild-info')
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def _guildinfo(self, ctx):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label='Перепригласить', url=BotConfig['BotInvite']))
        if ctx.guild.verification_level == discord.VerificationLevel.none: verification_level = ''
        else: verification_level = f'> **Уровень верификации** - {DiscordVerificationLevel[str(ctx.guild.verification_level)]}\n'

        emb = discord.Embed(title='Информация о сервере:',
            description=f'> **Название** - {ctx.guild}\n'
                        f'> **Владелец** - {ctx.guild.owner}\n'
                        f'> **Создан** - <t:{int(ctx.guild.created_at.timestamp())}:D>\n'
                        f'{verification_level}'
                        f'> **Количество каналов** - {len(ctx.guild.channels)}\n'
                        f'> **Количество ролей** - {len(ctx.guild.roles)}\n'
                        f'> **Количество участников** - {ctx.guild.member_count}\n',
            color=BotConfig['OrangeColor'])
        
        if ctx.guild.icon:
            emb.set_thumbnail(url=ctx.guild.icon)

        if ctx.guild.banner:
            emb.set_image(url=ctx.guild.banner)
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


    @commands.command(name='channel-info')
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def _channelinfo(self, ctx, text_channel: discord.TextChannel=None):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label='Перепригласить', url=BotConfig['BotInvite']))
        channel = ctx.channel if not text_channel else text_channel

        if channel.slowmode_delay == 0: slowmode = ''
        else: slowmode = f'> **Задержка** - {DiscordSlowmods[channel.slowmode_delay]}\n'

        if not channel.category: category = ''
        else: category = f'> **Категория** - {channel.category}\n'

        if not channel.topic: topic = ''
        else: topic = f'> **Описание** - {channel.topic}\n'

        emb = discord.Embed(title='Информация о канале:',
            description=f'> **Название** - {channel}\n'
                        f'> **ID** - {channel.id}\n'
                        f'{slowmode}{category}{topic}'
                        f'> **Создан** - <t:{int(channel.created_at.timestamp())}:D>',
            color=BotConfig['OrangeColor'])
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


def setup(bot):
    bot.add_cog(Information(bot))
    print(f'[SYSTEM] Module "information" loaded!')
