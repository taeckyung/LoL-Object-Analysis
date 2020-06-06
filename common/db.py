from .data_structure import GameData
from typing import Generator, List
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
collection = client['rank_game']['v10_10']

elo = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]


def data_by_id(id_list: List[str]) -> Generator[GameData, None, None]:
	"""
	Wrapper function to supply data by own id.
	:return:
	"""
	target = collection.find({"_id": {"$in": [ObjectId[id_] for id_ in id_list]}})
	for data in target:
		yield GameData(data)


def data_over_diamond(only_valid_monster=True) -> Generator[GameData, None, None]:
	"""
	Wrapper function to supply data from over Diamond tier.
	:return:
	"""
	target = collection.find({"tier": {"$in": elo[-4:]}, "game_duration": {"$gte": 1200}})
	for data in target:
		game_data = GameData(data)
		if not only_valid_monster or (only_valid_monster and game_data.is_monster_log_valid()):
			yield game_data


def data_over_platinum(only_valid_monster=True) -> Generator[GameData, None, None]:
	"""
	Wrapper function to supply data from over Platinum tier.
	:return:
	"""
	target = collection.find({"tier": {"$in": elo[4:]}, "game_duration": {"$gte": 1200}})
	for data in target:
		game_data = GameData(data)
		if not only_valid_monster or (only_valid_monster and game_data.is_monster_log_valid()):
			yield game_data
