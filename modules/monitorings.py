import blist
import requests
import json
from disnake.ext import commands, tasks
from utils.config import BotConfig

class Monitorings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blist = blist.Blist(self.bot, token=BotConfig['Blist'])

    
    @tasks.loop(minutes=30)
    async def post(self):
        BoticordData = {
                'servers': len(self.bot.guilds),
                'shards': self.bot.shard_count or 1,
                'users': len(self.bot.users)
            }
        BladelistData = {
                'server_count': len(self.bot.guilds),
                'shard_count': self.bot.shard_count or 1
            }
        
        requests.post(f'https://api.boticord.top/v1/stats',
            data=json.dumps(BoticordData),
            headers={
                'Authorization': BotConfig['Boticord'],
                'Content-Type': 'application/json'
            })
        requests.post(f'https://api.bladelist.gg/bots/875927971649712148',
            data=json.dumps(BladelistData),
            headers={
                'Authorization': f'Token {BotConfig["Bladelist"]}',
                'Content-Type': 'application/json'
            })
        await self.blist.post_bot_stats()

    
    @commands.Cog.listener()
    async def on_ready(self):
        self.post.start()

    
def setup(bot):
    bot.add_cog(Monitorings(bot))
    print(f'[SYSTEM] Module "monitorings" loaded!')
