import discord, json, requests
from discord.ext import commands
from utils.config import BotBasicColor, BotPrefix, BotToken, BotErrorColor


class Commands(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    
    @commands.command()
    async def help(self, ctx):
        emb = discord.Embed(title='Команды бота:',
            description=f'**:chart_with_upwards_trend: {BotPrefix}stats** - статистика бота'
                        f'**:video_game: {BotPrefix}activity** - игры и ютуб в голосовом канале', color=BotBasicColor)
        await ctx.send(embed=emb)


    @commands.command()
    async def stats(self, ctx):
        file = open("uptime.txt", "r")
        text = file.read()
        file.close()

        emb = discord.Embed(title='Статистика бота:',
            description=f'**:books: Всего серверов:** {len(self.Bot.guilds)}\n'
                        f'**:busts_in_silhouette: Всего пользователей:** {len(self.Bot.users)}\n'
                        f'**:satellite_orbital: Время работы:** {text}', color=BotBasicColor)
        await ctx.send(embed=emb)


    @commands.command()
    async def activity(self, ctx, func=None):
        if ctx.author.voice != None:
            if func == None:
                emb = discord.Embed(title='Функции команды:',
                    description='**:clapper: ytt** - "YouTube Together" или же совместный просмотр YouTube в голосовом канале\n'
                                '**:chess_pawn: chess** - "Chess In The Park" или же шахматы в голосовом канале\n'
                                '**:black_joker: poker** - "Poker Night" или же покер в голосовм канале', color=BotBasicColor)
                await ctx.send(embed=emb)

            elif func == 'ytt':
                data = {'max_age': 3600, 'max_uses': 0, 'target_application_id': 755600276941176913, 'target_type': 2, 'temporary': False,
                    'validate': None}
                headers = {'Authorization': f'Bot {BotToken}', 'Content-Type': 'application/json'}
                response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                    data=json.dumps(data), headers=headers)
                link = json.loads(response.content)

                emb = discord.Embed(title='YouTube Together:',
                    description='**:clapper: Для совместного просмотра YouTube, перейдите по ссылке**', color=BotBasicColor)
                await ctx.send(content=f'https://discord.gg/{link["code"]}', embed=emb)

            elif func == 'chess':
                data = {'max_age': 3600, 'max_uses': 0, 'target_application_id': 832012774040141894, 'target_type': 2, 'temporary': False,
                    'validate': None}
                headers = {'Authorization': f'Bot {BotToken}', 'Content-Type': 'application/json'}
                response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                    data=json.dumps(data), headers=headers)
                link = json.loads(response.content)

                emb = discord.Embed(title='Chess In The Park:', description='**:chess_pawn: Для игры в шахматы, перейдите по ссылке**',
                    color=BotBasicColor)
                await ctx.send(content=f'https://discord.gg/{link["code"]}', embed=emb)

            elif func == 'poker':
                data = {'max_age': 3600, 'max_uses': 0, 'target_application_id': 755827207812677713, 'target_type': 2, 'temporary': False,
                    'validate': None}
                headers = {'Authorization': f'Bot {BotToken}', 'Content-Type': 'application/json'}
                response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                    data=json.dumps(data), headers=headers)
                link = json.loads(response.content)

                emb = discord.Embed(title='Poker Night:', description='**:black_joker: Для игры в покер, перейдите по ссылке**',
                    color=BotBasicColor)
                await ctx.send(content=f'https://discord.gg/{link["code"]}', embed=emb)

            else:
                emb = discord.Embed(title='Ошибка:', description='**Вы указали не существующую функцию команды!**', color=BotErrorColor)
                await ctx.send(embed=emb)
            
        else:
            emb = discord.Embed(title='Ошибка:', description='**Вы должны находиться в голосовом канале при использовании команды!**',
                color=BotErrorColor)
            await ctx.send(embed=emb)


    @commands.command()
    async def embed(self, ctx, *, text=None):
        if text != None:
            text = text.split('|')
            if '|' in ctx.message.content:
                emb = discord.Embed(title=text[1], description=text[0], color=BotBasicColor)
                for a in ctx.message.attachments:
                    if a.url != None:
                        emb.set_image(url=a.url)
                await ctx.message.delete()
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(description=text[0], color=BotBasicColor)
                for a in ctx.message.attachments:
                    if a.url != None:
                        emb.set_image(url=a.url)
                await ctx.message.delete()
                await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title=f'Ошибка:', description='Укажи что надо написать',
                color=BotErrorColor)
            await ctx.send(embed=emb)


def setup(Bot):
    Bot.add_cog(Commands(Bot))
    print(f'[MODULES] Commands\'s load!')
