from common.data_structure import GameCount, BaseParser, GameData
from common.db import data_over_diamond
from pymongo import MongoClient
from typing import Dict

client = MongoClient('localhost', 27017)
collection = client['rank_game']['v10_10']

high_elo = ["DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]
high_data = collection.find({"tier": {"$in": high_elo}})


class FirstDragonHerald(BaseParser):
	def __init__(self):
		super().__init__()
		self.firstDragonCount = GameCount()
		self.firstHeraldCount = GameCount()
		self.firstBothCount = GameCount()

	def parse(self, game_data: GameData):
		if not game_data.is_monster_log_valid:
			return

		first_dragon = None
		first_herald = None

		for log in game_data.monster_logs:
			monster_type = log.monster_type
			is_winner = game_data.is_id_winner(log.killer_id)
			time = log.timestamp // 60000
			if first_dragon is None and monster_type in GameData.DRAGON_TYPES:
				self.firstDragonCount.update(is_winner, time)
				first_dragon = is_winner
			elif first_herald is None and monster_type == GameData.RIFT_HERALD:
				self.firstHeraldCount.update(is_winner, time)
				first_herald = is_winner
			if first_dragon is not None and first_herald is not None:
				break

		if first_herald == first_dragon:
			self.firstBothCount.update(first_dragon)

	def __str__(self):
		return "First Dragon WinRate: %s\n" % self.firstDragonCount + \
				"First Herald WinRate: %s\n" % self.firstHeraldCount + \
				"First Dragon & Herald WinRate: %s\n" % self.firstBothCount

	def plot(self):
		self.firstDragonCount.plot('First Dragon')
		self.firstHeraldCount.plot('First Rift Herald')


if __name__ == '__main__':
	firstDragonHerald = FirstDragonHerald()
	for data in data_over_diamond():
		firstDragonHerald.parse(data)
	print(firstDragonHerald)
	firstDragonHerald.plot()


