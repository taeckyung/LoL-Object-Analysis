from common.data_structure import GameCount
from common.db import high_elo_data
from pymongo import MongoClient
from typing import Dict

client = MongoClient('localhost', 27017)
collection = client['rank_game']['v10_10']

high_elo = ["DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]
high_data = collection.find({"tier": {"$in": high_elo}})


class FirstDragonHerald:
	def __init__(self):
		self.firstDragonCount = GameCount()
		self.firstHeraldCount = GameCount()
		self.firstBothCount = GameCount()

	def parse(self, d: Dict):
		winner_side = 'blue' if d['teams']['win']['side'] == 'blue' else 'red'

		def check_winner(kid):
			return (winner_side == 'blue' and kid < 6) or (winner_side == 'red' and kid >= 6)

		first_dragon = None
		first_herald = None

		for log in d['monster_logs']:
			monster_type = log['monster_type']
			is_winner = check_winner(log['killer_id'])
			time = log['timestamp'] // 60000
			if first_dragon is None and 'DRAGON' in monster_type:
				self.firstDragonCount.update(is_winner, time)
				first_dragon = is_winner
			elif first_herald is None and  'RIFTHERALD' in monster_type:
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

	def to_csv(self):
		self.firstDragonCount.to_csv('firstDragon.csv')
		self.firstHeraldCount.to_csv('firstHerald.csv')
		self.firstBothCount.to_csv('firstBoth.csv')

	def plot(self):
		self.firstDragonCount.plot('First Dragon')
		self.firstHeraldCount.plot('First Rift Herald')


if __name__ == '__main__':
	firstDragonHerald = FirstDragonHerald()
	for data in high_elo_data:
		firstDragonHerald.parse(data)
	print(firstDragonHerald)
	firstDragonHerald.plot()


