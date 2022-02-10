from .mydb import db
from .local_db import chickens_db

col = db.get_collection("chickens")


async def get_chicken(chick_id):
    if chick_id in chickens_db.keys():
        return chickens_db[chick_id]
    chicken = await col.find_one({"_id": chick_id})
    chickens_db[chick_id] = chicken
    return chicken


async def get_many_chickens(chick_ids: list):
    response = []
    for chick_id in chick_ids:
        if chick_id in chickens_db.keys():
            response.append(chickens_db[chick_id])
            chick_ids.remove(chick_id)
    query = col.find({"_id": {"$in": chick_ids}})
    async for doc in query:
        response.append(doc)
        chickens_db[doc["_id"]] = doc
    return response
