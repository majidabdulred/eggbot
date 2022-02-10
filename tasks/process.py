import asyncio
from discord.user import User

loop = asyncio.get_event_loop()
dm_tasks = []


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
