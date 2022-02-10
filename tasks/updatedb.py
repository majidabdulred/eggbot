"""
Updates the User data fields chicks for every user.
"""
import asyncio

from db.mydb import db
from apis import get_chickens
from db.users import add_chickens
from util import mylogs
from datetime import datetime, timedelta

col = db.get_collection("test")


def _parse_chickids(chicks_raw):
    """Takes a list of opensea chicken response and provides chickens ids in a list :int"""
    chicks = [int(i["token_id"]) for i in chicks_raw]
    return chicks


async def _update_user(user):
    for acc in user["accounts"]:
        mylogs.debug(f"Address {acc['address']}")
        chickens = await get_chickens(acc["address"])
        chickens = _parse_chickids(chickens)
        await add_chickens(acc["address"], chickens)
        mylogs.debug(f"Finished one: {chickens}")


async def main_updater():
    two_hours_ago = datetime.utcnow() - timedelta(hours=10)
    users = col.find({"updatedAt": {"$lt": two_hours_ago}})
    total = await col.count_documents({"updatedAt": {"$lt": two_hours_ago}})
    count = 1
    async for user in users:
        print(user["updatedAt"])
        mylogs.debug(f"{count}/{total}")
        loop = asyncio.get_event_loop()
        loop.create_task(_update_user(user))
        count += 1
        await asyncio.sleep(1)
