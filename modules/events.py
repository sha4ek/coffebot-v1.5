import discord, asyncio, requests
from discord.ext import commands
from threading import Thread
#from boticordpy import BoticordClient
from utils.config import BotSettings, BotUptime, BotPostfix # импортируем конфиг бота


class Events(commands.Cog): # создаём класс модуля с ивентами
    def __init__(self, Bot):
        self.Bot = Bot
        
    
    #Boticord = BoticordClient(self.Bot, BotSettings['BoticordToken'])


    @commands.Cog.listener()
    async def on_ready(self): # создаём ивент запуска бота
        response = requests.post('https://boticord.top/api/stats')
        response.headers = {Authorization: BotSettings['BoticordToken']}
        response.body = {
            servers: len(self.Bot.guilds),
            shards: self.Bot.shard_count,
            users: len(self.Bot.users)
        }
        
        #stats = {'servers': len(self.Bot.guilds), 'shards': self.Bot.shard_count, 'users': len(self.Bot.users)}
        
        print(f'[SYSTEM] {self.Bot.user.name}\'s online!') # выводим событие в консоль
        
        #await Boticord.Bots.postStats(stats)

        uptime = Thread(target=BotUptime)
        uptime.start()

        while True:
            await self.Bot.change_presence(activity=discord.Activity(
                name=f'{BotSettings["Bot"]["Prefix"][0]}help | {len(self.Bot.guilds)} {BotPostfix(len(self.Bot.guilds), "сервер", "сервера", "серверов")}',
                type=discord.ActivityType.watching), status=discord.Status.idle)
            await asyncio.sleep(10)
            await self.Bot.change_presence(activity=discord.Activity(
                name=f'{BotSettings["Bot"]["Prefix"][0]}help | {len(self.Bot.users)} {BotPostfix(len(self.Bot.users), "пользователь", "пользователя", "пользователей")}',
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
            channel = self.Bot.get_channel(880968020980273173)
            emb1 = discord.Embed(title='Ошибка:', description=f'**:anger: Произошла неизвестная ошибка!**',
                color=BotSettings['Bot']['ErrorColor'])
            emb2 = discord.Embed(title='Ошибка:',
                description=f'**:tent: Сервер:** {ctx.guild.name}\n'
                            f'**:bulb: Команда:** {ctx.message.content}\n'
                            f'**:anger: Ошибка:** ```py\n{error}\n```', color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb1)
            await channel.send(embed=emb2)
            raise error


def setup(Bot): # подключаем класс к основному файлу 
    Bot.add_cog(Events(Bot))
    print(f'[MODULES] Events\'s load!') # принтуем
