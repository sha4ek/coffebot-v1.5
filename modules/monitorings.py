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
                'Authorization': 'kxNTVE5UF5zwA7USPxaDXm11ym0b9OBR5Fv1IsCvBA4V18FGDbAvNByeCHXfCTInxo32zGziT8Q0fyos46FlQV3NMYVWGlIEgvs3S4t7giEmeZIH6jS8QY65516hO1l6GsBVjJi64MKXuiVwsB09qPX4GcO',
                'Content-Type': 'application/json'
            })
        await self.blist.post_bot_stats()

    
    @commands.Cog.listener()
    async def on_ready(self):
        self.post.start()

    
def setup(bot):
    bot.add_cog(Monitorings(bot))
    print(f'[SYSTEM] Module "monitorings" loaded!')
