from aiohttp import request

API_URL = "https://api.chickenderby.com"


async def get_scheduled_races():
    URL = API_URL + "/api/race/all-races-scheduled"
    async with request("GET", url=URL) as res:
        if res.status != 200:
            raise ValueError("CHICKENDERBY_API_ERROR", URL, res)
        result = await res.json()
        return result


async def get_chickens(chicks: list) -> list:
    URL = "https://crun-minter.herokuapp.com/tokens"
    async with request("POST", URL, json={"tokenIds": chicks}) as res:
        if res.status != 200:
            raise ValueError("CRUN_API_ERROR", URL, res)
        results = await res.json()
        return results["body"]


async def get_weth_price():
    URL = "https://api.chickenderby.com/api/getCoinRate"
    async with request("GET", URL) as res:
        if res.status != 200:
            raise ValueError("GET_COIN_RATE_ERROR", res)
        results = await res.json()
        price = results.get("weth")
        return price


async def get_race_data(raceid):
    URL = f"https://api.chickenderby.com/api/race/get-race-data?raceId={raceid}"
    async with request("GET", URL) as res:
        if res.status == 400:
            return None
        elif res.status != 200:
            raise ValueError("GET_RACE_DATA_ERROR", res)
        results = await res.json()
        return results