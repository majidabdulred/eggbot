import asyncio
from os import getenv
from util import mylogs
from aiohttp import request, ServerDisconnectedError
from dotenv import load_dotenv

OPENSEA_API = "http://api.opensea.io/api/v2/assets/matic?"

load_dotenv()
header = {"X_API_KEY": getenv("X_API_KEY")}


def _verify_results(chicks: list):
    response = []
    """Verifies that only chicken-derby nfts are in the response. Takes a list and returns a list"""
    for ch in chicks:
        if ch["asset_contract"]["address"] == "0x8634666ba15ada4bbc83b9dbf285f73d9e46e4c2":
            response.append(ch)
    return response


async def _get_chickens_1(address):
    async with request(method="GET", headers=header,
                       url=f"{OPENSEA_API}asset_contract=0x8634666ba15ada4bbc83b9dbf285f73d9e46e4c2&owner_address={address}") as re:
        if re.status != 200:
            mylogs.error(f"Opesea response error . {re.url} {re.status}")
            return None
        data = await re.json()
        if re.status != 200:

            if "does not exist for chain matic" in data[0]:
                mylogs.warning("Address does not exists in matic chain")
        return data


async def _get_next(url):
    params = url.split("?")[1]
    url = OPENSEA_API + params
    async with request(method="GET", headers=header, url=url) as re:
        data = await re.json()
        if re.status != 200:
            raise ValueError("CluckNorris")
        return data


async def get_chickens(address):
    """Returns list of chickens with ids"""
    count = 0
    results = []
    data = await _get_chickens_1(address)
    if data is None:
        return []
    results += _verify_results(data["results"])
    while True:
        count += 1
        if data['next'] is None or count >= 40:
            mylogs.debug(f"Total {len(results)}")
            break
        try:
            mylogs.debug(f"Next {len(results)}")
            data = await _get_next(data['next'])
        except ServerDisconnectedError:
            mylogs.error("Server Disconnection Error")
            await asyncio.sleep(1)
        results += _verify_results(data["results"])
    return results


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    mylogs.info("Getting the chickens")
    loop.run_until_complete(get_chickens("0x46c779dfc0ce0a798de208f3059371ea692093ba"))
