import discord, asyncio, requests
from discord.ext import commands
from threading import Thread
from boticordpy import BoticordClient
from utils.config import BotSettings, BotUptime, BotPostfix # импортируем конфиг бота


class Events(commands.Cog): # создаём класс модуля с ивентами
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_ready(self): # создаём ивент запуска бота
        boticord = BoticordClient(self.Bot, BotSettings['BoticordToken'])
        stats = {'servers': len(self.Bot.guilds), 'shards': self.Bot.shard_count, 'users': len(self.Bot.users)}
        
        print(f'[SYSTEM] {self.Bot.user.name}\'s online!') # выводим событие в консоль
        
        await boticord.Bots.postStats(stats)

        uptime = Thread(target=BotUptime)
        uptime.start()
        
        while True:
            await self.Bot.change_presence(activity=discord.Activity(
                name=f'{BotSettings["Bot"]["MainPrefix"]}help | {len(self.Bot.guilds)} {BotPostfix(len(self.Bot.guilds), "сервер", "сервера", "серверов")}',
                type=discord.ActivityType.watching), status=discord.Status.idle)
            await asyncio.sleep(10)
            await self.Bot.change_presence(activity=discord.Activity(
                name=f'{BotSettings["Bot"]["MainPrefix"]}help | {len(self.Bot.users)} {BotPostfix(len(self.Bot.users), "пользователь", "пользователя", "пользователей")}',
                type=discord.ActivityType.watching), status=discord.Status.idle)
            await asyncio.sleep(10)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = commands.CommandNotFound, commands.CommandOnCooldown

        if isinstance(error, ignored):
            pass

        elif isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title='Ошибка:',
                description=f'**:anger: У вас отсутствуют права "{", ".join(BotSettings["Permissions"][perms] for perms in error.missing_perms)}" на использование команды!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif isinstance(error, commands.BotMissingPermissions):
            permissions = ctx.guild.me.permissions_in(ctx.channel)

            if not permissions.send_messages:
                emb = discord.Embed(title='Ошибка:',
                    description=f'**:anger: У бота отсутствуют права "{", ".join(BotSettings["Permissions"][perms] for perms in error.missing_perms)}" на использование команды!**',
                    color=BotSettings['Bot']['ErrorColor'])
                await ctx.author.send(embed=emb)
            if not permissions.embed_links:
                await ctx.send(f'**Ошибка:\n:anger: У бота отсутствуют права "{", ".join(BotSettings["Permissions"][perms] for perms in error.missing_perms)}" на использование команды!**')
            else:
                emb = discord.Embed(title='Ошибка:',
                    description=f'**:anger: У бота отсутствуют права "{", ".join(BotSettings["Permissions"][perms] for perms in error.missing_perms)}" на использование команды!**',
                    color=BotSettings['Bot']['ErrorColor'])
                await ctx.send(embed=emb)
        
        elif isinstance(error, commands.BadArgument):
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы указали неправильный аргумент!**', color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif isinstance(error, commands.NotOwner):
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы не разработчик бота!**', color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        else:
            channel = self.Bot.get_channel(BotSettings['Bot']['ErrorsLogChannel'])

            emb1 = discord.Embed(title='Ошибка:', description=f'**:anger: Произошла неизвестная ошибка!**',
                    color=BotSettings['Bot']['ErrorColor'])
            emb2 = discord.Embed(title='Ошибка:',
                description=f'**:tent: Сервер:** {ctx.guild.name}\n'
                            f'**:bulb: Команда:** {ctx.message.content}\n'
                            f'**:anger: Ошибка:** ```py\n{error}\n```', color=BotSettings['Bot']['ErrorColor'])

            else:
                await ctx.send(embed=emb1)
                await channel.send(embed=emb2)
                raise error


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        collection = BotSettings['Mongo']['Collection'].custom_prefix
        channel = self.Bot.get_channel(BotSettings['Bot']['GuildsLogChannel'])

        collection.insert_one({
            'guild_name': guild.name,
            'guild_id': guild.id,
            'guild_owner_name': f'{guild.owner.name}#{guild.owner.discriminator}',
            'guild_owner_id': guild.owner.id,
            'guild_prefix': BotSettings['Bot']['MainPrefix']
            })

        emb = discord.Embed(title='Бот добавлен на сервер:',
            description=f'**:pencil: Название:** {guild.name}\n'
                        f'**:id: Идентификатор:** {guild.id}\n'
                        f'**:notebook_with_decorative_cover: Имя создателя:** {guild.owner}\n'
                        f'**:id: Идентификатор создателя:** {guild.id}', color=BotSettings['Bot']['NormalColor'])
        emb.set_thumbnail(url=guild.icon_url)
        await channel.send(embed=emb)


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        collection = BotSettings['Mongo']['Collection'].custom_prefix
        channel = self.Bot.get_channel(BotSettings['Bot']['GuildsLogChannel'])

        collection.delete_one({
            'guild_name': guild.name,
            'guild_id': guild.id,
            'guild_owner_name': f'{guild.owner.name}#{guild.owner.discriminator}',
            'guild_owner_id': guild.owner.id,
            })

        emb = discord.Embed(title='Бот убран с сервера:',
            description=f'**:pencil: Название:** {guild.name}\n'
                        f'**:id: Идентификатор:** {guild.id}\n'
                        f'**:notebook_with_decorative_cover: Имя создателя:** {guild.owner}\n'
                        f'**:id: Идентификатор создателя:** {guild.id}', color=BotSettings['Bot']['ErrorColor'])
        emb.set_thumbnail(url=guild.icon_url)
        await channel.send(embed=emb)


def setup(Bot): # подключаем класс к основному файлу 
    Bot.add_cog(Events(Bot))
    print(f'[MODULES] Events\'s load!') # принтуем
