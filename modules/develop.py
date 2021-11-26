import disnake as discord
import time
import aeval
from disnake.ext import commands
from utils.config import BotConfig, MongoConfig


class Develop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, ucode=None):
        if not ucode:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не указали код!**',
                color=BotConfig['RedColor'])
        
        else:
            code = '\n'.join(ucode.split('\n')[1:])[:-3] if ucode.startswith('```') and ucode.endswith('```') else ucode
            libs = {
                'discord': discord,
                'bot': self.bot,
                'ctx': ctx,
                'GuildsData': MongoConfig['GuildsData']
            }

            start = time.time()

            try:
                reval = await aeval.aeval(code, libs, {})
                end = time.time() - start

                emb = discord.Embed(title='Успешное выполнение:',
                    description=f'> **Время выполнения** - {end}\n'
                                f'> **Входные данные** - \n```py\n{code}\n```\n'
                                f'> **Выходные данные** - \n```py\n{reval}\n```\n',
                    color=BotConfig['GreenColor'])

            except Exception as exception:
                end = time.time() - start

                emb = discord.Embed(title='Ошибка выполнения:',
                    description=f'> **Время выполнения** - {end}\n'
                                f'> **Входные данные** - \n```py\n{code}\n```\n'
                                f'> **Выходные данные** - \n```py\n{exception}\n```\n',
                    color=BotConfig['RedColor'])

        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Develop(bot))
    print(f'[SYSTEM] Module "develop" loaded!')
