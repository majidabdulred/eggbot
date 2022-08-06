import asyncio
from discord import Embed
from discord_slash import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
import time
from db.local_db import server, scheduled_races
from util.logs import mylogs
from apis.chickenderby import get_scheduled_races

loop = asyncio.get_event_loop()


def time_dif(fg):
    m = time.strptime(fg, "%Y-%m-%dT%H:%M:%S.%fZ")
    k = time.mktime(m)
    now = time.mktime(time.gmtime())
    return k - now

def create_embed1(race):
    desc = f"**Order : ** {race.peckingOrder}\n" \
           f"**Distance : ** {race.distance}\n" \
           f"**Fee : ** ${race.feeUSD}\n" \
           f"**Prize Pool : ** ${race.prizePoolUSD}\n"
    embed = Embed(title=race.name, description=desc)
    for n, lane in enumerate(race.lanes):
        value = lane.userWallet.username if lane.userWallet.username else f"{lane.userWalletId[:8]}..."
        embed.add_field(name=f"Lane {n,+1}",value=value)
    buttons = [
        create_button(style=ButtonStyle.URL, label="Watch", url=f"https://play.chickenderby.com/?raceId={race['id']}"),
    ]
    linkbuttons = create_actionrow(*buttons)
    embed.set_author(name="RaceModel Started")
    return embed, linkbuttons


async def each_race(race):
    embed, comps = create_embed1(race)
    timeleft = time_dif(race["startsAt"])
    if timeleft <= 0:
        pass
    else:
        mylogs.info(f"RACE_ADDED : {race['id']} : {timeleft} secs")
        await asyncio.sleep(timeleft + 3)
    mylogs.info(f"RACE_SEND : {race['id']}")
    await server.race_started.send(embed=embed, components=[comps])


async def sch():
    results = await get_scheduled_races()
    for race in results.rows:
        if race.id not in scheduled_races:
            loop.create_task(each_race(race))
            scheduled_races.append(race.id)


async def race_scheduler(t):
    while True:
        loop.create_task(sch())
        await asyncio.sleep(t)
