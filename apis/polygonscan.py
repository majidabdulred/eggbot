import asyncio
from os import getenv

from aiohttp import request

from util import mylogs

from dotenv import load_dotenv

load_dotenv()


async def get_previous_sales(address):
    url = "https://api.polygonscan.com/api"
    params = {"module": "account",
              "action": "tokennfttx",
              "contractaddress": "0x8634666ba15ada4bbc83b9dbf285f73d9e46e4c2",
              "page": 1,
              "offset": 100,
              "sort": "desc",
              "apikey": getenv("POLYGONSCAN_API_KEY"),
              "address": address}
    async with request(method="GET", params=params,
                       url=url) as re:
        if re.status != 200:
            mylogs.error(f"POLYGONSCAN_ERROR : {address}")
            return None
        result = (await re.json())["result"]
        for ki in range(len(result)):
            result[ki]["srno"] = ki + 1
        return result


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_previous_sales("0x74f90dbb59e9b8c4dfa0601cd303cb11e9fa4a78"))
