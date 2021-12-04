import requests
import json
from disnake.ext import commands, tasks
from utils.config import BotConfig

class Monitorings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @tasks.loop(minutes=30)
    async def post(self):
        BoticordData = {
                'servers': len(self.bot.guilds),
                'shards': self.bot.shard_count or 1,
                'users': len(self.bot.users)
            }
        DiscordBoatsData = {
                'server_count': len(self.bot.guilds),
            }
        
        requests.post(f'https://api.boticord.top/v1/stats',
            data=json.dumps(BoticordData),
            headers={
                'Authorization': BotConfig['Boticord'],
                'Content-Type': 'application/json'
            })
        requests.post(f'https://discord.boats/api/bot/875927971649712148',
            data=json.dumps(DiscordBoatsData),
            headers={
                'Authorization': BotConfig['Discord Boats'],
                'Content-Type': 'application/json'
            })

    
    @commands.Cog.listener()
    async def on_ready(self):
        self.post.start()

    
def setup(bot):
    bot.add_cog(Monitorings(bot))
    print(f'[SYSTEM] Module "monitorings" loaded!')
