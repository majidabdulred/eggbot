from discord.ext.commands import Cog
from discord_slash.cog_ext import cog_slash
from util import serverid
from util.slash_options import options_find


class Find(Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_slash(name="find",
               guild_ids=[serverid],
               description="Find any chicken matching the traits",
               options=options_find)
    async def findchicks(self, ctx, **kwargs):
        print(kwargs)
        await ctx.send("Hi")


def setup(bot):
    bot.add_cog(Find(bot))
