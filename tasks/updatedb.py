"""
Updates the User data fields chicks for every user.
"""
import asyncio

from db.mydb import db
from apis import get_chickens
from db.users import set_chickens
from util import mylogs
from datetime import datetime, timedelta

col = db.get_collection("test")

mylogs.setLevel("DEBUG")


def _parse_chickids(chicks_raw):
    """Takes a list of opensea chicken response and provides chickens ids in a list :int"""
    chicks = [int(i["token_id"]) for i in chicks_raw]
    return chicks


async def _update_user(user):
    for acc in user["accounts"]:
        mylogs.debug(f"Address {acc['address']}")
        chickens = await get_chickens(acc["address"])
        chickens = _parse_chickids(chickens)
        await set_chickens(acc["address"], chickens)
        mylogs.debug(f"Finished one: {chickens}")


async def main_updater(last_refresh_time):
    hours_ago = datetime.utcnow() - timedelta(hours=last_refresh_time)
    users = col.find({"updatedAt": {"$lt": hours_ago}})
    total = await col.count_documents({"updatedAt": {"$lt": hours_ago}})
    count = 1
    async for user in users:
        mylogs.debug(f"{count}/{total}")
        loop = asyncio.get_event_loop()
        loop.create_task(_update_user(user))
        count += 1
        await asyncio.sleep(1)


async def main_update_chicks_one(userdb):
    await _update_user(userdb)
