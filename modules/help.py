import disnake as discord
from disnake.ext import commands
from CoffeePaginator import Paginator
from utils.config import BotConfig
from utils.functions import BotPrefix


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def help(self, ctx):
        prefix = BotPrefix(self.bot, ctx.message)[2]

        emb = discord.Embed(title='Общее:',
            description=f'> **{prefix}avatar [участник]** - аватар учасника\n'
                        f'> **{prefix}invite** - приглашение бота\n'
                        f'> **{prefix}last-updates** - список последних обновлений бота',
            color=BotConfig['OrangeColor'])

        emb1 = discord.Embed(title='Весёлое:',
            description=f'> **{prefix}activity <youtube | chess | poker>** - активности в голосовом канале\n'
                        f'> **{prefix}kiss <участник>** - реакция "поцеловать"\n'
                        f'> **{prefix}hug <участник>** - реакция "обнять"\n'
                        f'> **{prefix}slap <участник>** - реакция "дать пощёчину"\n'
                        f'> **{prefix}pat <участник>** - реакция "погладить"\n',
            color=BotConfig['OrangeColor'])

        emb2 = discord.Embed(title='Информация:',
            description=f'> **{prefix}bot-stats** - статистика бота\n'
                        f'> **{prefix}user-info [участник]** - информация об участнике\n'
                        f'> **{prefix}guild-info** - информация о сервере\n'
                        f'> **{prefix}channel-info [канал]** - информация о канале',
            color=BotConfig['OrangeColor'])

        emb3 = discord.Embed(title='Модерация:',
            description=f'> **{prefix}clear <количество сообщений>** - очистка чата\n'
                        f'> **{prefix}ban <участник> [причина]** - бан участника\n'
                        f'> **{prefix}kick <участник> [причина]** - кик участника\n'
                        f'> **{prefix}unban <участник>** - разбан участника',
            color=BotConfig['OrangeColor'])

        emb4 = discord.Embed(title='Настройки:',
            description=f'> **{prefix}set-prefix <standard | префикс>** - установка префикса для сервера',
            color=BotConfig['OrangeColor'])

        emb5 = discord.Embed(title='Для разработчика:',
            description=f'> **{prefix}modules <load | unload | reload> [модуль]** - управление модулями бота\n'
                        f'> **{prefix}eval <код>** - выполнение кода вне редактора',
            color=BotConfig['OrangeColor'])
        
        embs = [emb, emb1, emb2, emb3, emb4]
        
        if ctx.author.id == BotConfig['DeveloperID']:
            embs.append(emb5)

        message = await ctx.send(embed=emb)
        pages = Paginator(message, embs, ctx.author, True, 60)
        await pages.start()


def setup(bot):
    bot.add_cog(Help(bot))
    print(f'[SYSTEM] Module "help" loaded!')
