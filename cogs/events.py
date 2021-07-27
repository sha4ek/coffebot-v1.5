import discord
from discord.ext import commands
from config import Prefix

class events(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Команда не найдена**\n'
                            f'**💯 Для ознакомления с ними напиши:** {Prefix}help',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        elif isinstance(error, commands.MissingRequiredArgument):
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Команда введена не правильно**\n'
                            f'**💯 Для ознакомления с ней напиши:** {Prefix}help',
                color=ctx.author.color)
            await ctx.send(embed=emb)
        elif isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(
                title='Ошибка:',
                description='**💢 Недостаточно прав для использования**',
                color=ctx.author.color)
            await ctx.send(embed=emb)
            
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 869390569250619393:
            if str(payload.emoji) == '<:GreenTick:869395280989143052>':
                role = self.Bot.get_guild(payload.guild_id).get_role(869390228798963752)
                member = self.Bot.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.add_roles(role)
        if payload.message_id == 869387019355320390:
            if str(payload.emoji) == '<:GreenTick:869395280989143052>':
                role = self.Bot.get_guild(payload.guild_id).get_role(869365112853630997)
                member = self.Bot.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 869390569250619393:
            if str(payload.emoji) == '<:GreenTick:869395280989143052>':
                role = self.Bot.get_guild(payload.guild_id).get_role(869390228798963752)
                member = self.Bot.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)
        if payload.message_id == 869387019355320390:
            if str(payload.emoji) == '<:GreenTick:869395280989143052>':
                role = self.Bot.get_guild(payload.guild_id).get_role(869365112853630997)
                member = self.Bot.get_guild(payload.guild_id).get_member(payload.user_id)
                await member.remove_roles(role)

def setup(Bot):
    Bot.add_cog(events(Bot))
    print('[Cogs] Events\'s load!')
