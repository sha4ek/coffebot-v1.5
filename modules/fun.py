import disnake as discord
import requests
import json
import nekos
from disnake.ext import commands
from utils.config import BotConfig
from utils.functions import BotPrefix


view = discord.ui.View()
view.add_item(discord.ui.Button(label='Перепригласить', url=BotConfig['BotInvite']))


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(case_insensitive=True, invoke_without_command=True)
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, create_instant_invite=True)
    async def activity(self, ctx):
        emb = discord.Embed(title='Помощь по команде:',
            description=f'> **{BotPrefix(self.bot, ctx.message)[2]}activity youtube** - YouTube в голосовом канале\n'
                        f'> **{BotPrefix(self.bot, ctx.message)[2]}activity chess** - шахматы в голосовом канале\n'
                        f'> **{BotPrefix(self.bot, ctx.message)[2]}activity poker** - покер в голосовом канале',
            color=BotConfig['OrangeColor'])
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


    @activity.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, create_instant_invite=True)
    async def youtube(self, ctx):
        if ctx.author.voice:
            data = {
                'max_age': 3600,
                'max_uses': 0,
                'target_application_id': 880218394199220334,
                'target_type': 2,
                'temporary': False,
                'validate': None
            }
            response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                data=json.dumps(data),
                headers={
                    'Authorization': f'Bot {BotConfig["Token"]}',
                    'Content-Type': 'application/json'
                })
            link = json.loads(response.content)
            
            emb = discord.Embed(title='YouTube Together:',
                description=f'> **[Подключиться к просмотру](https://discord.gg/{link["code"]})**',
                color=BotConfig['OrangeColor'])
        
        else:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы должны находиться в голосовом канале при использовании команды!**',
                color=BotConfig['RedColor'])
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


    @activity.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, create_instant_invite=True)
    async def chess(self, ctx):
        if ctx.author.voice:
            data = {
                'max_age': 3600,
                'max_uses': 0,
                'target_application_id': 832012774040141894,
                'target_type': 2,
                'temporary': False,
                'validate': None
            }
            response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                data=json.dumps(data),
                headers={
                    'Authorization': f'Bot {BotConfig["Token"]}',
                    'Content-Type': 'application/json'
                })
            link = json.loads(response.content)
            
            emb = discord.Embed(title='Chess In The Park:',
                description=f'> **[Подключиться к игре](https://discord.gg/{link["code"]})**',
                color=BotConfig['OrangeColor'])
        
        else:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы должны находиться в голосовом канале при использовании команды!**',
                color=BotConfig['RedColor'])
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


    @activity.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, create_instant_invite=True)
    async def poker(self, ctx):
        if ctx.author.voice:
            data = {
                'max_age': 3600,
                'max_uses': 0,
                'target_application_id': 755827207812677713,
                'target_type': 2,
                'temporary': False,
                'validate': None
            }
            response = requests.post(f'https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites',
                data=json.dumps(data),
                headers={
                    'Authorization': f'Bot {BotConfig["Token"]}',
                    'Content-Type': 'application/json'
                })
            link = json.loads(response.content)
            
            emb = discord.Embed(title='Poker Night:',
                description=f'> **[Подключиться к игре](https://discord.gg/{link["code"]})**',
                color=BotConfig['OrangeColor'])
        
        else:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы должны находиться в голосовом канале при использовании команды!**',
                color=BotConfig['RedColor'])
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def kiss(self, ctx, member: discord.Member=None):
        if not member:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=BotConfig['RedColor'])

        elif member == ctx.message.author:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете поцеловать самого себя!**',
                color=BotConfig['RedColor'])

        else:
            emb = discord.Embed(title='Реакция "Поцелуй":',
                description=f'> **{ctx.message.author.mention} поцеловал {member.mention}!**',
                color=BotConfig['OrangeColor'])
            emb.set_image(url=nekos.img('kiss'))
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def hug(self, ctx, member: discord.Member=None):
        if not member:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=BotConfig['RedColor'])

        elif member == ctx.message.author:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете обнять самого себя!**',
                color=BotConfig['RedColor'])

        else:
            emb = discord.Embed(title='Реакция "Обнимашки":',
                description=f'> **{ctx.message.author.mention} обнял {member.mention}!**',
                color=BotConfig['OrangeColor'])
            emb.set_image(url=nekos.img('hug'))
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def slap(self, ctx, member: discord.Member=None):
        if not member:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=BotConfig['RedColor'])

        elif member == ctx.message.author:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете дать пощёчину самому себе!**',
                color=BotConfig['RedColor'])

        else:
            emb = discord.Embed(title='Реакция "Пощёчина":',
                description=f'> **{ctx.message.author.mention} дал пощёчину {member.mention}!**',
                color=BotConfig['OrangeColor'])
            emb.set_image(url=nekos.img('slap'))
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


    @commands.command()
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def pat(self, ctx, member: discord.Member=None):
        if not member:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не указали участника!**',
                color=BotConfig['RedColor'])

        elif member == ctx.message.author:
            emb = discord.Embed(title='Ошибка:',
                description='> **Вы не можете погладить самого себя!**',
                color=BotConfig['RedColor'])

        else:
            emb = discord.Embed(title='Реакция "Погладить":',
                description=f'> **{ctx.message.author.mention} погладил {member.mention}!**',
                color=BotConfig['OrangeColor'])
            emb.set_image(url=nekos.img('pat'))
        emb.set_footer(text=BotConfig['Slashes'])
        await ctx.send(embed=emb, view=view)


def setup(bot):
    bot.add_cog(Fun(bot))
    print(f'[SYSTEM] Module "fun" loaded!')
