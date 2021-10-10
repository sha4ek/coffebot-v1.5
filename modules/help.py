import disnake
from disnake.ext import commands
from CoffeePaginator import Paginator

from utils.config import BotSettings


OrangeColor = BotSettings['OrangeColor'] # переменная с цветом эмбеда


class Help(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def help(self, ctx):
        emb = disnake.Embed(
            title='Общее:',
            description=f'> **{ctx.prefix}avatar [участник]** - аватарка учасника\n'
                        f'> **{ctx.prefix}links** - полезные ссылки',
            color=OrangeColor
        )

        emb1 = disnake.Embed(
            title='Весёлое:',
            description=f'> **{ctx.prefix}activity [функция]** - активности в голосовом канале\n'
                        f'> **{ctx.prefix}kiss <участник>** - реакция "Поцеловать"\n'
                        f'> **{ctx.prefix}hug <участник>** - реакция "Обнять"\n'
                        f'> **{ctx.prefix}slap <участник>** - реакция "Пощёчина"\n'
                        f'> **{ctx.prefix}pat <участник>** - реакция "Погладить"\n',
            color=OrangeColor
        )

        emb2 = disnake.Embed(
            title='Информация:',
            description=f'> **{ctx.prefix}stats** - немного статистики бота\n'
                        f'> **{ctx.prefix}user [участник]** - информация об участнике\n'
                        f'> **{ctx.prefix}server** - информация о сервере\n'
                        f'> **{ctx.prefix}channel [канал]** - информация о канале',
            color=OrangeColor
        )

        emb3 = disnake.Embed(
            title='Модерация:',
            description=f'> **{ctx.prefix}clear <количество сообщений>** - очистка чата\n'
                        f'> **{ctx.prefix}addrole <участник> <роль>** - добавление роли участнику\n'
                        f'> **{ctx.prefix}ban <участник> [причина]** - бан участника\n'
                        f'> **{ctx.prefix}kick <участник> [причина]** - кик участника\n'
                        f'> **{ctx.prefix}unban <участник>** - разбан участника',
            color=OrangeColor
        )

        emb4 = disnake.Embed(
            title='Настройки:',
            description=f'> **{ctx.prefix}prefix <префикс>** - установка префикса для сервера',
            color=OrangeColor
        )

        emb5 = disnake.Embed(
            title='Для разработчика:',
            description=f'> **{ctx.prefix}modules [функция] [модуль]** - управление модулями бота',
            color=OrangeColor
        )
        
        embs = [emb, emb1, emb2, emb3, emb4]
        message = await ctx.send(embed=emb)
        
        if ctx.author.id != self.Bot.owner_id:
            embs = embs
        else:
            embs.append(emb5)
        
        pages = Paginator(message, embs, ctx.author, True, 60)
        await pages.start()


def setup(Bot):
    Bot.add_cog(Help(Bot))
    print(f'[MODULES] Module "Help" is loaded!')
