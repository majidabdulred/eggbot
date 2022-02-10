import asyncio
from util import mylogs
from pymongo import MongoClient
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from collections import namedtuple
load_dotenv()
if __name__ == '__main__':
    client: MongoClient = AsyncIOMotorClient(os.getenv("DB"))
else:
    client = AsyncIOMotorClient(os.getenv("DB"))
    client.get_io_loop = asyncio.get_event_loop
    mylogs.info("DATABASE CONNECTED")

db = client.get_database("chick")

