"""
Ban royale thingy
"""

import random
from typing import Dict, Optional, Union

import discord 
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(
    command_prefix="!", # change to your prefix
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(
        users=True, roles=False,
        everyone=False
    ),
    intents=intents
)

client.remove_command('help')
client.config: Dict[str, Union[int, str]] = {
    "ban_logs": 804388540297379900, # where bans are tracked (can be same channel as ban channel)
    "ban_channel": 804388527642378301, # where everyone bans / where commands can be used
    "ban_chance": 1, # chance that the ban is successful, set to 1 for normal usage (100%)
    "react_emoji": "✅", # reacts with this when banned
    "token": "" # the BOT TOKEN that you'll be running this bot with
}

class Main(commands.Cog):

    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.config = self.client.config

    @commands.command(name="ban", aliases=['b'])
    async def _ban(self, ctx: commands.Context, *, user: str = None) -> discord.Message:
        if not user:
            return await ctx.send(f"{ctx.author.mention}, I need someone to ban.")

        if ctx.channel.id != self.config['ban_channel']:
            return await ctx.send(f"{ctx.author.mention}, You can't ban in this channel!")

        if not ctx.guild:
            return await ctx.send("You can't ban people in DMs")

        try:
            user = await commands.MemberConverter().convert(ctx, user)
        except Exception:
            return await ctx.send(f"{ctx.author.mention}, I can't find that user!")

        if user.id == ctx.author.id:
            return await ctx.send(f"{ctx.author.mention}, You can't ban yourself.")
     
        if ctx.author.top_role.position < user.top_role.position:
            return await ctx.send(f"{ctx.author.mention}, You can't ban that person!")

        if random.random() < self.config['ban_chance']:
            try:
                await user.ban(reason=f"Ban Royale: Banned by {ctx.author.name}")
            except discord.Forbidden: 
                return await ctx.send("I don't have permissions to do that. Please contact an admin to fix this.")
            
            await ctx.message.add_reaction(self.config['react_emoji'])
            return await self.client.get_channel(self.config['ban_logs']).send(f"{ctx.author.mention} banned {user.mention}!")
        return await ctx.send(f"{ctx.author.mention}, your attempted ban against **{user.name}** failed! (lol)")

client.add_cog(Main(client))
client.run(client.config['token'])
