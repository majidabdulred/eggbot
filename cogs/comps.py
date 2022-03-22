from .race import Race

from apis.chickenderby import get_race_data

from discord import Embed
from discord_slash import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component

from db.users import get_user, set_notify_race_started
from util.logs import mylogs


# discord.errors.HTTPException: 400 Bad Request (error code: 40060): Interaction has already been acknowledged.

async def handle_component(ctx):
    mylogs.info(f"COMPONENTS_USED : {ctx.custom_id} : {ctx.author.name} : {ctx.author_id}")
    if ctx.custom_id.startswith("results_chickens_"):
        await _handle_component_results(ctx)
    elif ctx.custom_id == "notification_race_started":
        await _handle_component_race_started(ctx)


async def _handle_component_race_started(ctx):
    res = NotifyRaceStarted(ctx)
    await res.run()


async def _handle_component_results(ctx):
    raceid = int(ctx.custom_id.lstrip("results_chickens_"))
    if not raceid: raise ArithmeticError
    race = HandleComponentChickens(ctx)
    await race.run(raceid)


class HandleComponentChickens(Race):
    def __init__(self, ctx):
        super().__init__(ctx)

    async def run(self, raceid):
        self.raceid = raceid
        await self.pre_ctx.defer(hidden=True)
        data = await get_race_data(raceid)
        if not data:
            await self.pre_ctx.send(f"Something went wrong", hidden=True)
            return
        self.init_race_data(data)
        del data
        embed, comps = self.create_embed()
        react = await self.chicken_paginating(self.pre_ctx)
        await react.edit_origin(embed=embed, components=[comps], hidden=True)
        while True:
            react = await wait_for_component(self.pre_ctx.bot, components=[comps], timeout=180, check=self.check_author)
            mylogs.debug(f"COMPONENT_USED : {react.custom_id} : {self.pre_ctx.author.name}")
            if react.custom_id == "chickens":
                react = await self.chicken_paginating(react, second_time=True)
            mylogs.debug(f"COMPONENT_USED : {react.custom_id} : {self.pre_ctx.author.name}")
            await react.edit_origin(embed=embed, components=[comps], hidden=True)

    async def chicken_paginating(self, react, second_time=False):
        if not self.chicken_embeds:
            self.chicken_embeds = self.create_chickens_embeds()
        page = 0
        if second_time:
            await react.defer(edit_origin=True)
            await react.edit_origin(embed=self.chicken_embeds[page][0], components=[self.chicken_embeds[page][1]],
                                    hidden=True)
        else:
            await react.send(embed=self.chicken_embeds[page][0], components=[self.chicken_embeds[page][1]], hidden=True)

        while True:
            react = await wait_for_component(self.pre_ctx.bot, components=[self.chicken_embeds[page][1]], timeout=180,
                                             check=self.check_author)
            await react.defer(edit_origin=True)
            if react.custom_id == "next_pag":
                page += 1
                if page >= len(self.chicken_embeds):
                    page = 0
            elif react.custom_id == "prev_pag":
                page -= 1
                if page < 0:
                    page = len(self.chicken_embeds) - 1
            elif react.custom_id == "go_back_chickens":
                return react

            await react.edit_origin(embed=self.chicken_embeds[page][0], components=[self.chicken_embeds[page][1]],
                                    hidden=True)


class NotifyRaceStarted:
    def __init__(self, ctx):
        self.userid = ctx.author_id
        self.pre_ctx = ctx

    async def run(self):
        await self.pre_ctx.defer(hidden=True)
        userdb = await get_user(self.userid)
        if not userdb:
            return
        if userdb.get("notify_race_started") in (None, True):
            await self.turn_off()
        else:
            await self.turn_on()

    async def turn_off(self):

        row = create_actionrow(create_button(style=ButtonStyle.red, label="Turn off", custom_id="turn_off_started"))
        embed = Embed(title="Notification Settings",
                      description="Your notification is **ON**.\n"
                                  "Click on **Turn off** to turn off your notification and you wont be pinged whenever "
                                  "a race with your chicken is started")
        embed.set_footer(text="Click on dismiss message to cancel")
        await self.pre_ctx.send(embed=embed, components=[row], hidden=True)
        react = await wait_for_component(self.pre_ctx.bot, components=[row], timeout=180, check=self.check_author)
        if react.custom_id == "turn_off_started":
            await react.defer(edit_origin=True)
            await set_notify_race_started(self.userid, False)
            embed = Embed(title="Successful",
                          description="Your notifications has been turned off.")
            await react.edit_origin(embed=embed, components=[], hidden=True)

    async def turn_on(self):
        row = create_actionrow(create_button(style=ButtonStyle.green, label="Turn On", custom_id="turn_on_started"))
        embed = Embed(title="Notification Settings",
                      description="Your notification is **OFF**.\n"
                                  "Click on **Turn On** to turn on your notification and you will be pinged whenever "
                                  "a race with your chicken is started")
        embed.set_footer(text="Click on dismiss message to cancel")
        await self.pre_ctx.send(embed=embed, components=[row], hidden=True)
        react = await wait_for_component(self.pre_ctx.bot, components=[row], timeout=180, check=self.check_author)
        if react.custom_id == "turn_on_started":
            await react.defer(edit_origin=True)
            await set_notify_race_started(self.userid, True)
            embed = Embed(title="Successful",
                          description="Your notifications has been turned on.")
            await react.edit_origin(embed=embed, components=[], hidden=True)

    def check_author(self, ctx):
        return self.userid == ctx.author_id
