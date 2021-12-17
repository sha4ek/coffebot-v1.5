import disnake as discord
import asyncio
from disnake.ext import commands
from utils.config import BotConfig, MongoConfig
from utils.functions import BotPostfix
from utils.translations import DiscordPermissions


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[SYSTEM] {self.bot.user.name} connected!')

        while True:
            await self.bot.change_presence(activity=discord.Activity(name=f'{BotConfig["MainPrefix"]}help | {len(self.bot.guilds)} {BotPostfix(len(self.bot.guilds), "сервер", "сервера", "серверов")}',
                    type=discord.ActivityType.watching),
                status=discord.Status.idle)
            await asyncio.sleep(180)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label='Перепригласить', url=BotConfig['BotInvite']))
        
        ignored = commands.CommandNotFound, commands.CommandOnCooldown

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.MemberNotFound):
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы указали несуществующего участника или того, кого нет на сервере!**',
                color=BotConfig['RedColor'])
            emb.set_footer(text=BotConfig['Slashes'])
            await ctx.send(embed=emb, view=view)

        elif isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title='Ошибка:',
                description=f'> **У вас отсутствуют права "{", ".join(DiscordPermissions[permissions] for permissions in error.missing_permissions)}" на использование команды!**',
                color=BotConfig['RedColor'])
            emb.set_footer(text=BotConfig['Slashes'])
            await ctx.send(embed=emb, view=view)

        elif isinstance(error, commands.BotMissingPermissions):
            permissions = ctx.guild.me.guild_permissions

            if not permissions.send_messages:
                emb = discord.Embed(title='Ошибка:',
                    description=f'> **У бота отсутствуют права "{", ".join(DiscordPermissions[permissions] for permissions in error.missing_permissions )}" на использование команды!**',
                    color=BotConfig['RedColor']
                    )
                emb.set_footer(text=BotConfig['Slashes'])
                await ctx.author.send(embed=emb, view=view)

            elif not permissions.embed_links:
                await ctx.send(f'**Ошибка:**\n> **У бота отсутствуют права "{", ".join(DiscordPermissions[permissions] for permissions in error.missing_permissions)}" на использование команды!**\n{BotConfig["Slashes"])}')
            
            else:
                emb = discord.Embed(title='Ошибка:',
                    description=f'> **У бота отсутствуют права "{", ".join(DiscordPermissions[permissions] for permissions in error.missing_permissions)}" на использование команды!**',
                    color=BotConfig['RedColor'])
                emb.set_footer(text=BotConfig['Slashes'])
                await ctx.send(embed=emb, view=view)

        elif isinstance(error, commands.NotOwner):
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не разработчик бота!**',
                color=BotConfig['RedColor'])
            emb.set_footer(text=BotConfig['Slashes'])
            await ctx.send(embed=emb, view=view)

        elif isinstance(error, commands.BadArgument):
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы указали неверный аргумент!**',
                color=BotConfig['RedColor'])
            emb.set_footer(text=BotConfig['Slashes'])
            await ctx.send(embed=emb, view=view)

        else:
            ErrorsLogChannel = self.bot.get_channel(BotConfig['ErrorsLogChannel'])

            emb = discord.Embed(title='Ошибка:',
                description=f'> **Произошла неизвестная ошибка!**',
                color=BotConfig['RedColor'])
            emb.set_footer(text=BotConfig['Slashes'])
            emb1 = discord.Embed(title='Неизвестная ошибка:',
                description=f'> **Сервер** - {ctx.guild.name}\n'
                            f'> **Пользователь** - {ctx.author} ({ctx.author.id})\n'
                            f'> **Команда** - {ctx.message.content}\n'
                            f'> **Ошибка** - \n```py\n{error}\n```',
                color=BotConfig['RedColor'])
            
            if ctx.command.name != 'eval':
                await ctx.send(embed=emb, view=view)
                await ErrorsLogChannel.send(embed=emb1)
                print(f'[ERROR] Error occurred in the "{ctx.command}" command! More:')
                raise error


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        GuildsLogChannel = self.bot.get_channel(BotConfig['GuildsLogChannel'])
        emb = discord.Embed(title='Добавление на сервер:',
                description=f'> **Название** - {guild.name}\n'
                            f'> **Идентификатор** - {guild.id}\n'
                            f'> **Создатель** - {guild.owner} ({guild.owner_id})\n'
                            f'> **Количество участников** - {guild.member_count}',
                color=BotConfig['GreenColor'])
        
        if guild.icon:
            emb.set_thumbnail(url=guild.icon)

        if guild.banner:
            emb.set_image(url=guild.banner)
        
        try:
            MongoConfig['GuildsData'].insert_one({
                'GuildID': guild.id,
            })
                
        except Exception as exception:
            await GuildsLogChannel.send(exception)

        await GuildsLogChannel.send(embed=emb)


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        GuildsLogChannel = self.bot.get_channel(BotConfig['GuildsLogChannel'])
        MongoConfig['GuildsData'].delete_one({
            'GuildID': guild.id,
        })

        emb = discord.Embed(title='Исключение с сервера:',
            description=f'> **Название** - {guild.name}\n'
                        f'> **Идентификатор** - {guild.id}\n'
                        f'> **Создатель** - {guild.owner} ({guild.owner_id})\n'
                        f'> **Количество участников** - {guild.member_count}',
            color=BotConfig['RedColor'])
        
        if guild.icon:
            emb.set_thumbnail(url=guild.icon)

        if guild.banner:
            emb.set_image(url=guild.banner)

        await GuildsLogChannel.send(embed=emb)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != (self.bot.user.id and BotConfig['DeveloperID']) and not message.guild:
                PrivateMessagesLogChannel = self.bot.get_channel(BotConfig['PrivateMessagesLogChannel'])

                msg = ''
                for i in message.content:
                    if i:
                        msg += f'> **Сообщение** - {message.content}\n'
                        break

                iurl = ''
                for i in message.attachments:
                    if i:
                        msg += f'> **Файл** - {message.attachments[0].filename} ({message.attachments[0].url})\n'
                    if i.url:
                        iurl = i.url

                emb = discord.Embed(title='Личные сообщения:',
                    description=f'> **Пользователь** - {message.author} ({message.author.id})\n'
                                f'{msg}',
                    color=BotConfig['OrangeColor']) 
                emb.set_thumbnail(url=message.author.avatar)
                emb.set_image(url=iurl)
                await PrivateMessagesLogChannel.send(embed=emb)


    @commands.Cog.listener()
    async def on_command(self, ctx):
        CommandsLogChannel = self.bot.get_channel(BotConfig['UsingCommandsLogChannel'])

        emb = discord.Embed(title='Использование команды:',
            description=f'> **Сервер** - {ctx.guild}\n'
                        f'> **Пользователь** - {ctx.author} ({ctx.author.id})\n'
                        f'> **Команда** - {ctx.message.content}',
            color=BotConfig['OrangeColor'])
        emb.set_thumbnail(url=ctx.author.avatar)

        if ctx.author.id != BotConfig['DeveloperID']:
            await CommandsLogChannel.send(embed=emb)


def setup(bot):
    bot.add_cog(Events(bot))
    print(f'[SYSTEM] Module "events" loaded!')
