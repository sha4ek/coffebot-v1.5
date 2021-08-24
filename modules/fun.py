import discord
import json
import requests
from discord.ext import commands
from utils.config import BotBasicColor, BotToken, BotErrorColor # импортируем конфиг бота


class Fun(commands.Cog): # создаём класс модуля фан-команд
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.command()
    async def activity(self, ctx, func = None): # создаём команду активити
        if ctx.author.voice != None: # проверяем, есть ли автор в голосовом канале
            if func == None: # проверяем, присутствует ли функция
                emb = discord.Embed(title='Функции команды:',
                    description='**:clapper: ytt** - "YouTube Together" или же совместный просмотр YouTube в голосовом канале\n'
                                '**:chess_pawn: chess** - "Chess In The Park" или же шахматы в голосовом канале\n'
                                '**:black_joker: poker** - "Poker Night" или же покер в голосовом канале',
                    color=BotBasicColor)
                await ctx.send(embed=emb)

            elif func == 'ytt':
                data = {'max_age': 3600, 'max_uses': 0, 'target_application_id': 755600276941176913, 'target_type': 2, 'temporary': False,
                    'validate': None}
                headers = {'Authorization': f'Bot {BotToken}', 'Content-Type': 'application/json'}
                response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                    data=json.dumps(data), headers=headers)
                link = json.loads(response.content)

                emb = discord.Embed(title='YouTube Together:',
                    description='**:clapper: Для совместного просмотра YouTube, перейдите по ссылке**',
                    color=BotBasicColor)
                await ctx.send(content=f'https://discord.gg/{link["code"]}', embed=emb)

            elif func == 'chess':
                data = {'max_age': 3600, 'max_uses': 0, 'target_application_id': 832012774040141894, 'target_type': 2, 'temporary': False,
                    'validate': None}
                headers = {'Authorization': f'Bot {BotToken}', 'Content-Type': 'application/json'}
                response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                    data=json.dumps(data), headers=headers)
                link = json.loads(response.content)

                emb = discord.Embed(title='Chess In The Park:',
                    description='**:chess_pawn: Для игры в шахматы, перейдите по ссылке**', color=BotBasicColor)
                await ctx.send(content=f'https://discord.gg/{link["code"]}', embed=emb)

            elif func == 'poker':
                data = {'max_age': 3600, 'max_uses': 0, 'target_application_id': 755827207812677713, 'target_type': 2, 'temporary': False,
                    'validate': None}
                headers = {'Authorization': f'Bot {BotToken}', 'Content-Type': 'application/json'}
                response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                    data=json.dumps(data), headers=headers)
                link = json.loads(response.content)

                emb = discord.Embed(title='Poker Night:',
                    description='**:black_joker: Для игры в покер, перейдите по ссылке**', color=BotBasicColor)
                await ctx.send(content=f'https://discord.gg/{link["code"]}', embed=emb)

            else:
                emb = discord.Embed(title='Ошибка:',
                    description='**:anger: Вы указали не существующую функцию команды!**', color=BotErrorColor)
                await ctx.send(embed=emb)
            
        else:
            emb = discord.Embed(title='Ошибка:',
                description='**:anger: Вы должны находиться в голосовом канале при использовании команды!**',
                color=BotErrorColor)
            await ctx.send(embed=emb)


def setup(Bot):
    Bot.add_cog(Fun(Bot))
    print(f'[MODULES] Fun\'s load!')