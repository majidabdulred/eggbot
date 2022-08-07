import asyncio

import aiohttp


class WethPrice:
    rate = 0.0


async def update_weth_price():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.chickenderby.com/api/coin-rates") as resp:
            data = await resp.json()
            WethPrice.rate = float(data["weth"])
    return float(data["weth"])


async def weth_price_scheduler():
    loop = asyncio.get_event_loop()
    while True:
        loop.create_task(update_weth_price())
        await asyncio.sleep(60)
