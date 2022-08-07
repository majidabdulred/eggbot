from datetime import datetime
import math
from discord import Embed
from discord.ext.commands import Cog, command
from discord_slash import ButtonStyle
from discord_slash.cog_ext import cog_slash
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component

import util.slash_options as op
from util import mylogs
import util.constants as C
from apis.chickenderby import get_chickens, get_chicken_race_history
from prettytable import PrettyTable
from models.model_get_chicken import Chicken

opensea_link = "https://opensea.io/assets/matic/0x8634666ba15ada4bbc83b9dbf285f73d9e46e4c2/"


class Token(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="token", aliases=["t", " t", " token"])
    async def degradred1(self, ctx):
        mylogs.debug(f"DEPRECATED_COMMAND : token :{ctx.author.name}")
        await ctx.reply("This command has been removed. Please use slash command.\n**/chicken**")

    @cog_slash(name="chicken", guild_ids=[C.serverid],
               description="Choose a chicken id",
               options=op.options_token)
    async def getslashtoken(self, ctx, tokenid: int):
        mylogs.info(f"COMMAND_USED : chicken : {tokenid} : {ctx.author.name} : {ctx.author.id}")
        res = GetChicken(ctx)
        await res.run(tokenid)


def setup(bot):
    bot.add_cog(Token(bot))


class GetChicken:
    def __init__(self, ctx):
        self.pre_ctx = ctx

    async def run(self, chickenid, hidden=False):
        await self.pre_ctx.defer(hidden=hidden)
        self.id = chickenid
        if not 1 <= self.id <= 33333:
            await self.pre_ctx.send(f"I couldn't find Chicken number {self.id} .")
            return
        response = await get_chickens([chickenid])
        if len(response) == 0:
            raise AssertionError
        self.data: Chicken = response[chickenid]
        embed, row = self.create_chicken_embed()
        await self.pre_ctx.send(embed=embed, components=[row])

    def create_chicken_embed(self) -> tuple:
        embed = Embed(title=self.data.name)
        embed.set_author(name=self.data.id)
        embed.set_image(url=self.data.image)

        embed.add_field(name="Heritage", value=self.data.heritage)
        embed.add_field(name="Perfection", value=self.data.perfection)
        embed.add_field(name="POP", value=self.data.poPoints)
        embed.add_field(name="Races", value=self.data.races)
        embed.add_field(name="Performance", value=self.data.performance)
        embed.add_field(name="Total Earnings", value=f"${self.data.earnings}")
        embed.add_field(name="Talent", value=self.data.talent)
        embed.add_field(name="Gender", value=self.data.gender)
        if self.data.beakAccessory:
            embed.add_field(name="BeakAccessory", value=self.data.beakAccessory)
        if self.data.stripes:
            embed.add_field(name="Stripes", value=self.data.stripes)
        buttons = []
        if self.data.races > 0:
            # buttons.append(create_button(style=ButtonStyle.blue, label="Race History", custom_id="view_race_history"))
            pass
        buttons.append(
            create_button(style=ButtonStyle.URL, label="View on Opensea", url=f"{opensea_link}{self.data.id}"))

        row = create_actionrow(*buttons)
        return embed, row


