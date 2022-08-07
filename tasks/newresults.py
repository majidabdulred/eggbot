import asyncio
from apis.chickenderby import get_race_results
from discord import Embed
from discord_slash import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
from prettytable import PrettyTable
from db.local_db import server

from util import mylogs
from models.model_races_results import RowsModel
from db.cache import add_send_race, has_send

loop = asyncio.get_event_loop()


async def _task2(race):
    res = RaceResults(race)
    await res.run()


async def _task1():
    results = await get_race_results()
    for race in results.rows:
        if await has_send(race.raceId):
            continue
        loop.create_task(_task2(race))


async def scheduler_race_results(interval):
    while True:
        loop.create_task(_task1())
        await asyncio.sleep(interval)


class RaceResults:
    def __init__(self, race:RowsModel):
        self.results_channel = server.race_results
        self.model = race

    async def run(self):
        embed, comps = self.create_embed()
        main_ctx = await self.results_channel.send(embed=embed, components=[comps])
        res = await add_send_race(int(self.model.raceId))
        mylogs.info(f"RESULTS_SEND : {self.model.raceId}")
        if not res:
            await main_ctx.delete()

    def create_embed(self):
        tab = PrettyTable(["Pos", "Name", "Owner"])
        for i, chick in enumerate(self.model.chickens):
            tab.add_row([i + 1, chick.name, chick.owner])
        tab.align = "l"
        race = self.model.race
        embed = Embed(title=race.name, description=f"")
        embed.add_field(name="Time", value=race.startsAt)
        embed.add_field(name="Pecking Order", value=race.peckingOrder)
        embed.add_field(name="Distance(m)", value=race.distance)
        embed.add_field(name="Fee", value=f"${race.feeUSD}")
        embed.add_field(name="PrizePool", value=f"${race.prizePoolUSD}")
        embed.add_field(name="Venue", value=race.location)
        embed.add_field(name="First", value=f"${self.model.chickens[0].raceEarnings}")
        embed.add_field(name="Second", value=f"${self.model.chickens[1].raceEarnings}")
        embed.add_field(name="Third", value=f"${self.model.chickens[2].raceEarnings}")
        embed.set_author(name=race.id)
        embed.add_field(name="Results", value=f"```\n{tab.get_string()}\n```", inline=False)
        buttons = [
            create_button(style=ButtonStyle.blue, label="Chickens", custom_id=f"results_chickens_{race.id}"),
            create_button(style=ButtonStyle.URL, label="Watch",
                          url=f"https://play.chickenderby.com/?raceId={race.id}")]
        row = create_actionrow(*buttons)

        return embed, row