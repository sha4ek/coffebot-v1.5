import discord
from discord.ext import commands
from Cybernator import Paginator
from config import Prefix

class help(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command()
    async def help(self, ctx):
        emb1 = discord.Embed(
            title='Помощь по команде:',
            description='**🔆 [аргумент]:** Обязательный аргумент\n'
                        '**🔆 (аргумент):** Необязательный аргумент\n',
            color=ctx.author.color)
        emb2 = discord.Embed(
            title='Общие команды:',
            description=f'**🔆 {Prefix}avatar (участник):** Показывает аватарку участника, с возможностью её скачивания\n'
                        f'**🔆 {Prefix}flip-text [текст]:** Переворачивает вами написанный текст\n'
                        f'**🔆 {Prefix}latency:** Показывает задержку бота\n'
                        f'**🔆 {Prefix}color:** Генерирует случайный цвет в виде HEX\n'
                        f'**🔆 {Prefix}suggest [идея]:** Отправляет вашу идею для бота создателю\n'
                        f'**🔆 {Prefix}bug-report [баг]:** Отправляет ваш баг бота создателю',
            color=ctx.author.color)
        emb3 = discord.Embed(
            title='Фановые команды:',
            description=f'**🔆 {Prefix}rps:** Игра "Камень, ножницы, бумага"\n'
                        f'**🔆 {Prefix}kiss [участник]:** Реакция "Поцеловать"\n'
                        f'**🔆 {Prefix}hug [участник]:** Реакция "Обнять"\n'
                        f'**🔆 {Prefix}slap [участник]:** Реакция "Дать пощёчину"\n'
                        f'**🔆 {Prefix}pat [участник]:** Реакция "Погладить"\n'
                        f'**🔆 {Prefix}8ball [вопрос]:** Магический шар',
            color=ctx.author.color)
        emb4 = discord.Embed(
            title='Информационные команды',
            description=f'**🔆 {Prefix}servers:** Показывает количество серверов, где стоит бот\n'
                        f'**🔆 {Prefix}userinfo (участник):** Показывает немного информации об участнике\n'
                        f'**🔆 {Prefix}serverinfo:** Показывает немного информации о сервере',
            color=ctx.author.color)
        emb5 = discord.Embed(
            title='Команды модерации',
            description=f'**🔆 {Prefix}kick [участник]:** Исключает участника с сервера\n'
                        f'**🔆 {Prefix}ban [участник]:** Блокирует участника на сервере\n'
                        f'**🔆 {Prefix}unban [участник]:** Разблокирует участника на сервере\n'
                        f'**🔆 {Prefix}embed [титул|описание]:** Пишет ваш текст в Embed-сообщении от лица бота\n'
                        f'**🔆 {Prefix}clear [количество]:** Удаляет указанное количество сообщений в чате',
            color=ctx.author.color)
        emb6 = discord.Embed(
            title='Команды создателя',
            description=f'**🔆 {Prefix}load [модуль]:** Включает модуль бота\n'
                        f'**🔆 {Prefix}unload [модуль]:** Выключает модуль бота\n'
                        f'**🔆 {Prefix}reload [модуль]:** Перезагружает модуль бота',
            color=ctx.author.color)
        if ctx.author.id != 546502974499717122:
            embeds = [emb1, emb2, emb3, emb4, emb5]
        else:
            embeds = [emb1, emb2, emb3, emb4, emb5, emb6]
        message = await ctx.send(embed=emb1)
        page = Paginator(self.Bot, message, embeds=embeds, timeout=60, only=ctx.author, footer=None, reactions=['⬅', '➡'], use_remove_reaction=False)
        await page.start()

def setup(Bot):
    Bot.add_cog(help(Bot))
    print('[Cogs] Help\'s load!')