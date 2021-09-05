import discord, requests
from discord.ext import commands
from utils.config import BotSettings # импортируем конфиг бота


class Music(commands.Cog): # создаём класс модуля музыки
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def lyrics(self, ctx, *, music = None):
        if music == None:
            emb = discord.Embed(title='Ошибка:', description='**:anger: Вы не указали песню!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)

        else:
            response = requests.get(f'https://some-random-api.ml/lyrics?title={music}')
            lyric = response.json()

            if len(lyric['lyrics']) <= 4000:
                emb = discord.Embed(title=f'Текст {lyric["title"]} ({lyric["author"]}):',
                    description=f'**{lyric["lyrics"]}**', color=BotSettings['Bot']['BasicColor'])
                emb.set_thumbnail(url=lyric['thumbnail']['genius'])
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(title=f'Текст {lyric["title"]} ({lyric["author"]}):',
                    description=f'**{lyric["links"]["genius"]}**', color=BotSettings['Bot']['BasicColor'])
                emb.set_thumbnail(url=lyric['thumbnail']['genius'])
                await ctx.send(embed=emb)



def setup(Bot): # подключаем класс к основному файлу 
    Bot.add_cog(Music(Bot))
    print(f'[MODULES] Music\'s load!') # принтуем
