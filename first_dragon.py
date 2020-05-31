from common.data_structure import GameCount
from common.db import iter_high_elo
from pymongo import MongoClient
from typing import Dict

client = MongoClient('localhost', 27017)
collection = client['rank_game']['v10_10']

high_elo = ["DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]
high_data = collection.find({"tier": {"$in": high_elo}})


class FirstDragon:
	def __init__(self):
		self.gameCount = GameCount()

	def parse(self, d: Dict):
		winner_side = 'blue' if d['teams']['win']['side'] == 'blue' else 'red'

		def check_winner(kid):
			return (winner_side == 'blue' and kid < 6) or (winner_side == 'red' and kid >= 6)

		for log in d['monster_logs']:
			monster_type = log['monster_type']
			if 'DRAGON' in monster_type:
				is_winner = check_winner(log['killer_id'])
				time = log['timestamp'] // 60000
				self.gameCount.update(is_winner, time)
				break

	def __str__(self):
		return "First Dragon WinRate: %s" % self.gameCount


if __name__ == '__main__':
	firstDragon = FirstDragon()
	iter_high_elo(firstDragon.parse)
	print(firstDragon)

