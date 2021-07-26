import discord, random, nekos, asyncio
from discord.ext import commands

class fun(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command()
    async def rps(self, ctx):
        solutions = ['🧱', '✂️', '📄']
        winner = 'Ничья**'

        emb = discord.Embed(
            title='Камень, ножницы, бумага:',
            description='**⚠ У тебя 10 секунд**\n'
                        '**⭐ Выбери свой ход:**',
            color=ctx.author.color)
        msg = await ctx.send(embed=emb)
        for r in solutions:
            await msg.add_reaction(r)
        try:
            react, user = await self.Bot.wait_for('reaction_add', timeout=10.0, check=lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in solutions)
        except asyncio.TimeoutError:
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Время выбора хода истекло**',
                color=ctx.author.color)
            await msg.edit(embed=emb)
            for r in solutions:
                await msg.clear_reaction(r)
        else:
            p1 = solutions.index(react.emoji)
            p2 = random.randint(0, 2)

            if p1 == 0 and p2 == 1 or p1 == 1 and p2 == 2 or p1 == 2 and p2 == 0:
                winner = f'Победил:** {ctx.author.mention}'
            elif p1 == 0 and p2 == 2 or p1 == 1 and p2 == 0 or p1 == 2 and p2 == 1:
                winner = f'Победил:** {self.Bot.user.mention}'

            emb = discord.Embed(
                title='Камень, ножницы, бумага:',
                description=f'**😀 {ctx.author.name}:** {solutions[p1]}\n'
                            f'**🤖 {self.Bot.user.name}:** {solutions[p2]}\n'
                            f'**🏆 {winner}',
                color=ctx.author.color)
            await msg.edit(embed=emb)
            for r in solutions:
                await msg.clear_reaction(r)

    @commands.command()
    async def kiss(self, ctx, member: discord.Member):
        if member == ctx.message.author:
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Ты не можешь поцеловать самого себя**',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(
                title='Реакция "Поцелуй":',
                description=f'**💋 {ctx.message.author.mention} поцеловал {member.mention}**',
                color=ctx.author.color)
            emb.set_image(url=nekos.img('kiss'))
            await ctx.send(embed=emb)

    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        if member == ctx.message.author:
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Ты не можешь обнять самого себя**',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(
                title='Реакция "Обнимашки":',
                description=f'**🫂 {ctx.message.author.mention} обнял {member.mention}**',
                color=ctx.author.color)
            emb.set_image(url=nekos.img('hug'))
            await ctx.send(embed=emb)

    @commands.command()
    async def slap(self, ctx, member: discord.Member):
        if member == ctx.message.author:
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Ты не можешь дать пощёчину самому себе**',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(
                title='Реакция "Пощёчина":',
                description=f'**🤕 {ctx.message.author.mention} дал пощёчину {member.mention}**',
                color=ctx.author.color)
            emb.set_image(url=nekos.img('slap'))
            await ctx.send(embed=emb)

    @commands.command()
    async def pat(self, ctx, member: discord.Member):
        if member == ctx.message.author:
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Ты не можешь погладить самого себя**',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(
                title='Реакция "Погладить":',
                description=f'**🫂 {ctx.message.author.mention} погладил {member.mention}**',
                color=ctx.author.color)
            emb.set_image(url=nekos.img('pat'))
            await ctx.send(embed=emb)

    @commands.command(aliases=['8ball'])
    async def ball(self, ctx, *, question):
        message = ['Нет', 'Да', 'Возможно', 'Опредленно нет', 'Попробуй ещё раз', 'Даже не думай!', 'Никогда!'] 
        emb = discord.Embed(
            title='Магический шар',
            description=f'**🔮 {random.choice(message)}**',
            color=ctx.author.color)
        await ctx.send(embed=emb)

def setup(Bot):
    Bot.add_cog(fun(Bot))
    print('[Cogs] Fun\'s load!')