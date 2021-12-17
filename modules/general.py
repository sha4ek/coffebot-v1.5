import disnake as discord
from disnake.ext import commands
from utils.config import BotConfig

view = discord.ui.View()
view.add_item(discord.ui.Button(label='Перепригласить', url=BotConfig['BotInvite']))


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def avatar(self, ctx, member: discord.Member=None):
        user = ctx.author if not member else member

        emb = discord.Embed(title=f'Аватар {user.name}:',
            color=BotConfig['OrangeColor'])
        emb.set_image(url=user.avatar)
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def invite(self, ctx):
        emb = discord.Embed(title='Приглашение бота:',
            description=f'> **[Пригласить]({BotConfig["BotInvite"]})**',
            color=BotConfig['OrangeColor'])
        await ctx.send(embed=emb)

    
    @commands.command(name='last-updates')
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def _lastupdates(self, ctx):
        emb = discord.Embed(title='Последние обновления:',
            description=f"""> **__CoffeeBot v1.5 (<t:1636180792:D>):__**
                        **-** улучшено взаимодействие с базой данных и обработчик ошибок
                        **-** изменены названия команд `prefix`; `stats`; `user`; `server`; `channel`; `links` на `set-prefix`; `bot-stats`; `user-info`; `guild-info`; `channel-info`; `invite`
                        **-** в команде `set-prefix` добавлен аргумент `standard` и помощь по команде при отсутствии аргументов
                        **-** удалена команда `addrole`
                        **-** добавлена проверка на личку пользователя в команде `ban` и `kick`
                        **-** исправлен баг, что при использовании команды `kick` пользователь не исключался, а блокировался на сервере
                        **-** добавлена команда `last-updates` для просмотра последних обновлений бота
                        **-** префикс снова поменялся на `c.`
                        **-** остальные мелкие доработки\n\n"""
                        f"""> **__CoffeeBot v1.4 (<t:1633829230:D>):__**
                        **-** бот переписан под библиотеку `disnake`
                        **-** основным префиксом бота стал `cb.`, а также можно использовать упоминание
                        **-** изменено оформление команд
                        **-** кулдаун использования команд снижен до 2 секунд
                        **-** улучшен обработчик ошибок
                        **-** в команде `help` реакции заменены на кнопки
                        **-** добавлены команды `kiss`, `hug`, `slap`, `pat`, `avatar`, `links`, `server`, `kick`, `unban`
                        **-** удалены команды `lyrics`, `cat`, `mute`, `unmute`\n\n"""
                        f"""> **__CoffeeBot v1.3.2 (<t:1631932750:D>):__**
                        **-** исправлен баг со сменой префикса и теперь он может быть не более 3 символов\n\n"""
                        f"""> **__CoffeeBot v1.3.1 (<t:1631077570:D>):__**
                        **-** доработана команда `help`\n\n"""
                        f"""> **__CoffeeBot v1.3 (<t:1630827550:D>):__**
                        **-** исправлен баг в команде `lyrics` и она перемещена в отдельную категорию `Music`
                        **-** добавлена команда `prefix`\n\n"""
                        f"""> **__CoffeeBot v1.2 (<t:1630447210:D>):__**
                        **-** в команду `stats` добавлен пинг бота
                        **-** добавлены команды `user`, `clear`, `addrole`, `ban`, `mute`, `unmute`, `cat`, `channel`, `lyrics`
                        **-** добавлена нечувствительность к регистру, обработчик ошибок и задержка в 4 секунды\n\n"""
                        f"""> **__CoffeeBot v1.1 (<t:1629787390:D>):__**
                        **-** улучшена команда `help`
                        **-** исправлены ошибки\n\n"""
                        f"""> **__CoffeeBot v1 (<t:1629637330:D>):__**
                        **-** добавлены команды `help`, `stats`, `yt`, `poker`, `chess`""",
            color=BotConfig['OrangeColor'])
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)
        

def setup(bot):
    bot.add_cog(General(bot))
    print(f'[SYSTEM] Module "general" loaded!')
