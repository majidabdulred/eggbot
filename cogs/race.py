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
options_race = [
    create_option(
        name="raceid",
        description="ID of the Race",
        option_type=4,
        required=True)]
opensea_link = "https://opensea.io/assets/matic/0x8634666ba15ada4bbc83b9dbf285f73d9e46e4c2/"


class RaceChickens(Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_slash(name="race", guild_ids=[serverid], options=options_race)
    async def chicks(self, ctx, raceid: int):
        mylogs.info(f"COMMAND_USED : race : {ctx.author.name} : {raceid}")
        race = Race(ctx)
        await race.run(raceid)


def setup(bot):
    bot.add_cog(RaceChickens(bot))


class Race:
    def __init__(self, ctx):
        self.pre_ctx = ctx
        self.chickens = []
        self.chicken_embeds = None

    async def run(self, raceid):
        self.raceid = raceid
        await self.pre_ctx.defer()
        data = await get_race_data(raceid)
        if not data:
            await self.pre_ctx.send(f"Raceid {self.raceid} doesnt exists")
            return
        self.init_race_data(data)
        del data
        embed, comps = self.create_embed()
        self.main_ctx = await self.pre_ctx.send(f"{self.pre_ctx.author.mention}", embed=embed, components=[comps])
        while True:
            react = await wait_for_component(self.pre_ctx.bot, self.main_ctx, timeout=180, check=self.check_author)
            mylogs.debug(f"COMPONENT_USED : {react.custom_id} : {self.pre_ctx.author.name}")
            if react.custom_id == "chickens":
                react = await self.chicken_paginating(react)
            mylogs.debug(f"COMPONENT_USED : {react.custom_id} : {self.pre_ctx.author.name}")
            await react.edit_origin(embed=embed, components=[comps])

    async def chicken_paginating(self, react):
        if not self.chicken_embeds:
            self.chicken_embeds = self.create_chickens_embeds()
        page = 0
        await react.edit_origin(embed=self.chicken_embeds[page][0], components=[self.chicken_embeds[page][1]])
        while True:
            react = await wait_for_component(self.pre_ctx.bot, self.main_ctx, timeout=180, check=self.check_author)
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

            await react.edit_origin(embed=self.chicken_embeds[page][0], components=[self.chicken_embeds[page][1]])

    def create_chickens_embeds(self) -> list:
        embeds = []

        for i, chick in enumerate(self.chickens):
            embed = Embed(title=chick.name)
            embed.set_author(name=self.id)
            embed.set_image(url=chick.image)
            embed.add_field(name="Position", value=f"{i + 1}")
            embed.add_field(name="Time", value=f"{chick.race_timing}s")
            embed.add_field(name="Prize", value=f"${chick.this_race_earnings}")
            embed.add_field(name="Heritage", value=chick.heritage)
            embed.add_field(name="Perfection", value=chick.perfection)
            embed.add_field(name="POP", value=chick.POP)
            embed.add_field(name="Races", value=chick.races)
            embed.add_field(name="Performance", value=chick.performance)
            embed.add_field(name="Total Earnings", value=f"${chick.total_earnings}")
            embed.add_field(name="Owner", value=chick.owner_full_name)
            buttons = [create_button(style=ButtonStyle.green, label="<", custom_id="prev_pag"),
                       create_button(style=ButtonStyle.green, label=">", custom_id="next_pag"),
                       create_button(style=ButtonStyle.blue, label="Go Back", custom_id="go_back_chickens"),
                       create_button(style=ButtonStyle.URL, label="View on Opensea", url=f"{opensea_link}{chick.id}")
                       ]
            row = create_actionrow(*buttons)
            embeds.append((embed, row))
        return embeds

    def create_embed(self):
        tab = PrettyTable(["Pos", "Name", "Owner", "Time(s)"])
        for i, chick in enumerate(self.chickens):
            tab.add_row([i + 1, chick.name, chick.owner, chick.race_timing])
        tab.align = "l"
        embed = Embed(title=self.race_name, description=f"")
        embed.add_field(name="Time", value=self.startedAt)
        embed.add_field(name="Pecking Order", value=self.peckingOrder)
        embed.add_field(name="Distance(m)", value=self.distance)
        embed.add_field(name="Fee", value=f"${self.feeUSD}")
        embed.add_field(name="PrizePool", value=f"${self.prizeUSD}")
        embed.add_field(name="Venue", value=self.location)
        embed.add_field(name="First", value=f"${self.chickens[0].this_race_earnings}")
        embed.add_field(name="Second", value=f"${self.chickens[1].this_race_earnings}")
        embed.add_field(name="Third", value=f"${self.chickens[2].this_race_earnings}")
        embed.set_author(name=self.raceid)
        embed.add_field(name="Results", value=f"```\n{tab.get_string()}\n```", inline=False)

        buttons = [
            create_button(style=ButtonStyle.blue, label="Chickens", custom_id="chickens"),
            create_button(style=ButtonStyle.URL, label="Watch",
                          url=f"https://play.chickenderby.com/?raceId={self.raceid}")]
        row = create_actionrow(*buttons)

        return embed, row

    def init_race_data(self, data):
        for chick in data["result"]["chickens"]:
            self.chickens.append(RacedChicken(chick))
        self.id = data.get("id")
        self.race_name = data.get("name")
        self.peckingOrder = data.get("peckingOrder")
        self.distance = data.get("distance")
        self.feeEth = data.get("fee")
        self.feeUSD = data.get("feeUSD")
        self.prizeEth = data.get("prizePool")
        self.prizeUSD = data.get("prizePoolUSD")
        self.location = data.get("location")

        self.startedAt = datetime.strptime(data.get("startsAt"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d %b %H:%M UTC")

    def check_author(self, ctx):
        return ctx.author_id == self.pre_ctx.author_id
