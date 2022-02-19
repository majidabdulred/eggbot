import asyncio
from discord.user import User

loop = asyncio.get_event_loop()
dm_tasks = []
from util.logs import mylogs


async def _delete_it_set(ele, from_set, after):
    await asyncio.sleep(after)
    try:
        from_set.remove(ele)
    except KeyError:
        mylogs.warning(f"VALUE_REMOVAL_ERROR : {ele} : {from_set}")


async def _delete_it_dict(key, from_set, after):
    await asyncio.sleep(after)
    try:
        from_set.pop(key)
    except KeyError:
        mylogs.warning(f"VALUE_REMOVAL_ERROR : {key} ")


def delete_later(ele, db, hours=0, minutes=0, seconds=0):
    secs = hours * 3600 + minutes * 60 + seconds
    if isinstance(db, set):
        db.add(ele)
        loop.create_task(_delete_it_set(ele, db, secs))
    elif isinstance(db, dict):
        db[ele[0]] = ele[1]
        loop.create_task(_delete_it_dict(ele[0], db, secs))


def send_dm(user, embed):
    dm_tasks.append({"user": user, "embed": embed})


async def _send_dm(dm_data):
    user: User = dm_data["user"]
    embed = dm_data["embed"]
    if user.dm_channel is None:
        await user.create_dm()
    await user.send(embed=embed)


async def run_dm_task():
    while True:
        dm_data = dm_tasks.pop(0)
        loop.create_task(_send_dm(dm_data))
        await asyncio.sleep(2)
