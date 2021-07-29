import discord, time
from discord.ext import commands
from config import Prefix, Postfix


class events(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.Cog.listener()
    async def on_ready(self):
        await self.Bot.change_presence(
            activity=discord.Activity(
                name=f'{Prefix}help | {len(self.Bot.guilds)} {Postfix(len(self.Bot.guilds), "сервер", "сервера", "серверов")}',
                type=discord.ActivityType.watching),
            status=discord.Status.idle)
        print(f'[{time.strftime("%H:%M")}] System: {self.Bot.user.name}\'s online!')


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.Bot.user:
            if not message.guild:
                channel = self.Bot.get_channel(869191233640226816)

                msg=""
                aurl=""
                for i in message.content:
                    if i != None:
                        msg+=f'**📄 Сообщение:** {message.content}\n'
                        break # брейкаем, чтобы отправилось 1 сообщение
                for i in message.attachments:
                    if i != []:
                        msg+=f'**📌 Файл:** {message.attachments[0].filename} ({message.attachments[0].url})'
                    if i.url != None:
                        aurl=i.url

                emb = discord.Embed(
                    title='ЛС бота:',
                    description=f'**📨 Отправитель:** {message.author} ({message.author.id})\n'
                                f'{msg}',
                    color=0xff9900) 
                emb.set_thumbnail(url=message.author.avatar_url)
                emb.set_image(url=aurl)
                await channel.send(embed=emb)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Данная команда не найдена**\n'
                            f'**💯 Для ознакомления со списком команд напиши:** {Prefix}help',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        elif isinstance(error, commands.BotMissingPermissions):
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 У бота недостаточно прав для исполнения команды**\n'
                            f'**💯 Отсутствует:** {"".join(error.missing_perms)}',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        elif isinstance(error, commands.MissingRequiredArgument):
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Команда введена неправильно**\n'
                            f'**💯 Пример использования:** {ctx.command.usage}',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        elif isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 У тебя недостаточно прав для использования команды**\n'
                            f'**💯 Отсутствует:** {"".join(error.missing_perms)}',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        else:
            channel = self.Bot.get_channel(869450110029922364)

            embg = discord.Embed(
                title='Неизвестная ошибка:',
                description=f'**💢 {error}**\n'
                            '**💯 Ошибка отправлена разработчикам, постараются исправить**',
                color=ctx.author.color)

            embb = discord.Embed(
                title='Неизвестная ошибка:',
                description=f'**💢 Команда:** {ctx.command}\n'
                            f'**⛺ Сервер:** {ctx.guild.name}\n'
                            f'**❗ Ошибка:** {error}\n'
                            f'**📃 [Перейти в консоль](https://dashboard.heroku.com/apps/coffeehost/logs)**',
                color=ctx.author.color)
            await ctx.send(embed=embg)
            await channel.send(embed=embb)
            print(f'[{time.strftime("%H:%M")}] Error: {ctx.command.name} error:')
            raise error


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 869390569250619393:
            if str(payload.emoji) == '<:GreenTick:869395280989143052>':
                role = self.Bot.get_guild(payload.guild_id).get_role(869390228798963752)
                member = self.Bot.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.add_roles(role)
        if payload.message_id == 869387019355320390:
            if str(payload.emoji) == '<:GreenTick:869395280989143052>':
                role = self.Bot.get_guild(payload.guild_id).get_role(869365112853630997)
                member = self.Bot.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.add_roles(role)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 869390569250619393:
            if str(payload.emoji) == '<:GreenTick:869395280989143052>':
                role = self.Bot.get_guild(payload.guild_id).get_role(869390228798963752)
                member = self.Bot.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)
        if payload.message_id == 869387019355320390:
            if str(payload.emoji) == '<:GreenTick:869395280989143052>':
                role = self.Bot.get_guild(payload.guild_id).get_role(869365112853630997)
                member = self.Bot.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)


def setup(Bot):
    Bot.add_cog(events(Bot))
    print(f'[{time.strftime("%H:%M")}] Cogs: Events\'s load!')
