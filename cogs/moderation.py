import discord
from discord.ext import commands
from config import Postfix

class moderation(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.User, *, reason = None):
        if member == ctx.author:
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Ты не можешь кикнуть самого себя**',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        else:
            if reason == None:
                embg = discord.Embed(
                    title='Исключение участника:',
                    description=f'**☁ Участник {member.mention} ({member}) был кикнут с сервера**\n'
                                f'**🛡 Модератор:** {ctx.author.mention}\n',
                    color=ctx.author.color)
                embdm = discord.Embed(
                    title='Исключение участника:',
                    description=f'**☁ Ты был кикнут с сервера {ctx.guild.name}**\n'
                                f'**🛡 Модератор:** {ctx.author.mention} ({ctx.author})\n',
                    color=ctx.author.color)
            else:
                embg = discord.Embed(
                    title='Исключение участника:',
                    description=f'**☁ Участник {member.mention} ({member}) был кикнут с сервера**\n'
                                f'**🛡 Модератор:** {ctx.author.mention}\n'
                                f'**⚠ Причина исключения:** {reason}',
                    color=ctx.author.color)
                embdm = discord.Embed(
                    title='Исключение участника:',
                    description=f'**☁ Ты был кикнут с сервера {ctx.guild.name}**\n'
                                f'**🛡 Модератор:** {ctx.author.mention} ({ctx.author})\n'
                                f'**⚠ Причина исключения:** {reason}',
                    color=ctx.author.color)
            await ctx.send(embed=embg)
            await member.send(embed=embdm)
            await ctx.guild.kick(member)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.User, *, reason = None):
        if member == ctx.author:
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Ты не можешь забанить самого себя**',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        else:
            if reason == None:
                embg = discord.Embed(
                    title='Блокировка участника:',
                    description=f'**☁ Участник {member.mention} ({member}) был забанен на сервере**\n'
                                f'**🛡 Модератор:** {ctx.author.mention}\n',
                    color=ctx.author.color)
                embdm = discord.Embed(
                    title='Блокировка участника:',
                    description=f'**☁ Ты был забанен на сервере {ctx.guild.name}**\n'
                                f'**🛡 Модератор:** {ctx.author.mention} ({ctx.author})\n',
                    color=ctx.author.color)
            else:
                embg = discord.Embed(
                    title='Блокировка участника:',
                    description=f'**☁ Участник {member.mention} ({member}) был забанен на сервере**\n'
                                f'**🛡 Модератор:** {ctx.author.mention}\n'
                                f'**⚠ Причина блокировки:** {reason}',
                    color=ctx.author.color)
                embdm = discord.Embed(
                    title='Блокировка участника:',
                    description=f'**☁ Ты был забанен на сервере {ctx.guild.name}**\n'
                                f'**🛡 Модератор:** {ctx.author.mention} ({ctx.author})\n'
                                f'**⚠ Причина блокировки:** {reason}',
                    color=ctx.author.color)
            await ctx.send(embed=embg)
            await member.send(embed=embdm)
            await ctx.guild.ban(member, reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User):
        if member == ctx.author:
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Ты не забанен на этом сервере**',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(
                title='Разблокировка участника:',
                description=f'**☁ Участник {member} был разбанен на сервере**\n'
                            f'**🛡 Модератор:** {ctx.author.mention}\n',
                color=ctx.author.color)
            await ctx.guild.unban(member)
            await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def embed(self, ctx, *, text):
        text = text.split('|')
        emb = discord.Embed(
            title=text[0],
            description=text[1],
            color=ctx.author.color)
        for a in ctx.message.attachments:
            if a.url != None:
                emb.set_image(url=a.url)
            else:
                pass
        await ctx.message.delete()
        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount):
        emb = discord.Embed(
            title='Очистка чата:',
            description=f'**🧹 Из чата было удалено {amount} {Postfix(int(amount), "сообщение", "сообщения", "сообщений")}**\n'
                        f'**🛡 Модератор:** {ctx.author.mention}',
            color=ctx.author.color)
        await ctx.channel.purge(limit=int(amount)+1)
        await ctx.send(embed=emb)
 
def setup(Bot):
    Bot.add_cog(moderation(Bot))
    print('[Cogs] Moderation\'s load!')