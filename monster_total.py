from common.data_structure import GameCount
from common.db import high_elo_data
from typing import Dict


class MonsterTotal:
	def __init__(self):
		self.dragon_type = ['AIR_DRAGON', 'WATER_DRAGON', 'EARTH_DRAGON', 'FIRE_DRAGON']

		self.riftheraldCountList = [GameCount() for _ in range(3)]
		self.baronCountList = [GameCount() for _ in range(11)]
		self.elderDragonCountList = [GameCount() for _ in range(11)]

		self.noDragonCount = GameCount()
		self.dragonCountDict = dict()
		self.elementDragonCountDict = dict()
		for dragon in self.dragon_type:
			self.dragonCountDict[dragon] = [GameCount() for _ in range(4)]  # Win count for dragon count [0, 1, 2, 3]
			self.elementDragonCountDict[dragon] = GameCount()

	def parse(self, d: Dict):
		riftherald_count = [0, 0]
		baron_count = [0, 0]
		elder_dragon_count = [0, 0]

		total_dragon_count = [0, 0]  # [lower_count, winner_count]
		dragon_count = [dict(), dict()]  # [loser_count, winner_count]
		dragon_time = [dict(), dict()]  # [loser_time, winner_time]
		for is_winner in range(2):
			for dragon in self.dragon_type:
				dragon_count[is_winner][dragon] = 0  # Number of dragon taken
				dragon_time[is_winner][dragon] = 0  # Last taken time

		winner_side = 'blue' if d['teams']['win']['side'] == 'blue' else 'red'

		def check_winner(kid):
			return (winner_side == 'blue' and kid < 6) or (winner_side == 'red' and kid >= 6)

		for log in d['monster_logs']:
			monster_type = log['monster_type']
			is_winner = check_winner(log['killer_id'])
			time = log['timestamp'] // 60000
			if monster_type in self.dragon_type:
				total_dragon_count[is_winner] += 1

				if is_winner and total_dragon_count[True] == 4:
					self.elementDragonCountDict[monster_type].update(True, time)
				elif (not is_winner) and total_dragon_count[False] == 4:
					self.elementDragonCountDict[monster_type].update(False, time)
				else:
					dragon_count[is_winner][monster_type] += 1
					dragon_time[is_winner][monster_type] = time
			elif monster_type == 'RIFTHERALD':
				riftherald_count[is_winner] += 1
				self.riftheraldCountList[riftherald_count[is_winner]].update(is_winner, time)
			elif monster_type == 'ELDER_DRAGON':
				elder_dragon_count[is_winner] += 1
				self.elderDragonCountList[elder_dragon_count[is_winner]].update(is_winner, time)
			elif monster_type == 'BARON_NASHOR':
				baron_count[is_winner] += 1
				self.baronCountList[baron_count[is_winner]].update(is_winner, time)

		for dragon in self.dragon_type:
			self.dragonCountDict[dragon][dragon_count[False][dragon]].update(False, dragon_time[False][dragon])
			self.dragonCountDict[dragon][dragon_count[True][dragon]].update(True, dragon_time[True][dragon])
		for is_winner in [False, True]:
			if total_dragon_count[is_winner] == 0:
				self.noDragonCount.update(is_winner)
			if riftherald_count[is_winner] == 0:
				self.riftheraldCountList[0].update(is_winner)
			if baron_count[is_winner] == 0:
				self.baronCountList[0].update(is_winner)
			if elder_dragon_count[is_winner] == 0:
				self.elderDragonCountList[0].update(is_winner)

	def __str__(self):
		s = ""
		for i in range(3):
			s += "RIFT_HERALD_%d: %s\n" % (i, self.riftheraldCountList[i])
		s += "NO_DRAGON: %s\n" % self.noDragonCount
		for dragon in self.dragon_type:
			for i in range(0, 4):
				s += "%s_%d: %s\n" % (dragon, i, self.dragonCountDict[dragon][i])
			s += "%s_ELEMENT: %s\n" % (dragon, self.elementDragonCountDict[dragon])
		for i in range(11):
			s += "ELDER_DRAGON_%d: %s\n" % (i, self.elderDragonCountList[i])
			s += "BARON_NASHOR_%d: %s\n" % (i, self.baronCountList[i])
		return s

	def to_csv(self):
		for i in range(3):
			self.riftheraldCountList[i].to_csv("RIFT_HERALD_%d.csv" % i)
		self.noDragonCount.to_csv("NO_DRAGON.csv")
		for dragon in self.dragon_type:
			for i in range(0, 4):
				self.dragonCountDict[dragon][i].to_csv("%s_DRAGON_%d.csv" % (dragon, i))
			self.elementDragonCountDict[dragon].to_csv("%s_ELEMENT.csv" % dragon)
		for i in range(11):
			self.elderDragonCountList[i].to_csv("ELDER_DRAGON_%d.csv" % i)
			self.baronCountList[i].to_csv("BARON_NASHOR_%d.csv" % i)

	def plot(self):
		for i in range(3):
			self.riftheraldCountList[i].plot("RIFT_HERALD_%d" % i)
		for dragon in self.dragon_type:
			for i in range(0, 4):
				self.dragonCountDict[dragon][i].plot("%s_%d" % (dragon, i))
			self.elementDragonCountDict[dragon].plot("%s_ELEMENT" % dragon)
		for i in range(11):
			self.elderDragonCountList[i].plot("ELDER_DRAGON_%d" % i)
			self.baronCountList[i].plot("BARON_NASHOR_%d" % i)


if __name__ == '__main__':
	monsterTotal = MonsterTotal()
	for data in high_elo_data:
		monsterTotal.parse(data)
	monsterTotal.plot()
	print(monsterTotal)
