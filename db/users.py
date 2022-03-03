import datetime
from util import updateCheck
from .mydb import db

col = db.get_collection("test")


async def get_user(userid):
    user = await col.find_one({"_id": userid})
    return user


async def get_users_from_address(address):
    cursor = col.find({"accounts.address": address})
    usersdb = await cursor.to_list(length=10)
    return usersdb


async def get_user_from_chickens(ids: list) -> list:
    cursor = col.find({"accounts.0.chicks": {"$in": ids}})
    res = await cursor.to_list(length=15)
    print(res)
    return res


async def save_user(userid, address):
    """data = {'userid':219879210,'address':{'address':'0xxwd3131','chicks'}'"""
    user = {"_id": userid, "accounts": [{"address": address, "chicks": []}], "updatedAt": datetime.datetime.utcnow()}
    await col.insert_one(user)


async def set_user_beta_to(_id, value):
    res = await col.update_one({"_id": _id}, {"$set": {"beta": value}})
    updateCheck(res, f"Add to beta {_id}")


async def set_address(userid, address):
    res = await col.update_one({"_id": userid}, {"$set": {"accounts.0.address": address},
                                                 "$currentDate": {"updatedAt": True}})

    updateCheck(res, f"SET_NEW_ADDRESS : {userid} : {address} ")


async def add_address(userid, address, chicks):
    res = await col.update_one({"_id": userid}, {"$addToSet": {"accounts": {"address": address, "chicks": chicks}},
                                                 "$currentDate": {"updatedAt": True}})

    updateCheck(res, f"ADD_NEW_ADDRESS : {userid} : {address} ")


async def remove_address(userid, address):
    # Add a filed to check how many chickens are there in the address
    res = await col.update_one({"_id": userid},
                               {"$pull": {"accounts": {"address": address}}, "$currentDate": {"updatedAt": True}})
    updateCheck(res, f"ADDRESS_REMOVE : {userid} : {address}")


async def update_chick_sum(userid, chicksum):
    res = await col.update_one({"_id": userid}, {"$set": {"chick_sum": chicksum}})
    updateCheck(res, f"CHICKSUM : {userid} : {chicksum}")


async def _update_for_0_chicken_users(address):
    res = await col.update_many({"accounts.address": address},
                                {"$currentDate": {"updatedAt": True}})
    updateCheck(res, f"NO_CHICKENS : {address}")


async def add_chickens(address, chicks: list):
    if len(chicks) == 0:
        await _update_for_0_chicken_users(address)
        return
    res = await col.update_many({"accounts.address": address},
                                {"$addToSet": {"accounts.$.chicks": {"$each": chicks}},
                                 "$currentDate": {"updatedAt": True}})
    updateCheck(res, f"ADD_CHICKS : {address} : {chicks}")


async def set_chickens(address, chicks: list):
    res = await col.update_many({"accounts.address": address},
                                {"$set": {"accounts.$.chicks": chicks}, "$currentDate": {"updatedAt": True}})
    updateCheck(res, f"SET_CHICKS : {address} : {chicks}")


async def remove_chickens(address, chicks: list):
    res = await col.update_many({"accounts.address": address},
                                {"$pull": {"accounts.$.chicks": {"$in": chicks}}, "$currentDate": {"updatedAt": True}})
    updateCheck(res, f"REM_CHICKS : {address} : {chicks}")
