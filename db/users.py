import datetime
from util import updateCheck

from .mydb import db

col = db.get_collection("test")


async def get_user(userid):
    user = await col.find_one({"_id": userid})
    return user


async def save_user(userid, address):
    """data = {'userid':219879210,'address':{'address':'0xxwd3131','chicks'}'"""
    user = {"_id": userid, "accounts": [{"address": address, "chicks": []}], "updatedAt": datetime.datetime.utcnow()}
    await col.insert_one(user)


async def set_user_beta_to(_id, value):
    res = await col.update_one({"_id": _id}, {"$set": {"beta": value}})
    updateCheck(res, f"Add to beta {_id}")


async def add_address(userid, address, chicks):
    res = await col.update_one({"_id": userid}, {"$addToSet": {"accounts": {"address": address, "chicks": chicks}},
                                                 "$currentDate": {"updatedAt": True}})

    updateCheck(res, f" Address add {address} , {userid} . ")


async def remove_address(userid, address):
    # Add a filed to check how many chickens are there in the address
    res = await col.update_one({"_id": userid},
                               {"$pull": {"accounts": {"address": address}}, "$currentDate": {"updatedAt": True}})
    updateCheck(res, f"Address removal {address},{userid}")


async def _update_for_0_chicken_users(address):
    res = await col.update_one({"accounts.address": address},
                               {"$currentDate": {"updatedAt": True}})
    updateCheck(res, f"Updated 0 chicken user {address}")


async def add_chickens(address, chicks: list):
    if len(chicks) == 0:
        await _update_for_0_chicken_users(address)
        return
    res = await col.update_one({"accounts.address": address},
                               {"$addToSet": {"accounts.$.chicks": {"$each": chicks}},
                                "$currentDate": {"updatedAt": True}})
    updateCheck(res, f"Added Chickens {address},{chicks}")


async def set_chickens(address, chicks: list):
    res = await col.update_one({"accounts.address": address},
                               {"$set": {"accounts.$.chicks": chicks}, "$currentDate": {"updatedAt": True}})
    updateCheck(res, f"Chickens Set to {address},{chicks}")


async def remove_chickens(address, chicks: list):
    res = await col.update_one({"accounts.address": address},
                               {"$pull": {"accounts.$.chicks": {"$in": chicks}}, "$currentDate": {"updatedAt": True}})
    updateCheck(res, f"Removed Chickens {address},{chicks}")
