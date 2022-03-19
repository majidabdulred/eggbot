import asyncio
from apis.chickenderby import get_race_results
from discord import Embed
from discord_slash import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
from prettytable import PrettyTable
from datetime import datetime

from util import mylogs
from util.models import RacedChicken
from db.local_db import server
from db.cache import add_send_race, has_send

loop = asyncio.get_event_loop()


async def _task2(race):
    res = RaceResults(data=race)
    await res.run()


async def _task1():
    results = await get_race_results()
    races = results["rows"]
    for race in races:
        if await has_send(race.get('race').get("id")):
            continue
        loop.create_task(_task2(race))


async def scheduler_race_results(interval):
    while True:
        loop.create_task(_task1())
        await asyncio.sleep(interval)


class RaceResults:
    def __init__(self, data):
        self.results_channel = server.race_results
        self.chickens = []
        for chick in data["gameInfo"]["chickens"]:
            self.chickens.append(RacedChicken(chick))
        info = data.get("race")
        self.id = info.get("id")
        self.race_name = info.get("name")
        self.peckingOrder = info.get("peckingOrder")
        self.distance = info.get("distance")
        self.feeEth = info.get("fee")
        self.feeUSD = info.get("feeUSD")
        self.prizeEth = info.get("prizePool")
        self.prizeUSD = info.get("prizePoolUSD")
        self.location = info.get("location")

        self.startedAt = datetime.strptime(info.get("startsAt"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d %b %H:%M UTC")

    async def run(self):
        embed, comps = self.create_embed()
        main_ctx = await self.results_channel.send(embed=embed, components=[comps])
        res = await add_send_race(int(self.id))
        mylogs.info(f"RESULTS_SEND : {self.id}")
        if not res:
            await main_ctx.delete()

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
        embed.set_author(name=self.id)
        embed.add_field(name="Results", value=f"```\n{tab.get_string()}\n```", inline=False)
        buttons = [
            create_button(style=ButtonStyle.blue, label="Chickens", custom_id=f"results_chickens_{self.id}"),
            create_button(style=ButtonStyle.URL, label="Watch",
                          url=f"https://play.chickenderby.com/?raceId={self.id}")]
        row = create_actionrow(*buttons)

        return embed, row
