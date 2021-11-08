import blist
from disnake.ext import commands, tasks
from utils.config import BotConfig

class Monitorings(commands.Cog):
    async def __init__(self, bot):
        self.bot = bot
        self.blist = blist.Blist(self.bot, token=BotConfig['Blist'])
        self.webhook = blist.WebhookServer(self.blist)

        await self.webhook.run()

    
    @tasks.loop(seconds=120)
    async def blist_post(self):
        await self.blist.post_bot_stats()

        # Outside of a cog

    @commands.Cog.listener()
    async def on_blist_vote(self, user_id, time):
        pass
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.blist_post.start()

    
def setup(bot):
    bot.add_cog(Monitorings(bot))
    print(f'[SYSTEM] Module "monitorings" loaded!')