class ChickenRaces:
    def __init__(self, pre_ctx, id, raceCount):
        self.pre_ctx = pre_ctx
        self.id = id
        self.raceCount = raceCount
        self.embeds = []
        self.which_page = 0

    async def run(self):
        await self.pre_ctx.defer()
        self.results, count = await get_chicken_race_history(self.id, 1, 15)
        self.pages = math.ceil(count / 16)
        self.create_embed(self.results)
        self.which_page += 1
        self.main_ctx = await self.pre_ctx.send(embed=self.embeds[0][0], components=[self.embeds[0][1]])
        while True:
            react = await wait_for_component(self.pre_ctx.bot, self.main_ctx, timeout=180, check=self.check_author)
            mylogs.info(f"COMPONENT_USED : {react.custom_id} : {self.pre_ctx.author.name} : {self.pre_ctx.author_id}")
            await react.defer(edit_origin=True)
            if react.custom_id == "next_chicken_races":
                await self.load_next_page()
                self.which_page += 1
            elif react.custom_id == "prev_chicken_races":
                self.which_page -= 1
            print("Page", self.which_page)
            await react.edit_origin(embed=self.embeds[self.which_page - 1][0],
                                    components=[self.embeds[self.which_page - 1][1]])

    async def load_next_page(self):
        if len(self.embeds) > self.which_page or self.which_page >= self.pages:
            return

        result = await get_chicken_race_history(self.id, self.which_page + 1, 15)
        self.create_embed(result)

    def create_embed(self, results):
        embed = Embed(title="Title")
        tab = PrettyTable(["Id", "Dist.", "Terrain", "Rank", "P/L($)"])
        tab.align = "r"
        tab.align["Terrain"] = "l"
        tab.align["Id"] = "l"
        for race in results:
            raceid = race.get("id")
            date = datetime.strptime(race.get("startsAt"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d %b")
            distance = race.get("distance")
            terrain_list = {1: "Dirt", 2: "Grass", 3: "Road", 4: "Rock", 5: "Sand", 6: "Ice", 7: "Track"}
            terrain = terrain_list.get(race.get("terrainId"))
            pos, race_earn = self._calc_position(race)
            race_earnings = round(race_earn - race.get("feeUSD"), 2)
            if race_earnings == 0:
                race_earnings = f"0.00"
            elif race_earnings > 0:
                race_earnings = f"+{race_earnings}"
            if len(str(race_earnings).split(".")[-1]) == 1:
                race_earnings = f"{race_earnings}0"
            tab.add_row([raceid, distance, terrain, pos, race_earnings])
        buttons = []
        if self.pages > 1 and self.which_page >= 1:
            buttons.append(create_button(style=ButtonStyle.green, label="<", custom_id="prev_chicken_races"))
        if self.pages > 1 and self.which_page + 1 < self.pages:
            buttons.append(create_button(style=ButtonStyle.green, label=">", custom_id="next_chicken_races"))
        buttons.append(create_button(style=ButtonStyle.blue, label="Go Back", custom_id="go_back_chicken_races"))
        buttons.append(create_button(style=ButtonStyle.URL, label="KnowYourWallet",
                                     url=f"https://knowyourwallet.io/chicken_derby/chickens/{self.id}"))
        row = create_actionrow(*buttons)
        embed.add_field(name="Results", value=f"```\n{tab.get_string()}\n```")
        self.embeds.append((embed, row))

    def create_table(self, page):
        tab = PrettyTable(["Id", "Dist.", "Terrain", "Rank", "P/L($)"])
        tab.align = "r"
        tab.align["Terrain"] = "l"
        tab.align["Id"] = "l"
        _from = (page - 1) * 15
        _to = _from + 15
        for race in self.results[_from:_to]:
            raceid = race.get("id")
            date = datetime.strptime(race.get("startsAt"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d %b")
            distance = race.get("distance")
            terrain_list = {1: "Dirt", 2: "Grass", 3: "Road", 4: "Rock", 5: "Sand", 6: "Ice", 7: "Track"}
            terrain = terrain_list.get(race.get("terrainId"))
            pos, race_earn = self._calc_position(race)
            race_earnings = round(race_earn - race.get("feeUSD"), 2)
            if race_earnings == 0:
                race_earnings = f"0.00"
            elif race_earnings > 0:
                race_earnings = f"+{race_earnings}"
            if len(str(race_earnings).split(".")[-1]) == 1:
                race_earnings = f"{race_earnings}0"
            tab.add_row([raceid, distance, terrain, pos, race_earnings])
        return tab

    def _calc_position(self, race):
        if race.get("id") == 4240:
            for i, chick in enumerate(race.get("result").get("gameInfo").get("chickens")):
                if int(chick.get("info").get("tokenId")) == self.id:
                    race_earn = chick.get("info").get("race_earnings") if chick.get("info").get("race_earnings") else 0
                    return i + 1, race_earn

    def check_author(self, ctx):
        return self.pre_ctx.author_id == ctx.author_id
