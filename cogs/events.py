import discord
from discord.ext import commands
from config import Prefix

class events(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Команда не найдена**\n'
                            f'**💯 Для ознакомления с ними напиши:** {Prefix}help',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        elif isinstance(error, commands.MissingRequiredArgument):
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Команда введена не правильно**\n'
                            f'**💯 Для ознакомления с ней напиши:** {Prefix}help',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        elif isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Недостаточно прав для использования**',
                color=ctx.author.color)
            await ctx.send(embed=emb)

def setup(Bot):
    Bot.add_cog(events(Bot))
    print('[Cogs] Events\'s load!')