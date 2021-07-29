import discord, time
from discord.ext import commands
from Cybernator import Paginator
from config import Prefix


class help(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command(
        aliases=['хелп', 'помощь'],
        brief='Список всех команд',
        usage=f'{Prefix}help')
    async def help(self, ctx):
        emb1 = discord.Embed(
            title='Помощь по команде:',
            description='**🔆 [аргумент]:** Обязательный аргумент\n'
                        '**🔆 (аргумент):** Необязательный аргумент\n'
                        '**🔆 Нажимай на реакции для перехода по страницам**\n',
            color=ctx.author.color)
        emb2 = discord.Embed(
            title='Общие команды:',
            description=f'**🔆 {Prefix}avatar (участник):** Вывести аватарку пользователя в чат с возможностью скачивания\n'
                        f'**🔆 {Prefix}flip-text [текст]:** Перевернуть ваш текст\n'
                        f'**🔆 {Prefix}color:** Сгенерировать цвет в виде HEX\n'
                        f'**🔆 {Prefix}suggest [идея]:** Отправить идею для бота разработчикам\n'
                        f'**🔆 {Prefix}bug-report [баг]:** Отправить баг бота разработчикам',
            color=ctx.author.color)
        emb3 = discord.Embed(
            title='Фановые команды:',
            description=f'**🔆 {Prefix}rps:** Игра "Камень, ножницы, бумага"\n'
                        f'**🔆 {Prefix}kiss [участник]:** Реакция "Поцеловать"\n'
                        f'**🔆 {Prefix}hug [участник]:** Реакция "Обнять"\n'
                        f'**🔆 {Prefix}slap [участник]:** Реакция "Пощёчина"\n'
                        f'**🔆 {Prefix}pat [участник]:** Реакция "Погладить"\n',
            color=ctx.author.color)
        emb4 = discord.Embed(
            title='Информационные команды',
            description=f'**🔆 {Prefix}botinfo:** Показать немного информации о боте\n'
                        f'**🔆 {Prefix}userinfo (участник):** Показать немного информации об участнике\n'
                        f'**🔆 {Prefix}serverinfo:** Показать немного информации о сервере',
            color=ctx.author.color)
        emb5 = discord.Embed(
            title='Команды модерации',
            description=f'**🔆 {Prefix}kick [участник] (причина):** Исключить участника\n'
                        f'**🔆 {Prefix}ban [участник] (причина):** Заблокировать участника\n'
                        f'**🔆 {Prefix}unban [участник]:** Разблокировать участника\n'
                        f'**🔆 {Prefix}embed [титул|описание]:** Написать сообщение в Embed\n'
                        f'**🔆 {Prefix}clear [количество]:** Удалить из чата определённое количество сообщений',
            color=ctx.author.color)
        emb6 = discord.Embed(
            title='Команды создателя',
            description=f'**🔆 {Prefix}module [функция] (модуль):** Управление модулями бота',
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
    print(f'[{time.strftime("%H:%M")}] Cogs: Help\'s load!')
