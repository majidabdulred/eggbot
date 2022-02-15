from discord.ext.commands import Cog, command
from discord_slash.cog_ext import cog_slash
import util.constants as C

from tasks.refresh_role import UpdateUser


class Refresh(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @command(name="help")
    async def help_command(self, ctx):
        return

    @cog_slash(name="refresh", guild_ids=[C.serverid],
               description="Refresh your roles")
    async def refresh_roles(self, ctx):
        await ctx.defer(hidden=True)
        up = UpdateUser(self.bot, ctx.author)
        await up.refresh_single_user()
        if not up.changed:
            str_to_send = f"Your data is up to date.{up.total_score_str}\n{up.already_have_role}\n{up.wallet_str}.\n{up.chickens_str}."
        else:
            str_to_send = f"{up.total_score_str}\n{up.wallet_str}.\n{up.chickens_str}.\n{up.changed_str}"
        await ctx.send(str_to_send, hidden=True)


def setup(bot):
    bot.add_cog(Refresh(bot))
