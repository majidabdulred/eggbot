import asyncio

from discord.ext.commands import Cog
from discord_slash.cog_ext import cog_component

from util import mylogs
from tasks import updatedb


class TestCog(Cog):

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        mylogs.setLevel("DEBUG")
        mylogs.debug("TESTING STARTED")
        loop = asyncio.get_event_loop()
        loop.create_task(updatedb.main_updater())



def setup(bot):
    bot.add_cog(TestCog(bot))
