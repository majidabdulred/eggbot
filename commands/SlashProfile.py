from discord_slash import ButtonStyle
from discord.embeds import Embed
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component

from db.users import get_user
from commands.refresh_role import UpdateUser
from .tokensales import Transactions
from util.create_embeds import create_change_wallet_button
from db.local_db import refresh_timer
from tasks.process import delete_later
from .wallet import ChangeWallet, NewWallet


class SlashProfile:

    def __init__(self, ctx):
        self.profile_ctx = ctx
        self.user = ctx.author
        self.bot = self.profile_ctx.bot
        self.main_embed = Embed.Empty
        self.main_comps = None

    async def run(self):
        await self.profile_ctx.defer()
        await self.refresh_instance_data()
        if not self.userdb:
            return
        self.main_ctx = await self.profile_ctx.send(embed=self.main_embed, components=[*self.main_comps])
        while True:
            react = await wait_for_component(self.bot, self.main_ctx, timeout=180, check=self.check_author)
            if react.custom_id == "go_back_profile":
                await self.main_ctx.edit(components=[])
            elif react.custom_id == "refresh_profile":
                react = await self.handle_refresh(react)
            elif react.custom_id == "prev_trans":
                trans_event = Transactions(react, self.bot, address=self.address)
                react = await trans_event.run()
            elif react.custom_id == "change_wallet":
                change = ChangeWallet(self.main_ctx, self.bot, self.user)
                react = await change.run(react)
            else:
                return

            if react.custom_id == "go_back_token_sales":
                await react.edit_origin(embed=self.main_embed, components=[*self.main_comps])
            elif react.custom_id == "go_back_refresh":
                await react.defer(edit_origin=True)
                await self.refresh_instance_data()
                await react.edit_origin(embed=self.main_embed, components=[*self.main_comps])
            elif react.custom_id == "go_back_verify":
                self.main_ctx = await react.send(embed=self.main_embed, components=[*self.main_comps])
            else:
                return

    async def handle_refresh(self, react):
        await react.defer(edit_origin=True)

        await self.update_user.refresh_single_user()
        delete_later(self.user.id, refresh_timer, hours=10)
        if not self.update_user.changed:
            str_to_send = f"Your data is up to date.{self.update_user.total_score_str}\n" \
                          f"{self.update_user.already_have_role}\n{self.update_user.wallet_str}.\n{self.update_user.chickens_str}."
        else:
            str_to_send = f"{self.update_user.total_score_str}\n{self.update_user.wallet_str}.\n" \
                          f"{self.update_user.chickens_str}.\n{self.update_user.changed_str}"
        embed, comps = create_change_wallet_button(str_to_send)
        await self.main_ctx.edit(embed=embed, components=[comps])
        react = await wait_for_component(self.bot, self.main_ctx, timeout=180, check=self.check_author)
        if react.custom_id == "change_wallet":
            change = ChangeWallet(self.main_ctx, self.bot, self.user)
            react = await change.run(react)
        return react

    async def _create_profile_embed(self):
        description = ""
        await self.update_user.get_profile_info(self.userdb)
        user = self.update_user
        description += f"\n\n**Address** :\n`{self.address[:12] + '...'}`\n\n"
        chicks = "You don't have any chickens.\n\n" if user.chickens_str0 == "" else user.chickens_str0 + "\n\n"
        description += f"**Chickens** :\n {chicks}"
        description += f"**Points**   :\n  {user.total_score}\n"
        embed = Embed(title="User Information", description=description)
        embed.set_footer(text=
                         f"Refresh : To refresh your data if doesnt seems correct.(limited 1 refresh per hour)\n" \
                         f"Transaction : See your Chicken Derby NFT Transfers and Sales.\n"
                         f"Change Wallet : Change your wallet if you have moved your chickens to another wallet.")
        button1 = [
            create_button(style=ButtonStyle.green, label="Refresh", custom_id="refresh_profile",
                          disabled=True if self.user.id in refresh_timer else False),
            create_button(style=ButtonStyle.green, label="Transaction", custom_id="prev_trans"),
            create_button(style=ButtonStyle.green, label="Change Wallet", custom_id="change_wallet")]
        button2 = [
            create_button(style=ButtonStyle.blue, label="Go Back", custom_id="go_back_profile"),
            create_button(style=ButtonStyle.URL, label="View on Opensea",
                          url=f"https://opensea.io/{self.address}/chicken-derby?search[sortBy]=LISTING_DATE")]

        row1 = create_actionrow(*button1)
        row2 = create_actionrow(*button2)
        return embed, (row1, row2)

    async def new_wallet_registration(self):
        embed = Embed(title="Wallet verification",
                      description="Your wallet is not verified.\nClick on Start to start get the verification link.")
        button = [create_button(style=ButtonStyle.green, label="Start", custom_id="start")]
        row = create_actionrow(*button)

        start_message = await self.profile_ctx.reply(embed=embed, components=[row])
        react = await wait_for_component(self.bot, start_message, timeout=180, check=self.check_author)
        if react.custom_id == "start":
            await react.defer(hidden=True)
            new = NewWallet(start_message, self.user)
            await new.run(react)

    async def refresh_instance_data(self):
        self.userdb = await get_user(self.user.id)
        if not self.userdb:
            await self.new_wallet_registration()
            return
        self.update_user = UpdateUser(self.bot, self.user)
        self.address = self.userdb["accounts"][0]["address"]
        self.main_embed, self.main_comps = await self._create_profile_embed()

    def check_author(self, ctx):
        return ctx.author_id == self.user.id
