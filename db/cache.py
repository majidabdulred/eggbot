from .mydb import db

races_send = db.get_collection("races_send")
from pymongo.errors import DuplicateKeyError


async def has_send(raceid):
    return await races_send.find_one({"_id": raceid})


async def add_send_race(raceid):
    try:
        return await races_send.insert_one({"_id": raceid})
    except DuplicateKeyError:
        return
