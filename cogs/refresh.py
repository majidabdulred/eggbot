from discord.ext.commands import Cog, is_owner, command
from discord_slash.cog_ext import cog_slash

from tasks.refresh_role import UpdateUser
from util.slash_options import options_refreshuser
from util.create_embeds import create_change_wallet_button, wallet_connect_message_refresh
import util.constants as C
from db.users import get_user_from_address
from db.local_db import verify_messages
from util.logs import mylogs


class Refresh(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="refresh", aliases=[" refresh"])
    async def dep_refresh(self, ctx):
        await ctx.reply("This command has been removed. Please use slash command.\n**/refresh**")

    @cog_slash(name="refresh", guild_ids=[C.serverid],
               description="Refresh your roles")
    async def refresh_roles(self, ctx):
        mylogs.debug(f"COMMAND_USED : refresh : {ctx.author.id} : {ctx.author.name}")
        await ctx.defer(hidden=True)
        await self._refresh_a_user(ctx, user=ctx.author)

    @is_owner()
    @cog_slash(name="refreshusers", guild_ids=[936169787724275732],
               options=options_refreshuser)
    async def admin_refresh_user(self, ctx, **kwargs):
        if len(kwargs) <= 0:
            await ctx.send("Nothing Provided")
            return
        if "userid" in kwargs.keys():
            userid = kwargs["userid"]
            user = await self.bot.server.fetch_user(userid)
            if user is None:
                return await ctx.send("Not the user")
            await self._refresh_a_user(ctx, user)
            return
        elif "address" in kwargs.keys():
            usersdb = await get_user_from_address(address=kwargs["address"])
            if len(usersdb) <= 0:
                await ctx.send("None user with this address found")
            for userdb in usersdb:
                user = await self.bot.server.fetch_user(userdb["_id"])
                if user is None:
                    await ctx.send(f"User Not found {userdb['_id']}")
                    continue
                await self._refresh_a_user(ctx, ctx.user)

    async def _refresh_a_user(self, ctx, user):
        up = UpdateUser(self.bot, user)
        if not (await up.exists()):
            embed, comps = wallet_connect_message_refresh(ctx)
            await ctx.send(embed=embed, components=[comps], hidden=True)

            return

        await up.refresh_single_user()
        if not up.changed:
            str_to_send = f"Your data is up to date.{up.total_score_str}\n{up.already_have_role}\n{up.wallet_str}.\n{up.chickens_str}."
        else:
            str_to_send = f"{up.total_score_str}\n{up.wallet_str}.\n{up.chickens_str}.\n{up.changed_str}"
        embed, comps = create_change_wallet_button(str_to_send)
        verify_messages[ctx.author.id] = {}
        verify_messages[ctx.author.id]["mode"] = "change"
        await ctx.send(embed=embed, components=[comps], hidden=True)


def setup(bot):
    bot.add_cog(Refresh(bot))
