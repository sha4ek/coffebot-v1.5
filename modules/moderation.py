import disnake
from disnake.ext import commands

from utils.config import BotSettings
from utils.functions import BotPostfix


GreenColor = BotSettings['GreenColor'] # переменная с цветом эмбеда
RedColor = BotSettings['RedColor'] # переменная с цветом эмбеда


class Moderation(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, read_message_history=True, manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = None):
        if amount == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description=f'> **Вы не указали количество сообщений!**',
                color=RedColor
            )

        else:
            if amount >= 101:
                emb = disnake.Embed(
                    title='Ошибка:',
                    description=f'> **Вы не можете указать больше 100 сообщений!**',
                    color=RedColor
                )

            else:
                emb = disnake.Embed(
                    title='Очистка чата:',
                    description=f'> **Из чата было удалено {amount} {BotPostfix(amount, "сообщение", "сообщения", "сообщений")}**',
                    color=GreenColor
                )
                await ctx.channel.purge(limit=amount+1)
        
        await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: disnake.Member=None, role: disnake.Role=None):
        if member == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=RedColor
            )

        elif member.id == ctx.author.id:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете указать самого себя!**',
                color=RedColor
            )

        elif role == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не указали роль!**',
                color=RedColor
            )

        elif member.top_role.position >= ctx.guild.me.top_role.position:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете выдать роль участнику, который выше или равен боту по роли!**',
                color=RedColor
            )

        elif member.top_role.position >= ctx.author.top_role.position:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете выдать роль участнику, который выше или равен вам по роли!**',
                color=RedColor
            )

        elif role.position >= ctx.guild.me.top_role.position:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете выдать роль, которая выше или равна боту!**',
                color=RedColor
            )

        elif role.position >= ctx.author.top_role.position:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете выдать роль, которая выше или равна вам!**',
                color=RedColor
            )
            
        else:
            emb = disnake.Embed(
                title='Добавление роли:',
                description=f'> **Роль "{role.name}" выдана {member.mention}**',
                color=GreenColor
            )

            await member.add_roles(role)
        
        await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: disnake.Member=None, *, reason=None):
        if member == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=RedColor
            )

        elif member.id == ctx.author.id:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете указать самого себя!**',
                color=RedColor
            )

        elif member.top_role.position >= ctx.author.top_role.position:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете забанить участника, который выше или равен вам по роли!**',
                color=RedColor
            )

        elif member.top_role.position >= ctx.guild.me.top_role.position:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете забанить участника, который выше или равен боту по роли!**',
                color=RedColor
            )

        else:
            if reason == None:
                emb = disnake.Embed(
                    title='Бан участника:',
                    description=f'> **Участник {member} забанен на сервере**',
                    color=GreenColor
                )

                embdm = disnake.Embed(
                    title='Бан участника:',
                    description=f'> **Вы забанены на сервере {ctx.guild.name} модератором {ctx.author}**',
                    color=GreenColor
                )

                await member.send(embed=embdm)
                await ctx.guild.ban(member)
                
            else:
                emb = disnake.Embed(
                    title='Бан участника:',
                    description=f'> **Участник {member} забанен на сервере по причине "{reason}"**',
                    color=GreenColor
                )

                embdm = disnake.Embed(
                    title='Бан участника:',
                    description=f'> **Вы забанены на сервере {ctx.guild.name} модератором {ctx.author} по причине "{reason}"**',
                    color=GreenColor
                )

                await member.send(embed=embdm)
                await ctx.guild.ban(member, reason=reason)

        await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: disnake.Member=None, *, reason=None):
        if member == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=RedColor
            )

        elif member.id == ctx.author.id:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете указать самого себя!**',
                color=RedColor
            )

        elif member.top_role.position >= ctx.author.top_role.position:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете кикнуть участника, который выше или равен вам по роли!**',
                color=RedColor
            )

        elif member.top_role.position >= ctx.guild.me.top_role.position:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете кикнуть участника, который выше или равен боту по роли!**',
                color=RedColor
            )

        else:
            if reason == None:
                emb = disnake.Embed(
                    title='Кик участника:',
                    description=f'> **Участник {member} кикнут с сервера**',
                    color=GreenColor
                )

                embdm = disnake.Embed(
                    title='Кик участника:',
                    description=f'> **Вы кикнуты с сервера {ctx.guild.name} модератором {ctx.author}**',
                    color=GreenColor
                )

                await member.send(embed=embdm)
                await ctx.guild.ban(member)
                
            else:
                emb = disnake.Embed(
                    title='Кик участника:',
                    description=f'> **Участник {member} кикнут с сервера по причине "{reason}"**',
                    color=GreenColor
                )

                embdm = disnake.Embed(
                    title='Кик участника:',
                    description=f'> **Вы кикнуты с сервера {ctx.guild.name} модератором {ctx.author} по причине "{reason}"**',
                    color=GreenColor
                )
                
                await member.send(embed=embdm)
                await ctx.guild.ban(member, reason=reason)

        await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: disnake.User = None):
        if member == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=RedColor
            )

        elif member.id == ctx.author.id:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете указать сами себя!**',
                color=RedColor
            )
            
        else:
            emb = disnake.Embed(
                title='Разбан участника:',
                description=f'> **Участник {member} был разбанен на сервере модератором {ctx.author.mention}**',
                color=GreenColor
            )
            await ctx.guild.unban(member)
        
        await ctx.send(embed=emb)


def setup(Bot):
    Bot.add_cog(Moderation(Bot))
    print(f'[MODULES] Module "Moderation" is loaded!')
