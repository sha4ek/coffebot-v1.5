import discord, random
from discord.ext import commands

class general(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None: user = ctx.author
        else: user = member

        emb1 = discord.Embed(
            title=f'Аватарка {user.name}:',
            description=f'**📎 [Ссылка]({user.avatar_url})**',
            color=user.color)
        emb2 = discord.Embed(color=user.color)
        emb2.set_image(url=user.avatar_url)
        await ctx.send(embed=emb1)
        await ctx.send(embed=emb2)

    @commands.command(aliases=['flip-text'])
    async def flip_text(self, ctx, *, text):
        emb = discord.Embed(
            title='Перевёрнутый текст:',
            description=f'**✨ Обычный:** {text}\n'
                        f'**💫 Перевёрнутый:** {text[::-1]}',
            color=ctx.author.color)
        await ctx.send(embed=emb)

    @commands.command()
    async def latency(self, ctx):
        if self.Bot.ws.latency < 250: ping = '**🟢 Нормальный пинг**'
        else: ping = '**🔴 Плохой пинг**'

        emb = discord.Embed(
            title='Текущая задержка бота:',
            description=f'**⏱ {self.Bot.ws.latency * 1000:.0f} мс**\n'
                        f'{ping}',
            color=ctx.author.color)
        await ctx.send(embed=emb)

    @commands.command()
    async def color(self, ctx):
        clr = (random.randint(0,16777215))
        
        emb = discord.Embed(
            title='Сгенерированный цвет:',
            description= f'**🌈 #{hex(clr)[2:]}**',
            color=clr)
        await ctx.send(embed=emb)

    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        channel = self.Bot.get_channel(869152457094209586)

        embg = discord.Embed(
            title='Новая идея:',
            description=f'**🔔 Спасибо за идею, постараемся реализовать**',\
            color=ctx.author.color)

        embb = discord.Embed(
            title='Новая идея:',
            description=f'**😀 Предложил:** {ctx.author}\n'
                        f'**⛺ Сервер:** {ctx.guild.name}\n'
                        f'**🌟 Идея:** {suggestion}',
            color=ctx.author.color)
        embb.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embg)
        await channel.send(embed=embb)

    @commands.command(aliases=['bug-report'])
    async def bug_report(self, ctx, *, bug):
        channel = self.Bot.get_channel(869196062374629386)

        embg = discord.Embed(
            title='Репорт на баг:',
            description=f'**🔔 Спасибо что сообщил о баге, постараемся вскоре исправить**',\
            color=ctx.author.color)

        embb = discord.Embed(
            title='Репорт на баг:',
            description=f'**😀 Сообщил:** {ctx.author}\n'
                        f'**⛺ Сервер:** {ctx.guild.name}\n'
                        f'**🌟 Баг:** {bug}',
            color=ctx.author.color)
        embb.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embg)
        await channel.send(embed=embb)

def setup(Bot):
    Bot.add_cog(general(Bot))
    print('[Cogs] General\'s load!')