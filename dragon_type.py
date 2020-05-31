from common.data_structure import GameCount
from common.db import iter_high_elo
from typing import Dict



class DragonType:
	def __init__(self):
		self.dragonCountDict = dict()
		self.elementDragonCountDict = dict()
		self.dragon_type = ['AIR_DRAGON', 'WATER_DRAGON', 'EARTH_DRAGON', 'FIRE_DRAGON']

		for dragon in self.dragon_type:
			self.dragonCountDict[dragon] = [GameCount() for _ in range(4)]  # Win count for dragon count [0, 1, 2, 3]
			self.elementDragonCountDict[dragon] = GameCount()

	def parse(self, d: Dict):
		total_count = [0, 0]  # [lower_count, winner_count]
		dragon_count = [dict(), dict()]  # [loser_count, winner_count]
		dragon_time = [dict(), dict()]  # [loser_time, winner_time]
		for i in range(2):
			for dragon in self.dragon_type:
				dragon_count[i][dragon] = 0  # Number of dragon taken
				dragon_time[i][dragon] = 0  # Last taken time

		winner_side = 'blue' if d['teams']['win']['side'] == 'blue' else 'red'

		def check_winner(kid):
			return (winner_side == 'blue' and kid < 6) or (winner_side == 'red' and kid >= 6)

		for log in d['monster_logs']:
			monster_type = log['monster_type']
			is_winner = check_winner(log['killer_id'])
			time = log['timestamp'] // 60000
			if monster_type in self.dragon_type:
				total_count[is_winner] += 1

				if is_winner and total_count[True] == 4:
					self.elementDragonCountDict[monster_type].update(True, time)
				elif (not is_winner) and total_count[False] == 4:
					self.elementDragonCountDict[monster_type].update(False, time)
				else:
					dragon_count[is_winner][monster_type] += 1
					dragon_time[is_winner][monster_type] = time

		for dragon in self.dragon_type:
			self.dragonCountDict[dragon][dragon_count[False][dragon]].update(False, dragon_time[False][dragon])
			self.dragonCountDict[dragon][dragon_count[True][dragon]].update(True, dragon_time[True][dragon])

	def __str__(self):
		s = ""
		for dragon in self.dragon_type:
			for i in range(0, 4):
				s += "%s_%d: %s\n" % (dragon, i, self.dragonCountDict[dragon][i])
			s += "%s_ELEMENT: %s\n" % (dragon, self.elementDragonCountDict[dragon])
		return s


if __name__ == '__main__':
	dragonType = DragonType()
	iter_high_elo(dragonType.parse)
	print(dragonType)
