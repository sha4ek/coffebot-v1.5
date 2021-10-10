import disnake
from disnake.ext import commands

from utils.config import BotSettings


OrangeColor = BotSettings['OrangeColor'] # переменная с цветом эмбеда


class General(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def avatar(self, ctx, member: disnake.Member = None):
        user = member if member != None else ctx.author

        emb = disnake.Embed(
            title=f'Аватарка {user.name}:',
            color=OrangeColor
        )
        emb.set_image(url=user.avatar)

        await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def links(self, ctx):
        emb = disnake.Embed(
            title='Полезные ссылки:',
            description=f'> **[Пригласить бота]({BotSettings["BotInvite"]})**\n'
                        f'> **[Сервер поддержки]({BotSettings["SupportGuild"]})**',
            color=OrangeColor
        )

        await ctx.send(embed=emb)
        

def setup(Bot):
    Bot.add_cog(General(Bot))
    print(f'[MODULES] Module "General" is loaded!')
