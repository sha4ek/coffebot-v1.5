import discord
from discord.ext import commands
from utils.config import BotSettings, BotPostfix # импортируем конфиг бота


class Moderation(commands.Cog): # создаём класс модуля команды помощи
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, read_message_history=True,
        manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int=None): # создаём команду очистки
        if amount == None:
            emb = discord.Embed(title='Ошибка',
                description=f'**:anger: Вы не указали количество сообщений!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)
        else:
            if amount >= 101:
                emb = discord.Embed(title='Ошибка',
                    description=f'**:anger: Вы не можете указать больше 100 сообщений!**',
                    color=BotSettings['Bot']['ErrorColor'])
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(title='Очистка чата:',
                    description=f'**:broom: Из чата было удалено {amount} {BotPostfix(amount, "сообщение", "сообщения", "сообщений")}**',
                    color=BotSettings['Bot']['NormalColor'])
                await ctx.channel.purge(limit=amount+1)
                await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member = None, role: discord.Role = None):
        if member == None:
            emb = discord.Embed(title='Ошибка:', description='**:anger: Вы не указали участника!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.id == ctx.author.id:
            emb = discord.Embed(title='Ошибка:', description='**:anger: Вы не можете указать самого себя!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif role == None:
            emb = discord.Embed(title='Ошибка:', description='**:anger: Вы не указали роль!**',
            color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.top_role.position >= ctx.guild.me.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы не можете выдать роль участнику, который выше или равен боту по роли!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.top_role.position >= ctx.author.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы не можете выдать роль участнику, который выше или равен вам по роли!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif role.position >= ctx.guild.me.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы не можете выдать роль, которая выше или равна боту!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif role.position >= ctx.author.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы не можете выдать роль, которая выше или равна вам!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)
            
        else:
            await member.add_roles(role)
            emb = discord.Embed(title='Добавление роли:',
                description=f'**{ctx.author.name} выдал {member.name} роль "{role.name}"**',
                color=BotSettings['Bot']['NormalColor'])
            await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, *, reason=None):
        if member == None:
            emb = discord.Embed(title='Ошибка:', description=f'**:anger: Вы не указали участника!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.id == ctx.author.id:
            emb = discord.Embed(title='Ошибка:', description='**:anger: Вы не можете указать самого себя!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.top_role.position >= ctx.author.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы не можете забанить участника, который выше или равен вам по роли!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.top_role.position >= ctx.guild.me.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы не можете забанить участника, который выше или равен боту по роли!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        else:
            if reason == None:
                embg = discord.Embed(title='Бан участника:', description=f'**:hammer: Участник {member} забанен на сервере**',
                    color=BotSettings['Bot']['NormalColor'])
                embdm = discord.Embed(title='Бан участника:',
                    description=f'**:hammer: Вы забанены на сервере {ctx.guild.name} модератором {ctx.author}**',
                    color=BotSettings['Bot']['NormalColor'])
                await ctx.send(embed=embg)
                await ctx.send(embed=embdm)
                await ctx.guild.ban(member)
                
            else:
                embg = discord.Embed(title='Бан участника:',
                    description=f'**:hammer: Участник {member} забанен на сервере по причине "{reason}"**',
                    color=BotSettings['Bot']['NormalColor'])
                embdm = discord.Embed(title='Бан участника:',
                    description=f'**:hammer: Вы забанены на сервере {ctx.guild.name} модератором {ctx.author} по причине "{reason}"**',
                    color=BotSettings['Bot']['NormalColor'])
                await ctx.send(embed=embg)
                await ctx.send(embed=embdm)
                await ctx.guild.ban(member, reason=reason)


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member=None):
        role = discord.utils.get(ctx.guild.roles, name='Muted')

        if member == None:
            emb = discord.Embed(title='Ошибка:', description=f'**:anger: Вы не указали участника!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.id == ctx.author.id:
            emb = discord.Embed(title='Ошибка:', description='**:anger: Вы не можете указать самого себя!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.top_role.position >= ctx.author.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы не можете замьютить участника, который выше или равен вам по роли!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.top_role.position >= ctx.guild.me.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы не можете замьютить участника, который выше или равен боту по роли!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif role in member.roles:
            emb = discord.Embed(title='Ошибка:',
                description=f'**:anger: Участник {member} уже замьючен на сервере!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif role == None:
            emb = discord.Embed(title='Роль мьюта:', description=f'**:mute: Роль мьюта создана, используйте команду снова**',
                    color=BotSettings['Bot']['NormalColor'])
            await ctx.guild.create_role(name='Muted', color=0x696969, reason='Роль мута')
            await ctx.send(embed=emb)

        else:
            embg = discord.Embed(title='Мьют участника:', description=f'**:mute: Участник {member} замьючен на сервере**',
                    color=BotSettings['Bot']['NormalColor'])
            embdm = discord.Embed(title='Мьют участника:',
                description=f'**:mute: Вы замьючены на сервере {ctx.guild.name} модератором {ctx.author}**',
                color=BotSettings['Bot']['NormalColor'])
            await ctx.send(embed=embg)
            await member.send(embed=embdm)
            await member.add_roles(role, reason='Мьют')


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member=None):
        role = discord.utils.get(ctx.guild.roles, name='Muted')

        if member == None:
            emb = discord.Embed(title='Ошибка:', description=f'**:anger: Вы не указали участника!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.id == ctx.author.id:
            emb = discord.Embed(title='Ошибка:', description='**:anger: Вы не можете указать самого себя!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.top_role.position >= ctx.author.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы не можете размьютить участника, который выше или равен вам по роли!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif member.top_role.position >= ctx.guild.me.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы не можете размьютить участника, который выше или равен боту по роли!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        elif not role in member.roles:
            emb = discord.Embed(title='Ошибка:',
                description=f'**:anger: Участник {member} ещё не замьючен на сервере!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        else:
            embg = discord.Embed(title='Размьют участника:', description=f'**:sound: Участник {member} размьючен на сервере**',
                    color=BotSettings['Bot']['NormalColor'])
            embdm = discord.Embed(title='Размьют участника:',
                description=f'**:sound: Вы размьючены на сервере {ctx.guild.name} модератором {ctx.author}**',
                color=BotSettings['Bot']['NormalColor'])
            await ctx.send(embed=embg)
            await member.send(embed=embdm)
            await member.remove_roles(role, reason='Размьют')


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    @commands.has_permissions(manage_guild=True) 
    async def prefix(self, ctx, prefix = None):
        collection = BotSettings['Mongo']['Collection'].custom_prefix            
        if prefix != None: # проверка введён ли префикс
            if len(str(prefix)) < 3: # проверка длины префикса(нельзя больше 2 символов)
                collection.update_one({
                    'guild_name': ctx.guild.name,
                    'guild_id': ctx.guild.id,
                    'guild_owner_name': f'{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}',
                    'guild_owner_id': ctx.guild.owner.id
                    },
                    {'$set':{'guild_prefix': prefix}})

                emb = discord.Embed(title=f'Смена префикса:',
                    description=f'**:flashlight: Вы успешно сменили префикс на:** {prefix}',
                    color=BotSettings['Bot']['NormalColor'])
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(title='Ошибка:',
                    description=f'**:anger: Префикс не может быть больше 2 символов!**',
                    color=BotSettings['Bot']['ErrorColor'])
                await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title='Ошибка:',
                    description=f'**:anger: Вы не указали префикс!**',
                    color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)


def setup(Bot):  # подключаем класс к основному файлу 
    Bot.add_cog(Moderation(Bot))
    print(f'[MODULES] Moderation\'s load!') # принтуем
