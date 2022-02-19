from discord.ext.commands import Cog, command
from db import users as Users
from util.constants import submit_data_channel
from util.logs import mylogs
from db.local_db import submit_datadb
from commands.refresh_role import UpdateUser


class Verify(Cog):

    def __init__(self, bot):
        self.bot = bot

    def submit_data_check(self, ctx, uid, address):
        mylogs.debug(f"submitdata : {uid} : {address}")
        if ctx.channel.id != submit_data_channel:
            return False
        if uid == "" or not uid.isdigit():
            return False
        elif int(uid) not in submit_datadb.keys():
            return False
        return True

    @command(name="submitdata")
    async def submit_data(self, ctx, link: str, address: str):
        uid = link.lstrip("https://chickenderby.github.io/verify/?")
        if not self.submit_data_check(ctx, uid, address):
            await ctx.message.add_reaction("❌")
            return
        await ctx.message.add_reaction("🔧")
        userid = int(uid)
        main_ctx, user = submit_datadb[userid]
        old_data = await Users.get_user(userid)
        if old_data:
            await Users.set_address(userid, address)
            message = main_ctx.reply(
                f"<@{userid}>\nYour new address `{address[:12] + '...'}` has been verified. Use **/profile** commands to see your data.")
        else:
            await Users.save_user(userid, address)
            message = main_ctx.reply(
                f"<@{userid}>\nYour address `{address[:12] + '...'}` has been verified. Use **/profile** commands to see your data. ")
        submit_datadb.pop(userid)
        await ctx.message.add_reaction("👍")
        up = UpdateUser(self.bot, user)
        await up.refresh_single_user()
        await message


def setup(bot):
    bot.add_cog(Verify(bot))
