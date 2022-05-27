from discord import Embed
from discord.ext.commands import Cog
from discord_slash import ButtonStyle
from discord_slash.cog_ext import cog_slash
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from db.local_db import server
import util.slash_options as op
import util.constants as C
from db.whitelistdb import get_user_whitelist, add_whitelist, remove_whitelist
from util.logs import mylogs


class Whitelist(Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_slash(name="whitelist", guild_ids=[C.serverid],
               description="Add your address to whitelist",
               options=op.options_whitelist)
    async def whitelist(self, ctx, address: str):
        mylogs.debug(f"COMMAND_USED : whitelist : {ctx.author.name} : {ctx.author_id}")
        res = WhitelistAdd(ctx, address)
        await res.run()


class WhitelistAdd:
    def __init__(self, ctx, address):
        self.ctx = ctx
        self.address = address
        self.author_id = ctx.author_id

    async def run(self):
        await self.ctx.defer(hidden=True)
        if self.ctx.channel.id != server.add_whitelist.id:
            mylogs.debug(f"INVALID_CHANNEL : whitelist : {self.ctx.author.name}")
            await self.ctx.send(f"This command can only be used in <#{server.add_whitelist.id}> .", hidden=True)
            return
        if len(self.address) != 42:
            mylogs.debug(f"INVALID_COMMAND_USAGE : whitelist : {self.address}  : {self.ctx.author.name}")
            await self.ctx.send("Address not in valid format . Please write the full wallet address", hidden=True)
            return
        if user := await get_user_whitelist(self.ctx.author_id):
            mylogs.debug(f"WHITELIST_ALREADY_FOUND : {self.ctx.author.name} : {user['address']}")

            await self.already_stored_address(user)
            return

        await add_whitelist(self.ctx.author_id, self.address)
        if user := await get_user_whitelist(self.ctx.author_id):
            mylogs.info(f"ADDED_WHITELIST : {self.ctx.author.name}  : {self.address}")
            await self.ctx.send(f"Successfully added `{self.address}` to the whitelist", hidden=True)
            await server.add_whitelist.send(f"Added {self.ctx.author.name} to whitelist.")
        await self.ctx.author.add_roles(*[server.whitelist_role])

    async def already_stored_address(self, user):
        embed = Embed(title="You have already registered",
                      description=f"You have already added `{user['address']}` to the whitelist.\n"
                                  "Click on Remove to remove this address from whitelist and add a new one.")

        button1 = [
            create_button(style=ButtonStyle.red, label="Remove", custom_id="remove_white_address")]
        row1 = create_actionrow(*button1)
        await self.ctx.send(embed=embed, components=[row1], hidden=True)
        react = await wait_for_component(self.ctx.bot, components=row1, check=self.check_author,
                                         timeout=180)
        if react.custom_id == "remove_white_address":
            await react.defer(edit_origin=True)
            await remove_whitelist(self.author_id)
            mylogs.debug(f"REMOVED_WHITELIST : {self.ctx.author.name} : {self.address}")
            await react.edit_origin(embeds=[], components=[],
                                    content=f"Successfully removed `{user['address']}` from whitelist.\n"
                                            f"Use /whitelist to add a new address")
            await self.ctx.author.remove_roles(*[server.whitelist_role])

    def check_author(self, ctx):
        return ctx.author_id == self.author_id


def setup(bot):
    bot.add_cog(Whitelist(bot))
