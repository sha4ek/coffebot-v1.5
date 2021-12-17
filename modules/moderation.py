import disnake as discord
from disnake.ext import commands
from utils.config import BotConfig
from utils.functions import BotPostfix


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.view = discord.ui.View().add_item(discord.ui.Button(label='Перепригласить', url=BotConfig['BotInvite']))


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, read_message_history=True, manage_messages=True)
    async def clear(self, ctx, amount: int=None):
        if not amount:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не указали количество сообщений!**',
                color=BotConfig['RedColor'])

        elif amount > 100:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете указать больше 100 сообщений!**',
                color=BotConfig['RedColor'])

        else:
            await ctx.channel.purge(limit=amount+1)
            emb = discord.Embed(title='Очистка чата:',
                description=f'> **Из чата удалено {amount} {BotPostfix(amount, "сообщение", "сообщения", "сообщений")}!**',
                color=BotConfig['GreenColor'])
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=self.view)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, *, reason=None):
        if not member:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=BotConfig['RedColor'])

        elif member.id == ctx.author.id:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете указать самого себя!**',
                color=BotConfig['RedColor'])

        elif member.top_role.position >= ctx.author.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете забанить участника, который выше или равен вам по роли!**',
                color=BotConfig['RedColor'])

        elif member.top_role.position >= ctx.guild.me.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете забанить участника, который выше или равен боту по роли!**',
                color=BotConfig['RedColor'])

        elif not reason:
            emb = discord.Embed(title='Бан участника:',
                description=f'> **Участник {member} забанен на сервере!**',
                color=BotConfig['GreenColor'])
            emb2 = discord.Embed(title='Бан участника:',
                description=f'> **Вы забанены на сервере {ctx.guild.name} модератором {ctx.author}!**',
                color=BotConfig['GreenColor'])

            try:
                await member.send(embed=emb2)
            except:
                pass

            await ctx.guild.ban(member)
                
        else:
            emb = discord.Embed(title='Бан участника:',
                description=f'> **Участник {member} забанен на сервере по причине "{reason}"!**',
                color=BotConfig['GreenColor'])
            emb2 = discord.Embed(title='Бан участника:',
                description=f'> **Вы забанены на сервере {ctx.guild.name} модератором {ctx.author} по причине "{reason}"!**',
                color=BotConfig['GreenColor'])

            try:
                await member.send(embed=emb2)
            except:
                pass
            
            await ctx.guild.ban(member, reason=reason)
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=self.view)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):
        if not member:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=BotConfig['RedColor'])

        elif member.id == ctx.author.id:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете указать самого себя!**',
                color=BotConfig['RedColor'])

        elif member.top_role.position >= ctx.author.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете кикнуть участника, который выше или равен вам по роли!**',
                color=BotConfig['RedColor'])

        elif member.top_role.position >= ctx.guild.me.top_role.position:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете кикнуть участника, который выше или равен боту по роли!**',
                color=BotConfig['RedColor'])

        elif not reason:
            emb = discord.Embed(title='Кик участника:',
                description=f'> **Участник {member} кикнут с сервера!**',
                color=BotConfig['GreenColor'])
            emb2 = discord.Embed(title='Кик участника:',
                description=f'> **Вы кикнуты с сервера {ctx.guild.name} модератором {ctx.author}!**',
                color=BotConfig['GreenColor'])

            try:
                await member.send(embed=emb2)
            except:
                pass

            await ctx.guild.kick(member)
                
        else:
            emb = discord.Embed(title='Кик участника:',
                description=f'> **Участник {member} кикнут с сервера по причине "{reason}"!**',
                color=BotConfig['GreenColor'])
            emb2 = discord.Embed(title='Кик участника:',
                description=f'> **Вы кикнуты с сервера {ctx.guild.name} модератором {ctx.author} по причине "{reason}"!**',
                color=BotConfig['GreenColor'])

            try:
                await member.send(embed=emb2)
            except:
                pass
            
            await ctx.guild.kick(member, reason=reason)
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=self.view)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    async def unban(self, ctx, member: discord.User=None):
        if not member:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=BotConfig['RedColor'])

        elif member.id == ctx.author.id:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете указать самого себя!**',
                color=BotConfig['RedColor'])
            
        else:
            try:
                await ctx.guild.unban(member)
                emb = discord.Embed(title='Разбан участника:',
                    description=f'> **Участник {member} разбанен на сервере!**',
                    color=BotConfig['GreenColor'])
            except:
                emb = discord.Embed(title='Ошибка:',
                    description=f'> **Участник не забанен на сервере!**',
                    color=BotConfig['RedColor'])
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=self.view)


def setup(bot):
    bot.add_cog(Moderation(bot))
    print(f'[SYSTEM] Module "moderation" loaded!')
