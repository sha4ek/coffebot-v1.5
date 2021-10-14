import disnake, asyncio, random
from disnake.ext import commands

from utils.config import BotSettings, MongoSettings
from utils.functions import BotPostfix
from utils.translations import DiscordPermissions


MainPrefix = BotSettings['MainPrefix'] # переменная с основным префиксом
GreenColor = BotSettings['GreenColor'] # переменная с цветом эмбеда
RedColor = BotSettings['RedColor'] # переменная с цветом эмбеда
OrangeColor = BotSettings['OrangeColor'] # переменная с цветом эмбеда
GuildsData = MongoSettings['GuildsData'] # переменная с дата-базой монги


class Events(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.Cog.listener()
    async def on_ready(self):
        developer = self.Bot.get_user(546502974499717122)

        emb = disnake.Embed(
            title='Подключение бота:',
            description=f'> **{self.Bot.user.name} успешно подключен!**',
            color=GreenColor
        )

        await developer.send(embed=emb)
        print(f'[SYSTEM] {self.Bot.user.name} is connected!')

        while True:
            await self.Bot.change_presence(
                activity=disnake.Activity(
                    name=f'{MainPrefix}help | {len(self.Bot.guilds)} {BotPostfix(len(self.Bot.guilds), "сервер", "сервера", "серверов")}',
                    type=disnake.ActivityType.watching
                ),
                status=disnake.Status.idle
            )
            await asyncio.sleep(6)
            await self.Bot.change_presence(
                activity=disnake.Activity(
                    name=f'{MainPrefix}help | {len(self.Bot.users)} {BotPostfix(len(self.Bot.users), "пользователь", "пользователя", "пользователей")}',
                    type=disnake.ActivityType.watching
                ),
                status=disnake.Status.idle
            )
            await asyncio.sleep(6)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = commands.CommandNotFound, commands.CommandOnCooldown

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.MemberNotFound):
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы указали несуществующего участника!**',
                color=RedColor
                )
            await ctx.send(embed=emb)

        elif isinstance(error, commands.MissingPermissions):
            emb = disnake.Embed(
                title='Ошибка:',
                description=f'> **У вас отсутствуют права "{", ".join(DiscordPermissions[permissions] for permissions in error.missing_permissions )}" на использование команды!**',
                color=RedColor)
            await ctx.send(embed=emb)

        elif isinstance(error, commands.BotMissingPermissions):
            permissions = ctx.guild.me.guild_permissions

            if not permissions.send_messages:
                emb = disnake.Embed(
                    title='Ошибка:',
                    description=f'> **У бота отсутствуют права "{", ".join(DiscordPermissions[permissions] for permissions in error.missing_permissions )}" на использование команды!**',
                    color=RedColor
                    )
                await ctx.author.send(embed=emb)

            if not permissions.embed_links:
                await ctx.send(f'**Ошибка:**\n> **У бота отсутствуют права "{", ".join(DiscordPermissions[permissions] for permissions in error.missing_permissions )}" на использование команды!**')
            
            else:
                emb = disnake.Embed(
                    title='Ошибка:',
                    description=f'> **У бота отсутствуют права "{", ".join(DiscordPermissions[permissions] for permissions in error.missing_permissions)}" на использование команды!**',
                    color=RedColor)
                await ctx.send(embed=emb)

        elif isinstance(error, commands.NotOwner):
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не разработчик бота!**',
                color=RedColor
                )
            await ctx.send(embed=emb)

        else:
            channel = self.Bot.get_channel(BotSettings['ErrorsLogChannel'])

            emb = disnake.Embed(
                title='Ошибка:',
                description=f'> **Произошла неизвестная ошибка!**',
                color=RedColor
                )

            emb1 = disnake.Embed(
                title='Неизвестная ошибка:',
                description=f'> **Сервер:** {ctx.guild.name}\n'
                            f'> **Команда:** {ctx.message.content}\n'
                            f'> **Ошибка:** \n```py\n{error}\n```',
                color=RedColor
                )

            await ctx.send(embed=emb)
            await channel.send(embed=emb1)
            raise error


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        GuildsLogChannel = self.Bot.get_channel(BotSettings['GuildsLogChannel'])

        GuildsData.insert_one({
            'GuildID': guild.id,
            'GuildPrefix': MainPrefix
            })

        emb = disnake.Embed(
            title='Бот добавлен на сервер:',
            description=f'> **Название:** {guild.name}\n'
                        f'> **Идентификатор:** {guild.id}\n'
                        f'> **Создатель:** {guild.owner} ({guild.owner_id})\n'
                        f'> **Количество участников:** {guild.member_count}',
            color=GreenColor
            )
        emb.set_thumbnail(url=guild.icon)

        if guild.banner != None:
            emb.set_image(url=guild.banner)

        await GuildsLogChannel.send(embed=emb)


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        GuildsLogChannel = self.Bot.get_channel(BotSettings['GuildsLogChannel'])

        GuildsData.delete_one({
            'GuildID': guild.id,
            'GuildPrefix': MainPrefix
            })

        emb = disnake.Embed(
            title='Бот убран с сервера:',
            description=f'> **Название:** {guild.name}\n'
                        f'> **Идентификатор:** {guild.id}\n'
                        f'> **Создатель:** {guild.owner} ({guild.owner_id})\n'
                        f'> **Количество участников:** {guild.member_count}',
            color=RedColor
            )
        emb.set_thumbnail(url=guild.icon)

        if guild.banner != None:
            emb.set_image(url=guild.banner)
            
        await GuildsLogChannel.send(embed=emb)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.Bot.user:
            if not message.guild:
                PrivateMessagesLogChannel = self.Bot.get_channel(BotSettings['PrivateMessagesLogChannel'])
                
                msg = ''
                iurl = ''
                for i in message.content:
                    if i != None:
                        msg += f'> **Сообщение:** {message.content}\n'
                        break
                    
                for i in message.attachments:
                    if i != []:
                        msg += f'> **Файл:** {message.attachments[0].filename} ({message.attachments[0].url})\n'
                    if i.url != None:
                        iurl = i.url

                emb = disnake.Embed(
                    title='Личные сообщения бота:',
                    description=f'> **Пользователь:** {message.author} ({message.author.id})\n'
                                f'{msg}',
                    color=OrangeColor) 
                emb.set_thumbnail(url=message.author.avatar)
                emb.set_image(url=iurl)

                await PrivateMessagesLogChannel.send(embed=emb)


    @commands.Cog.listener()
    async def on_command(self, ctx):
        CommandsLogChannel = self.Bot.get_channel(BotSettings['CommandsLogChannel'])

        emb = disnake.Embed(
            title='Использование команды:',
            description=f'> **Пользователь:** {ctx.author} ({ctx.author.id})\n'
                        f'> **Команда:** {ctx.message.content}',
            color=OrangeColor)
        emb.set_thumbnail(url=ctx.author.avatar)

        await CommandsLogChannel.send(embed=emb)


def setup(Bot):
    Bot.add_cog(Events(Bot))
    print(f'[MODULES] Module "Events" is loaded!')
