import asyncio
from discord import Embed
from discord_slash import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
import time
from db.local_db import server, scheduled_races
from aiohttp import request
from db.users import get_user_from_chickens
from util.logs import mylogs
from apis.chickenderby import get_weth_price

loop = asyncio.get_event_loop()


def time_dif(fg):
    m = time.strptime(fg, "%Y-%m-%dT%H:%M:%S.%fZ")
    k = time.mktime(m)
    now = time.mktime(time.gmtime())
    return k - now


async def _make_call():
    API = "https://api.chickenderby.com/api/race/all-races-scheduled"
    async with request("GET", url=API) as res:
        if res.status != 200:
            raise ValueError("CHICKENDERBY_API_ERROR")
        results = await res.json()
        return results


def _filter_out_chicken_ids(race: dict) -> list:
    chicken_ids = []
    for lane in race["lanes"]:
        chicken_ids.append(int(lane["chickenId"]))
    return chicken_ids


def create_embed1(race: dict, users: list, wethprice):
    usd_fee = f"| ${round(race['fee'] * wethprice, 2)}" if wethprice else ""
    usd_prize = f"| ${round(race['prizePool'] * wethprice, 2)}" if wethprice else ""
    desc = f"**Order : ** {race['peckingOrder']}\n" \
           f"**Distance : ** {race['distance']}\n" \
           f"**Fee : ** Ξ{race['fee']} {usd_fee}\n" \
           f"**Prize Pool : ** Ξ{race['prizePool']} {usd_prize}\n"
    embed = Embed(title=race["name"], description=desc)
    hju = {}
    for lane in race['lanes']:
        for user in users:
            if (chkid := int(lane["chickenId"])) in user["accounts"][0]["chicks"]:
                hju[chkid] = user
                break
            else:
                hju[chkid] = None

    count = 0
    for chicks in hju.items():
        count += 1
        if chicks[1]:
            embed.add_field(name=f"Lane {count}", value=f"<@{chicks[1]['_id']}>\n")
    buttons = [
        create_button(style=ButtonStyle.URL, label="Watch", url=f"https://play.chickenderby.com/?raceId={race['id']}")]
    linkbuttons = create_actionrow(*buttons)
    embed.set_author(name="Race Started")
    return embed, linkbuttons


async def each_race(race):
    chicken_ids = _filter_out_chicken_ids(race)
    users = await get_user_from_chickens(chicken_ids)
    weth_price = await get_weth_price()
    embed, comps = create_embed1(race, users, weth_price)
    timeleft = time_dif(race["startsAt"])
    if timeleft <= 0:
        pass
    else:
        mylogs.info(f"RACE_ADDED : {race['id']} : {timeleft} secs")
        await asyncio.sleep(timeleft + 10)
    mylogs.info(f"RACE_SEND : {race['id']}")
    await server.race_started.send(embed=embed, components=[comps])


async def sch():
    results = await _make_call()
    for race in results["rows"]:
        if race["id"] not in scheduled_races:
            loop.create_task(each_race(race))
            scheduled_races.append(race["id"])


async def race_scheduler(t):
    while True:
        loop.create_task(sch())
        await asyncio.sleep(t)
