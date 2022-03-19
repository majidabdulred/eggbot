from .race import Race
from discord import Embed
from discord.ext.commands import Cog
from discord_slash import ButtonStyle
from discord_slash.cog_ext import cog_slash
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from prettytable import PrettyTable
from datetime import datetime
from apis.chickenderby import get_race_data
from util.constants import serverid
from discord_slash.utils.manage_commands import create_option
from util import mylogs
from util.models import RacedChicken


# discord.errors.HTTPException: 400 Bad Request (error code: 40060): Interaction has already been acknowledged.

async def handle_component(ctx):
    print(ctx.custom_id)
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
