import random

from discord import Embed
from discord_slash import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component

from db.local_db import submit_datadb
from tasks.process import delete_later


class ChangeWallet:
    def __init__(self, ctx, bot, user=None, new_wallet=False):
        self.main_ctx = ctx
        self.bot = bot
        self.user = user
        self.new_wallet = new_wallet

    async def run(self, react):
        embed, comps = self.create_embed()
        await react.send(embed=embed, components=[comps], hidden=True)
        delete_later((self.user.id, (self.main_ctx, self.user)), submit_datadb, minutes=10)
        react = await wait_for_component(self.bot, components=comps, check=self.check_author,
                                         timeout=180)
        react.custom_id = "go_back_verify"
        return react

    def check_author(self, ctx):
        return ctx.author_id == self.user.id

    def create_embed(self):
        prefix = "" if not self.new_wallet else \
            "You wallet is not Verified . Please follow this procedure to verify your wallet.\n"

        embed = Embed(
            description=f"{prefix}Click on **Connect** to connect your new wallet. It will take you to a "
                        "website starting with  `https://chickenderby.github.io` . \n"
                        "Click on **Connect Metamask** on the website to connect your wallet.\n\n",
            title="Connect Your Wallet")
        buttons = [
            create_button(style=ButtonStyle.URL, label="Connect",
                          url=f"https://chickenderby.github.io/verify/?{self.user.id}"),
            create_button(style=ButtonStyle.blue, label="Go back",
                          custom_id=str(random.randrange(1000000, 9999999)))]
        comps = create_actionrow(*buttons)

        return embed, comps


class NewWallet:
    def __init__(self, ctx, user=None):
        self.profile_ctx = ctx
        self.user = user

    async def run(self, react):
        embed, comps = self.create_embed()
        await react.reply(embed=embed, components=[comps], hidden=True)
        delete_later((self.user.id, (self.profile_ctx, self.user)), submit_datadb, minutes=10)

    def create_embed(self):
        prefix = "You wallet is not Verified . Please follow this procedure to verify your wallet.\n"

        embed = Embed(
            description=f"{prefix}Click on **Connect** to connect your new wallet. It will take you to a "
                        "website starting with  `https://chickenderby.github.io` . \n"
                        "Click on **Connect Metamask** on the website to connect your wallet.\n\n",
            title="Connect Your Wallet")
        buttons = [
            create_button(style=ButtonStyle.URL, label="Connect",
                          url=f"https://chickenderby.github.io/verify/?{self.user.id}")]
        comps = create_actionrow(*buttons)

        return embed, comps
