import asyncio
import datetime

from .mydb import db

col = db.get_collection("whitelist")


async def add_whitelist(userid, address):
    """data = {'userid':219879210,'address':'0xab76c8a0a8fb2fb2b4a9a7f0df541173ca6504bb'"""
    user = {"_id": userid, "address": address, "updatedAt": datetime.datetime.utcnow()}
    await col.insert_one(user)


async def remove_whitelist(userid):
    """data = {'userid':219879210,'address':'0xab76c8a0a8fb2fb2b4a9a7f0df541173ca6504bb'"""
    await col.delete_one({"_id": userid})


async def count_whitelist():
    k = await col.count_documents({})
    return k


async def get_user_whitelist(userid):
    user = await col.find_one({"_id": userid})
    return user


