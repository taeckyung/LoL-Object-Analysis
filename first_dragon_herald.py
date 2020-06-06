from common.data_structure import GameCount, BaseParser, GameData
from common.db import data_over_diamond


class FirstDragonHerald(BaseParser):
	def __init__(self):
		super().__init__()
		self.firstDragonCount = GameCount()
		self.firstHeraldCount = GameCount()
		self.firstBothCount = GameCount()
		self.firstDragonTypeCountDict = dict()
		for dragon_type in GameData.DRAGON_TYPES:
			self.firstDragonTypeCountDict[dragon_type] = GameCount()

	def parse(self, game_data: GameData):
		first_dragon = None
		first_herald = None

		for log in game_data.monster_logs:
			monster_type = log.monster_type
			is_winner = game_data.is_id_winner(log.killer_id)
			time = log.timestamp // 60000
			if first_dragon is None and monster_type in GameData.DRAGON_TYPES:
				self.firstDragonCount.insert(is_winner, time)
				self.firstDragonTypeCountDict[monster_type].insert(is_winner, time)
				first_dragon = is_winner
			elif first_herald is None and monster_type == GameData.RIFT_HERALD:
				self.firstHeraldCount.insert(is_winner, time)
				first_herald = is_winner
			if first_dragon is not None and first_herald is not None:
				break

		if first_herald == first_dragon:
			self.firstBothCount.insert(first_dragon)

	def __str__(self):
		s = ""
		s += "FIRST_DRAGON: %s\n" % self.firstDragonCount
		s += "FIRST_RIFT_HERALD: %s\n" % self.firstHeraldCount
		s += "FIRST_DRAGON_AND_RIFT_HERALD: % s\n" % self.firstBothCount
		for dragon_type in GameData.DRAGON_TYPES:
			s += "FIRST_%s: %s\n" % (dragon_type, self.firstDragonTypeCountDict[dragon_type])
		return s

	def plot(self):
		self.firstDragonCount.plot('FIRST_DRAGON')
		self.firstHeraldCount.plot('FIRST_RIFT_HERALD')
		self.firstBothCount.plot('FIRST_DRAGON_AND_RIFT_HERALD')
		for dragon_type in GameData.DRAGON_TYPES:
			self.firstDragonTypeCountDict[dragon_type].plot("FIRST_%s" % dragon_type)


if __name__ == '__main__':
	firstDragonHerald = FirstDragonHerald()
	for data in data_over_diamond():
		firstDragonHerald.parse(data)
	print(firstDragonHerald)
	firstDragonHerald.plot()


