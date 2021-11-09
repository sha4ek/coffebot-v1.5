import blist
import requests
import json
from disnake.ext import commands, tasks
from utils.config import BotConfig

class Monitorings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blist = blist.Blist(self.bot, token=BotConfig['Blist'])

    
    @tasks.loop(minutes=15)
    async def post(self):
        data = {
                'servers': len(self.bot.guilds),
                'users': len(self.bot.users)
            }
        
        requests.post(f'https://api.boticord.top/v1/stats',
            data=json.dumps(data),
            headers={
                'Authorization': BotConfig['Boticord'],
                'Content-Type': 'application/json'
            })

        await self.blist.post_bot_stats()

    
    @commands.Cog.listener()
    async def on_ready(self):
        self.post.start()

    
def setup(bot):
    bot.add_cog(Monitorings(bot))
    print(f'[SYSTEM] Module "monitorings" loaded!')
