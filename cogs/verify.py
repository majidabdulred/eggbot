from discord.ext.commands import Cog, command
from discord_slash.cog_ext import cog_component
from util import create_embeds
from db import users as Users
from db.local_db import verify_messages

from db import server


class Verify(Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_component()
    async def verify(self, ctx):
        print("Verify")
        embed, buttons = create_embeds.wallet_connect_message(ctx.author_id)
        await ctx.send(embed=embed, components=[buttons], hidden=True)

    @cog_component()
    async def add_to_beta(self, ctx):
        if ctx.author_id not in verify_messages.keys():
            return
        await Users.set_user_beta_to(ctx.author_id, True)
        await ctx.send("You have been Successfully Added to the beta", hidden=True)
        await ctx.author.add_roles(*[server.beta_role])
        del verify_messages[ctx.author_id]

    @cog_component()
    async def remove_from_beta(self, ctx):
        if ctx.author_id not in verify_messages.keys():
            return
        await Users.set_user_beta_to(ctx.author_id, False)
        await ctx.send("You have been successfully removed from beta list", hidden=True)
        await ctx.author.remove_roles(*[server.beta_role])
        del verify_messages[ctx.author_id]

    @cog_component()
    async def change_wallet(self, ctx):
        if ctx.author_id not in verify_messages.keys():
            return
        user = await Users.get_user(ctx.author_id)
        address = user["accounts"][0]["address"]
        verify_messages[ctx.author_id]["to_delete"] = True
        verify_messages[ctx.author_id]["delete_address"] = address
        embed, buttons = create_embeds.wallet_connect_message_2(ctx.author_id)
        message = await ctx.send(embed=embed, components=[buttons], hidden=True)

    @cog_component()
    async def enroll(self, ctx):
        print(ctx.author_id)
        verify_messages[ctx.author_id] = {}
        verify_messages[ctx.author_id]["user_ctx"] = ctx.author
        user = await Users.get_user(ctx.author_id)
        if user is None or len(user["accounts"]) <= 0:
            embed, buttons = create_embeds.wallet_connect_message(ctx.author_id)
            await ctx.send(embed=embed, components=[buttons], hidden=True)
            return
        if "beta" in user.keys() and user["beta"]:
            embed, buttons = create_embeds.already_have_your_wallet_and_in_beta(user["accounts"][0]["address"])
        else:
            embed, buttons = create_embeds.already_have_your_wallet(user["accounts"][0]["address"])

        await ctx.send(embed=embed, components=[buttons], hidden=True)

    @command(name="submitdata")
    async def submitdata(self, ctx, link: str, address: str):
        if ctx.channel.id != 941032417941135371:
            return
        uid = link.lstrip("https://chickenderby.github.io/verify/?")
        if uid == "" or not uid.isdigit():
            return
        elif int(uid) not in verify_messages.keys():
            return
        userid = int(uid)
        user = verify_messages[userid]
        if user["mode"] == "new":
            await Users.save_user(userid, address)
        elif user["mode"] == "change":
            await Users.add_address(userid, address, [])
            if "to_delete" in user.keys() and user["to_delete"] and user["delete_address"] != address:
                await Users.remove_address(userid, user["delete_address"])
        else:
            return
        await server.robot_channel.send(f"<@{userid}> your wallet verification is complete.")
        # Remove this after beta verification
        if user["beta"]:
            await self.add_user_to_beta(user["user_ctx"])
        del verify_messages[userid]

    async def add_user_to_beta(self, user):
        await Users.set_user_beta_to(user.id, True)
        await server.robot_channel.send(f"<@{user.id}> You have been added to beta list.")

        await user.add_roles(*[server.beta_role])


def setup(bot):
    bot.add_cog(Verify(bot))
