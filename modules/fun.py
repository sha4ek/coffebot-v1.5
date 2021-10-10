import disnake, requests, json, nekos
from disnake.ext import commands

from utils.config import BotSettings


HeaderAuthorization = {'Authorization': f'Bot {BotSettings["Token"]}', 'Content-Type': 'application/json'} # переменная с хеадером
GreenColor = BotSettings['GreenColor'] # переменная с цветом эмбеда
RedColor = BotSettings['RedColor'] # переменная с цветом эмбеда
OrangeColor = BotSettings['OrangeColor'] # переменная с цветом эмбеда


class Fun(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot


    @commands.group(case_insensitive=True, invoke_without_command=True)
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, create_instant_invite=True)
    async def activity(self, ctx):
        emb = disnake.Embed(
            title='Помощь по команде:',
            description=f'> **{ctx.prefix}activity youtube** - совместный просмотр YouTube в голосовом канале\n'
                        f'> **{ctx.prefix}activity chess** - шахматы в голосовом канале\n'
                        f'> **{ctx.prefix}activity poker** - покер в голосовом канале',
            color=OrangeColor
        )

        await ctx.send(embed=emb)


    @activity.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, create_instant_invite=True)
    async def youtube(self, ctx):
        if ctx.author.voice != None:
            data = {
                'max_age': 3600,
                'max_uses': 0,
                'target_application_id': 880218394199220334,
                'target_type': 2,
                'temporary': False,
                'validate': None
            }

            response = requests.post(
                f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                data=json.dumps(data),
                headers=HeaderAuthorization
            )

            link = json.loads(response.content)
            
            emb = disnake.Embed(
                title='YouTube Together:',
                description=f'> **[Подключиться к просмотру](https://discord.gg/{link["code"]})**',
                color=OrangeColor
            )
        
        else:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы должны находиться в голосовом канале при использовании команды!**',
                color=RedColor
            )
        
        await ctx.send(embed=emb)


    @activity.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, create_instant_invite=True)
    async def chess(self, ctx):
        if ctx.author.voice != None:
            data = {
                'max_age': 3600,
                'max_uses': 0,
                'target_application_id': 832012774040141894,
                'target_type': 2,
                'temporary': False,
                'validate': None
            }

            response = requests.post(
                f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                data=json.dumps(data),
                headers=HeaderAuthorization
            )

            link = json.loads(response.content)
            
            emb = disnake.Embed(
                title='Chess In The Park:',
                description=f'> **[Подключиться к игре](https://discord.gg/{link["code"]})**',
                color=OrangeColor
            )
        
        else:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы должны находиться в голосовом канале при использовании команды!**',
                color=RedColor
            )
        
        await ctx.send(embed=emb)


    @activity.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, create_instant_invite=True)
    async def poker(self, ctx):
        if ctx.author.voice != None:
            data = {
                'max_age': 3600,
                'max_uses': 0,
                'target_application_id': 755827207812677713,
                'target_type': 2,
                'temporary': False,
                'validate': None
            }

            response = requests.post(
                f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                data=json.dumps(data),
                headers=HeaderAuthorization
            )

            link = json.loads(response.content)
            
            emb = disnake.Embed(
                title='Poker Night:',
                description=f'> **[Подключиться к игре](https://discord.gg/{link["code"]})**',
                color=OrangeColor
            )
        
        else:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы должны находиться в голосовом канале при использовании команды!**',
                color=RedColor
            )
        
        await ctx.send(embed=emb)


    @commands.command()
    async def kiss(self, ctx, member: disnake.Member = None):
        if member == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=RedColor
            )

        elif member == ctx.message.author:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете поцеловать самого себя!**',
                color=RedColor
            )

        else:
            emb = disnake.Embed(
                title='Реакция "Поцелуй":',
                description=f'> **{ctx.message.author.mention} поцеловал {member.mention}**',
                color=OrangeColor
            )
            emb.set_image(url=nekos.img('kiss'))
        
        await ctx.send(embed=emb)


    @commands.command()
    async def hug(self, ctx, member: disnake.Member = None):
        if member == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=RedColor
            )

        elif member == ctx.message.author:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете обнять самого себя!**',
                color=RedColor
            )

        else:
            emb = disnake.Embed(
                title='Реакция "Обнимашки":',
                description=f'> **{ctx.message.author.mention} обнял {member.mention}**',
                color=OrangeColor
            )
            emb.set_image(url=nekos.img('hug'))
        
        await ctx.send(embed=emb)


    @commands.command()
    async def slap(self, ctx, member: disnake.Member = None):
        if member == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=RedColor
            )

        elif member == ctx.message.author:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете дать пощёчину самому себе!**',
                color=RedColor
            )

        else:
            emb = disnake.Embed(
                title='Реакция "Пощёчина":',
                description=f'> **{ctx.message.author.mention} дал пощёчину {member.mention}**',
                color=OrangeColor
            )
            emb.set_image(url=nekos.img('slap'))
        
        await ctx.send(embed=emb)


    @commands.command()
    async def pat(self, ctx, member: disnake.Member = None):
        if member == None:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=RedColor
            )

        elif member == ctx.message.author:
            emb = disnake.Embed(
                title='Ошибка:',
                description='> **Вы не можете погладить самого себя!**',
                color=RedColor
            )

        else:
            emb = disnake.Embed(
                title='Реакция "Погладить":',
                description=f'> **{ctx.message.author.mention} погладил {member.mention}**',
                color=OrangeColor
            )
            emb.set_image(url=nekos.img('pat'))
        
        await ctx.send(embed=emb)


def setup(Bot):
    Bot.add_cog(Fun(Bot))
    print(f'[MODULES] Module "Fun" is loaded!')
