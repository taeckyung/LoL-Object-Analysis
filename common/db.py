from pymongo import MongoClient
from typing import Callable

client = MongoClient('localhost', 27017)
collection = client['rank_game']['v10_10']

high_elo = ["DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]
high_data = collection.find({"tier": {"$in": high_elo}})


def iter_high_elo(f: Callable):
	for data in high_data:
		f(data)
