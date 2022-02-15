from discord.ext.commands import Cog, command
from discord_slash.cog_ext import cog_component
from util import create_embeds
from db import users as Users
from db.local_db import verify_messages
from util.constants import submit_data_channel
from db import server
from util.logs import mylogs


class Verify(Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_component()
    async def no_thanks(self, ctx):
        mylogs.debug(f"COMPONENT_USED : no_thanks : {ctx.author_id} : {ctx.author.name}")
        await ctx.send(f"No Problem.\nYou can visit <#{server.leaderboard.id}> to know more.", hidden=True)
        del verify_messages[ctx.author_id]

    @cog_component()
    async def change_wallet(self, ctx):
        mylogs.debug(f"COMPONENT_USED : change_wallet : {ctx.author_id} : {ctx.author.name}")
        if ctx.author_id not in verify_messages.keys():
            mylogs.warning(f"VERIFY_MESSAGE_NOT_FOUND : {ctx.author_id.id} : {ctx.author.name} : change_wallet")
            return
        await ctx.defer(hidden=True)
        user = await Users.get_user(ctx.author_id)
        address = user.get("accounts")[0].get("address")
        verify_messages[ctx.author_id]["to_delete"] = True
        verify_messages[ctx.author_id]["delete_address"] = address
        embed, buttons = create_embeds.wallet_connect_message_2(ctx.author_id)
        await ctx.send(embed=embed, components=[buttons], hidden=True)
        verify_messages[ctx.author_id]["ctx_submitdata"] = ctx

    @command(name="submitdata")
    async def submitdata(self, ctx, link: str, address: str):
        uid = link.lstrip("https://chickenderby.github.io/verify/?")
        mylogs.debug(f"SUBMITDATA : {uid} : {address}")
        if ctx.channel.id != submit_data_channel:
            return
        if uid == "" or not uid.isdigit():
            return
        elif int(uid) not in verify_messages.keys():
            return
        userid = int(uid)
        user = verify_messages[userid]
        if user.get("mode") == "new":
            await Users.save_user(userid, address)
        elif user.get("mode") == "change":
            await Users.add_address(userid, address, [])
            if user.get("to_delete") and user.get("delete_address") != address:
                await Users.remove_address(userid, user.get("delete_address"))
        else:
            return
        if (ctx_submitdata := user.get("ctx_submitdata")) is not None:
            mylogs.debug(
                f"SUCCESS : submitdata : {ctx_submitdata.author_id} : {ctx_submitdata.author.name} : {user.get('to_delete')} => {address}")
            await ctx_submitdata.send(f"<@{userid}> your wallet verification is complete. Your address is `{address}`",
                                      hidden=True)
        else:
            await server.robot_channel.send(f"<@{userid}> your wallet verification is complete.")
        del verify_messages[userid]

        # Beta Deprecated
        # if "beta" in user.keys() and user["beta"]:
        #     await self.add_user_to_beta(user["user_ctx"])

    # Beta Deprecated
    # async def add_user_to_beta(self, user):
    #     await Users.set_user_beta_to(user.id, True)
    #     await server.robot_channel.send(f"<@{user.id}> You have been added to beta list.")
    #
    #     await user._add_role(*[server.beta_role])

    # Beta Deprecated
    # @cog_component()
    # async def add_to_beta(self, ctx):
    #     if ctx.author_id not in verify_messages.keys():
    #         return
    #     await ctx.defer()
    #     await Users.set_user_beta_to(ctx.author_id, True)
    #     await ctx.send("You have been Successfully Added to the beta", hidden=True)
    #     await ctx.author._add_role(*[server.beta_role])
    #     del verify_messages[ctx.author_id]
    #     await ctx.origin_message.delete()
    #     print(1)

    # Beta Deprecated
    # @cog_component()
    # async def remove_from_beta(self, ctx):
    #     if ctx.author_id not in verify_messages.keys():
    #         return
    #     await ctx.defer()
    #     await Users.set_user_beta_to(ctx.author_id, False)
    #     await ctx.send("You have been successfully removed from beta list", hidden=True)
    #     await ctx.author.remove_roles(*[server.beta_role])
    #     del verify_messages[ctx.author_id]

    # Beta Deprecated
    # @cog_component()
    # async def enroll(self, ctx):
    #     await ctx.defer(hidden=True)
    #     print(ctx.author_id)
    #     verify_messages[ctx.author_id] = {}
    #     verify_messages[ctx.author_id]["user_ctx"] = ctx.author
    #     user = await Users.get_user(ctx.author_id)
    #     if user is None or len(user["accounts"]) <= 0:
    #         embed, buttons = create_embeds.wallet_connect_message(ctx.author_id)
    #         await ctx.send(embed=embed, components=[buttons], hidden=True)
    #         return
    #     if "beta" in user.keys() and user["beta"]:
    #         embed, buttons = create_embeds.already_have_your_wallet_and_in_beta(user["accounts"][0]["address"])
    #     else:
    #         embed, buttons = create_embeds.already_have_your_wallet(user["accounts"][0]["address"])
    #     print(await ctx.bot.application_info())
    #     await ctx.send(embed=embed, components=[buttons], hidden=True)


# 	0xf13f7bf69a5e57ea3367222c65dd3380096d3fbf

def setup(bot):
    bot.add_cog(Verify(bot))
