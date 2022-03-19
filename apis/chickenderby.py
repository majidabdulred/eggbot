from aiohttp import request
from util.logs import mylogs

API_URL = "https://api.chickenderby.com"


async def get_scheduled_races():
    URL = API_URL + "/api/race/all-races-scheduled"
    async with request("GET", url=URL) as res:
        if res.status != 200:
            mylogs.error(f"CHICKENDERBY_API_ERROR : {URL} : {await res.text()}")
            raise ValueError
        result = await res.json()
        return result


async def get_race_results():
    URL = API_URL + "/api/race/game-results?page=1&limit=3"
    async with request("GET", url=URL) as res:
        if res.status != 200:
            mylogs.error(f"CHICKENDERBY_RACE_RESULTS : {URL} : {await res.text()}")
            raise ValueError
        results = await res.json()
        return results


async def get_chickens(chicks: list) -> list:
    URL = "https://crun-minter.herokuapp.com/tokens"
    async with request("POST", URL, json={"tokenIds": chicks}) as res:
        if res.status != 200:
            mylogs.error(f"CRUN_API_ERROR : {URL} : {await res.text()}")
            raise ValueError
        results = await res.json()
        return results["body"]


async def get_chicken_race_history(chickenid, page, limit):
    URL = f"https://api.chickenderby.com/api/race/get-races-by-chicken?chickenId={chickenid}&page={page}&limit={limit}"
    async with request("GET",url=URL) as res:
        if res.status != 200:
            mylogs.error(f"CHICKEN_RACE_HISTORY_API_ERROR : {URL} : {res.text()}")
            raise ValueError
        results = await res.json()
        return results["rows"],results["count"]


async def get_weth_price():
    URL = "https://api.chickenderby.com/api/getCoinRate"
    async with request("GET", URL) as res:
        if res.status != 200:
            mylogs.error(f"GET_COIN_RATE_ERROR : {URL} : {await res.text()}")
            raise ValueError
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
