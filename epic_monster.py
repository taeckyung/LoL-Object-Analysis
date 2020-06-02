from common.data_structure import GameCount, BaseParser, GameData
from common.db import data_over_diamond


class EpicMonster(BaseParser):
	def __init__(self):
		super().__init__()

		self.riftheraldCountList = [GameCount() for _ in range(3)]
		self.baronCountList = [GameCount() for _ in range(11)]
		self.elderDragonCountList = [GameCount() for _ in range(11)]
		self.elementDragonCountDict = dict()
		for dragon_type in GameData.DRAGON_TYPES:
			self.elementDragonCountDict[dragon_type] = GameCount()

	def parse(self, game_data: GameData):
		if not game_data.is_monster_log_valid:
			return

		riftherald_count = [0, 0]
		baron_count = [0, 0]
		elder_dragon_count = [0, 0]

		total_dragon_count = [0, 0]  # [lower_count, winner_count]
		dragon_count = [dict(), dict()]  # [loser_count, winner_count]
		dragon_time = [dict(), dict()]  # [loser_time, winner_time]
		for is_winner in [False, True]:
			for dragon_type in GameData.DRAGON_TYPES:
				dragon_count[is_winner][dragon_type] = 0  # Number of dragon taken
				dragon_time[is_winner][dragon_type] = 0  # Last taken time

		for log in game_data.monster_logs:
			monster_type = log.monster_type
			is_winner = game_data.is_id_winner(log.killer_id)
			time = log.timestamp // 60000
			if monster_type in GameData.DRAGON_TYPES:
				total_dragon_count[is_winner] += 1
				if is_winner and total_dragon_count[True] == 4:
					self.elementDragonCountDict[monster_type].update(True, time)
				elif (not is_winner) and total_dragon_count[False] == 4:
					self.elementDragonCountDict[monster_type].update(False, time)
			elif monster_type == GameData.RIFT_HERALD:
				riftherald_count[is_winner] += 1
				self.riftheraldCountList[riftherald_count[is_winner]].update(is_winner, time)
			elif monster_type == GameData.ELDER_DRAGON:
				elder_dragon_count[is_winner] += 1
				self.elderDragonCountList[elder_dragon_count[is_winner]].update(is_winner, time)
			elif monster_type == GameData.BARON_NASHOR:
				baron_count[is_winner] += 1
				self.baronCountList[baron_count[is_winner]].update(is_winner, time)

		for is_winner in [False, True]:
			if riftherald_count[is_winner] == 0 and riftherald_count[not is_winner] != 0:
				self.riftheraldCountList[0].update(is_winner)
			if baron_count[is_winner] == 0 and baron_count[not is_winner] != 0:
				self.baronCountList[0].update(is_winner)
			if elder_dragon_count[is_winner] == 0 and elder_dragon_count[not is_winner] != 0:
				self.elderDragonCountList[0].update(is_winner)

	def __str__(self):
		s = ""
		for i in range(3):
			s += "RIFT_HERALD_%d: %s\n" % (i, self.riftheraldCountList[i])
		for dragon_type in GameData.DRAGON_TYPES:
			s += "%s_ELEMENT: %s\n" % (dragon_type, self.elementDragonCountDict[dragon_type])
		for i in range(11):
			s += "ELDER_DRAGON_%d: %s\n" % (i, self.elderDragonCountList[i])
			s += "BARON_NASHOR_%d: %s\n" % (i, self.baronCountList[i])
		return s

	def plot(self):
		for i in range(3):
			self.riftheraldCountList[i].plot("RIFT_HERALD_%d" % i)
		for dragon in GameData.DRAGON_TYPES:
			self.elementDragonCountDict[dragon].plot("%s_ELEMENT" % dragon)
		for i in range(11):
			self.elderDragonCountList[i].plot("ELDER_DRAGON_%d" % i)
			self.baronCountList[i].plot("BARON_NASHOR_%d" % i)


if __name__ == '__main__':
	epicMonster = EpicMonster()
	for data in data_over_diamond():
		epicMonster.parse(data)
	epicMonster.plot()
	print(epicMonster)
