from .data_structure import GameData
from pymongo import MongoClient
from typing import Generator
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
collection = client['rank_game']['v10_10']

elo = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]


def data_over_diamond() -> Generator[GameData, None, None]:
	target = collection.find({"tier": {"$in": elo[-4:]}, "game_duration": {"$gte": 1200}})
	# target = collection.find({"_id": ObjectId('5ec3b60fc2e2b3e578aeea31')})
	for data in target:
		yield GameData(data)


def data_over_platinum() -> Generator[GameData, None, None]:
	target = collection.find({"tier": {"$in": elo[4:]}, "game_duration": {"$gte": 1200}})
	for data in target:
		yield GameData(data)
