print(f'[System] Connecting...')

import discord, os, asyncio, random
from discord.ext import commands
from config import Prefix, Postfix

Bot = commands.Bot(command_prefix=Prefix, intents=discord.Intents.all())
Bot.remove_command('help')
Bot.load_extension("jishaku")

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        Bot.load_extension(f'cogs.{file[:-3]}')

@Bot.event
async def on_ready():
    music = ['1000-7', '2DWRLD', 'Akame Ga Kill!', 'Akudama Drive', 'clown']

    print(f'[System] {Bot.user.name}\'s online')

    while True:
        await Bot.change_presence(
            activity=discord.Activity(
                name=f'за {len(Bot.users)} {Postfix(len(Bot.users), "участником", "участниками", "участниками")} | {Prefix}help',
                type=discord.ActivityType.watching),
            status=discord.Status.idle)
        await asyncio.sleep(6)

        await Bot.change_presence(
            activity=discord.Activity(
                name=f'за {len(Bot.guilds)} {Postfix(len(Bot.guilds), "сервером", "серверами", "серверами")} | {Prefix}help',
                type=discord.ActivityType.watching),
            status=discord.Status.idle)
        await asyncio.sleep(6)

        now_playing = random.randint(0, 4)

        await Bot.change_presence(
            activity=discord.Activity(
                name=f'{music[now_playing]} | {Prefix}help',
                type=discord.ActivityType.listening),
            status=discord.Status.idle)
        await asyncio.sleep(6)

@Bot.event
async def on_message(message):
    if f'{chr(96) * 3}py' in message.content:
        await message.add_reaction('🐍')
    if message.author != Bot.user:
        if not message.guild:
            channel = Bot.get_channel(869191233640226816)

            if message.content == None:
                text = 'Отсутствует'
            else:
                text = message.content
                
            if message.attachments == []:
                file = 'Отсутствует'
            else:
                file = f'{message.attachments[0].filename} ({message.attachments[0].url})'
            
            emb = discord.Embed(
                title='Личные сообщения бота',
                description=f'**📨 Отправитель:** {message.author} ({message.author.id})'
                            f'**📄 Сообщение:** {text}\n'
                            f'**📌 Прикреплённый файл:** {file}',
                color=0xff9900) 
            emb.set_thumbnail(url=message.author.avatar_url)
            
            for a in message.attachments:
                if a.url != None:
                    emb.set_image(url=a.url)
                else:
                    pass

            await channel.send(embed=emb)
        else:
            await Bot.process_commands(message)


@Bot.command()
@commands.is_owner()
async def load(ctx, extension):
    Bot.load_extension(f'cogs.{extension}')
    emb = discord.Embed(
        title='Включение модуля',
        description='**⚠ Модуль {extension} включен**',
        color=ctx.author.color)
    await ctx.send(embed=emb)

@Bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    Bot.unload_extension(f'cogs.{extension}')
    emb = discord.Embed(
        title='Выключение модуля',
        description='**⚠ Модуль {extension} выключен**',
        color=ctx.author.color)
    await ctx.send(embed=emb)

@Bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    Bot.reload_extension(f'cogs.{extension}')
    emb = discord.Embed(
        title='Перезагрузка модуля',
        description='**⚠ Модуль {extension} перезагружен**',
        color=ctx.author.color)
    await ctx.send(embed=emb)
    
@Bot.command(aliases=['place-react'])
async def place_react(ctx, message: discord.Message, reaction: discord.Emoji):
    await message.add_reaction(reaction)

token = os.environ.get('Token')

Bot.run(token)
