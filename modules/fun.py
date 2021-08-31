import discord, json, requests, nekos
from discord.ext import commands
from utils.config import BotSettings # импортируем конфиг бота


class Fun(commands.Cog): # создаём класс модуля фан-команд
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, create_instant_invite=True)
    async def activity(self, ctx, func = None): # создаём команду активити
        headers = {'Authorization': f'Bot {BotSettings["Bot"]["Token"]}', 'Content-Type': 'application/json'}

        if ctx.author.voice != None: # проверяем, есть ли автор в голосовом канале
            if func == None: # проверяем, присутствует ли функция
                emb = discord.Embed(title='Функции команды:',
                    description='**:clapper: ytt** - "YouTube Together" или же совместный просмотр YouTube в голосовом канале\n'
                                '**:chess_pawn: chess** - "Chess In The Park" или же шахматы в голосовом канале\n'
                                '**:black_joker: poker** - "Poker Night" или же покер в голосовом канале',
                    color=BotSettings['Bot']['BasicColor'])
                await ctx.send(embed=emb)

            elif func == 'ytt':
                data = {'max_age': 3600, 'max_uses': 0, 'target_application_id': 755600276941176913, 'target_type': 2, 'temporary': False,
                    'validate': None}
                response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                    data=json.dumps(data), headers=headers)
                link = json.loads(response.content)

                emb = discord.Embed(title='YouTube Together:',
                    description='**:clapper: Для совместного просмотра YouTube, перейдите по ссылке**',
                    color=BotSettings['Bot']['BasicColor'])
                await ctx.send(content=f'https://discord.gg/{link["code"]}', embed=emb)

            elif func == 'chess':
                data = {'max_age': 3600, 'max_uses': 0, 'target_application_id': 832012774040141894, 'target_type': 2, 'temporary': False,
                    'validate': None}
                response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                    data=json.dumps(data), headers=headers)
                link = json.loads(response.content)

                emb = discord.Embed(title='Chess In The Park:',
                    description='**:chess_pawn: Для игры в шахматы, перейдите по ссылке**', color=BotSettings['Bot']['BasicColor'])
                await ctx.send(content=f'https://discord.gg/{link["code"]}', embed=emb)

            elif func == 'poker':
                data = {'max_age': 3600, 'max_uses': 0, 'target_application_id': 755827207812677713, 'target_type': 2, 'temporary': False,
                    'validate': None}
                response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                    data=json.dumps(data), headers=headers)
                link = json.loads(response.content)

                emb = discord.Embed(title='Poker Night:',
                    description='**:black_joker: Для игры в покер, перейдите по ссылке**', color=BotSettings['Bot']['BasicColor'])
                await ctx.send(content=f'https://discord.gg/{link["code"]}', embed=emb)

            else:
                emb = discord.Embed(title='Ошибка:',
                    description='**:anger: Вы указали не существующую функцию команды!**', color=BotSettings['Bot']['ErrorColor'])
                await ctx.send(embed=emb)
            
        else:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы должны находиться в голосовом канале при использовании команды!**',
                color=BotSettings['Bot']['ErrorColor'])
            await ctx.send(embed=emb)


    @commands.command()
    @commands.cooldown(rate=1, per=4.0, type=commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def cat(self, ctx):
        emb1 = discord.Embed(title='Милые котики:', color=BotSettings['Bot']['BasicColor'])
        emb2 = discord.Embed(color=BotSettings['Bot']['BasicColor'])
        emb2.set_image(url=nekos.cat())
        await ctx.send(embed=emb1)
        await ctx.send(embed=emb2)


def setup(Bot):
    Bot.add_cog(Fun(Bot))
    print(f'[MODULES] Fun\'s load!')
