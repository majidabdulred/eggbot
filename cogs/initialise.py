import asyncio
from discord.ext.commands import Cog, command
from tasks.races import race_scheduler
from tasks.member_count import member_scheduler
from db import db, server
from tasks.results import scheduler_race_results
from util import serverid, mylogs
from discord import utils

settings = db["settings"]

mylogs.setLevel("DEBUG")


class Verify(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @command(name="help")
    async def help_command(self, ctx):
        return

    @Cog.listener()
    async def on_ready(self):
        mylogs.info("Starting Server Initialisation")
        settings = db["settings"]
        server_settings = await settings.find_one({"_id": serverid})
        server.__setattr__("guild", self.bot.get_guild(server_settings["_id"]))
        self._set_server(server_settings["channels"])

        whitelist = utils.get(server.guild.roles, name='Whitelist')
        server.__setattr__("whitelist_role", whitelist)

        loop = asyncio.get_event_loop()
        # loop.create_task(race_scheduler(20))
        # loop.create_task(scheduler_race_results(10))
        # loop.create_task(whitelist_counter())
        mylogs.info("Completed Server Initialisation")

    def _set_server(self, channels):
        """Created the server class and provides all the values"""
        for name, ch_id in channels.items():
            server.__setattr__(name, self.bot.get_channel(ch_id))


def setup(bot):
    bot.add_cog(Verify(bot))
