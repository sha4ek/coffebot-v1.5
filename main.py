import discord, os, asyncio
from discord.ext import commands
from utils.config import BotPrefix, BotToken, BotPostfix


BotIntents = discord.Intents.default()
BotIntents.members = True
Bot = commands.Bot(command_prefix=BotPrefix, intents=BotIntents)
Bot.remove_command('help')


for file in os.listdir('./modules'):
    if file.endswith('.py'):
        Bot.load_extension(f'modules.{file[:-3]}')


@Bot.event
async def on_ready():
    print(f'[SYSTEM] {Bot.user.name}\'s online!')

    seconds=0
    minutes=0
    hours=0
    days=0

    while True:
        seconds += 1

        if seconds == 60:
            minutes += 1
            seconds = 0
        if minutes == 60:
            hours += 1
            minutes = 0
        if hours == 24:
            days += 1
            hours = 0

        if seconds != 0:
            file = open("uptime.txt", "w")
            file.write(f'{seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
            file.close()
        if minutes != 0:
            file = open("uptime.txt", "w")
            file.write(f'{minutes} {BotPostfix(minutes, "минута", "минуты", "минут")} {seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
            file.close()
        elif hours != 0:
            file = open("uptime.txt", "w")
            file.write(f'{hours} {BotPostfix(hours, "час", "часа", "часов")} {minutes} {BotPostfix(minutes, "минута", "минуты", "минут")} {seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
            file.close()
        elif days != 0:
            file = open("uptime.txt", "w")
            file.write(f'{days} {BotPostfix(days, "день", "дня", "дней")} {hours} {BotPostfix(hours, "час", "часа", "часов")} {minutes} {BotPostfix(minutes, "минута", "минуты", "минут")} {seconds} {BotPostfix(seconds, "секунда", "секунды", "секунд")}')
            file.close()
        await asyncio.sleep(1)


Bot.run(BotToken)
