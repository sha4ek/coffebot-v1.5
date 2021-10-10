import disnake
from disnake.ext import commands

from utils.config import MongoSettings, BotSettings


GreenColor = BotSettings['GreenColor'] # переменная с цветом эмбеда
RedColor = BotSettings['RedColor'] # переменная с цветом эмбеда
GuildsData = MongoSettings['GuildsData'] # переменная с дата-базой монги


class Settings(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    
    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    @commands.has_permissions(manage_guild=True) 
    async def prefix(self, ctx, prefix = None):  
        if prefix != None:
            if len(str(prefix)) <= 3:
                GuildsData.update_one({
                    'GuildID': ctx.guild.id
                },
                {
                    '$set': {
                        'GuildPrefix': prefix
                    }
                })

                emb = disnake.Embed(
                    title=f'Смена префикса:',
                    description=f'> **Вы успешно сменили префикс на "{prefix}"**',
                    color=GreenColor
                )

            else:
                emb = disnake.Embed(
                    title='Ошибка:',
                    description=f'> **Префикс не может быть больше 3 символов!**',
                    color=RedColor
                )
        else:
            emb = disnake.Embed(
                title='Ошибка:',
                description=f'> **Вы не указали префикс!**',
                color=RedColor
            )
        
        await ctx.send(embed=emb)


def setup(Bot):
    Bot.add_cog(Settings(Bot))
    print(f'[MODULES] Module "Settings" is loaded!')
