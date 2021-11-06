import disnake as discord
from disnake.ext import commands
from utils.config import BotConfig, MongoConfig
from utils.functions import BotPrefix


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='set-prefix')
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def _setprefix(self, ctx, new_prefix=None):
        if not new_prefix:
            emb = discord.Embed(title=f'Помощь по команде:',
                description=f'> **{BotPrefix(self.bot, ctx.message)[2]}set-prefix [префикс]** - установить серверный префикс\n'
                            f'> **{BotPrefix(self.bot, ctx.message)[2]}set-prefix standard** - установить стандартный префикс\n',
                color=BotConfig['OrangeColor'])

        elif new_prefix == 'standard':
            if 'GuildPrefix' not in MongoConfig['GuildsData'].find_one({'GuildID': ctx.guild.id}):
                emb = discord.Embed(title='Ошибка:',
                    description='> **На сервере уже стоит стандартный префикс!**',
                    color=BotConfig['RedColor'])

            else:
                MongoConfig['GuildsData'].update_one({
                        'GuildID': ctx.guild.id
                    },
                    {
                        '$unset': {
                            'GuildPrefix': ''
                        }
                    })

                emb = discord.Embed(title='Смена префикса:',
                    description=f'> **Вы успешно сменили префикс на "{BotConfig["MainPrefix"]}"!**',
                    color=BotConfig['GreenColor'])

        else:
            if len(str(new_prefix)) <= 3:
                MongoConfig['GuildsData'].update_one({
                        'GuildID': ctx.guild.id
                    },
                    {
                        '$set': {
                            'GuildPrefix': new_prefix
                        }
                    })

                emb = discord.Embed(title='Смена префикса:',
                    description=f'> **Вы успешно сменили префикс на "{new_prefix}"!**',
                    color=BotConfig['GreenColor'])

            else:
                emb = discord.Embed(title='Ошибка:',
                    description=f'> **Префикс не должен быть больше 3 символов!**',
                    color=BotConfig['RedColor'])
                
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Settings(bot))
    print(f'[SYSTEM] Module "settings" loaded!')
