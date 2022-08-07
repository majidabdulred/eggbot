from aiohttp import request
from util.logs import mylogs

from models.model_races_scheduled import ScheduledRaces
from models.model_races_results import RaceResults
from models.model_races_by_chicken import RacesByChicken
from models.model_get_chicken import get_chickens_model
from models.model_race_by_id import RaceByIdModel
API_URL = "https://api.chickenderby.com"


async def get_scheduled_races():
    URL = API_URL + '/api/races?page=1&limit=100&filter={"status":"scheduled"}'
    async with request(method="GET", url=URL) as res:
        if res.status != 200:
            mylogs.error(f"CHICKENDERBY_API_ERROR : {URL} : {await res.text()}")
            raise ValueError
        result = await res.json()
        return ScheduledRaces(result)


async def get_race_results():
    URL = API_URL + '/api/results?page=1&limit=10'
    async with request("GET", url=URL) as res:
        if res.status != 200:
            mylogs.error(f"CHICKENDERBY_RACE_RESULTS : {URL} : {await res.text()}")
            raise ValueError
        results = await res.json()
        return RaceResults(results)


async def get_chickens(chicks: list):
    URL = "https://crun-minter.herokuapp.com/tokens"
    async with request("POST", URL, json={"tokenIds": chicks}) as res:
        if res.status != 200:
            mylogs.error(f"CRUN_API_ERROR : {URL} : {await res.text()}")
            raise ValueError
        results = await res.json()
        return get_chickens_model(results)


async def get_chicken_race_history(chickenid, page, limit):
    URL = API_URL+f"/api/races/chickens/{chickenid}?page={page}&limit={limit}"
    async with request("GET", url=URL) as res:
        if res.status != 200:
            mylogs.error(f"CHICKEN_RACE_HISTORY_API_ERROR : {URL} : {res.text()}")
            raise ValueError
        results = await res.json()
        return RacesByChicken(results)


async def get_race_data(raceid):
    URL = f"https://api.chickenderby.com/api/races/{raceid}"
    async with request("GET", URL) as res:
        if res.status == 400:
            return None
        elif res.status != 200:
            raise ValueError("GET_RACE_DATA_ERROR", res)
        results = await res.json()
        return RaceByIdModel(results)
