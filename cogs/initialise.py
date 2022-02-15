from discord.ext.commands import Cog, command

from db import db, server
from util import serverid, mylogs
from util.create_embeds import access_beta
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
        # await self._wallet_verifying_message(server_settings["verify_message_id"])

        beta_role = utils.get(server.guild.roles, name='Beta')
        server.__setattr__("beta_role", beta_role)

        mylogs.info("Server INIT Complete")

    # async def _menu_message(self, message_id):
    #     """Checks out the Menu message sets its attribute in server class"""
    #     menu_channel = server.menu_channel
    #     if menu_channel is None:
    #         await self._create_menu_channel_and_message()
    #         return
    #     mylogs.debug("Menu Channel Found")
    #     server.__setattr__('menu_message_id', message_id)

    async def _wallet_verifying_message(self, message_id):
        """Checks out the wallet verifying message and sets its attribute in server class"""
        verify_channel = server.verify_channel
        if verify_channel is None:
            await self._create_verify_channel_and_message()
            return
        mylogs.debug("Verification channel found")
        server.__setattr__("verify_message_id", message_id)

    # async def _create_menu_channel_and_message(self):
    #     """If the menu doesnt exists it created a new channel and a new message saves the channel and
    #      message id in database"""
    #     mylogs.debug("Creating a new menu channel")
    #     channel = await server.guild.create_text_channel("bot-menu", category=server.announcements.category)
    #     embed , buttons = access_menu()
    #     message = await channel.send(embed=embed,components=[buttons])
    #     await settings.update_one({"_id": serverid}, {"$set": {"channels.menu_channel": channel.id}})
    #     await settings.update_one({"_id": serverid}, {"$set": {"menu_message_id": message.id}})
    #     server.__setattr__("menu_message_id", message.id)

    async def _create_verify_channel_and_message(self):
        """If the verification doesnt exists it created a new channel and a new message saves the channel and
         message id in database"""
        mylogs.debug("Creating a new verification channel")
        channel = await server.guild.create_text_channel("Add-beta", category=server.announcements.category)
        embed, buttons = access_beta()
        message = await channel.send(embed=embed, components=[buttons])

        await settings.update_one({"_id": serverid}, {"$set": {"channels.verify_channel": channel.id}})
        await settings.update_one({"_id": serverid}, {"$set": {"verify_message_id": message.id}})
        server.__setattr__("verify_message_id", message.id)

    def _set_server(self, channels):
        """Created the server class and provides all the values"""
        for name, ch_id in channels.items():
            server.__setattr__(name, self.bot.get_channel(ch_id))


def setup(bot):
    bot.add_cog(Verify(bot))
