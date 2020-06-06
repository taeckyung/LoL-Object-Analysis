from common.data_structure import GameCount, GameData, BaseParser
from common.db import data_over_diamond, data_over_platinum


class DragonXHerald(BaseParser):
	def __init__(self, padding: float = 1):
		assert(padding <= 5)
		super().__init__()
		self.padding = padding
		self.dragonCountDict = dict()
		for dragon_type in GameData.DRAGON_TYPES:
			self.dragonCountDict[dragon_type] = GameCount()

	def parse(self, game_data: GameData):
		dragons = []
		heralds = []

		for log in game_data.monster_logs:
			monster_type = log.monster_type
			time = log.timestamp / 60000
			if time > 20 + self.padding:
				break
			if monster_type in GameData.DRAGON_TYPES:
				dragons.append(log)
			elif monster_type == GameData.RIFT_HERALD and log.killer_id != 0:
				heralds.append(log)

		if len(dragons) != 0:
			for dragon in dragons:
				dragon_time = dragon.timestamp / 60000
				for herald in heralds:
					herald_time = herald.timestamp / 60000
					# Herald killer_id is 0 if killed by Baron Nashor
					if (abs(dragon_time - herald_time) <= self.padding) and \
						not game_data.is_same_side(dragon.killer_id, herald.killer_id):
						self.dragonCountDict[dragon.monster_type].insert(game_data.is_id_winner(dragon.killer_id), dragon_time)

	def plot(self):
		for dragon_type in GameData.DRAGON_TYPES:
			self.dragonCountDict[dragon_type].plot("%s_EXCHANGE_WITH_%s" % (dragon_type, GameData.RIFT_HERALD))

	def __str__(self):
		s = ""
		for dragon_type in GameData.DRAGON_TYPES:
			s += "%s_EXCHANGE_WITH_%s: %s\n" % (dragon_type, GameData.RIFT_HERALD, self.dragonCountDict[dragon_type])
		return s


class BaronXElderOrElement(BaseParser):
	def __init__(self, padding: float = 1):
		assert(padding < 5)
		super().__init__()
		self.padding = padding
		self.elderCount = GameCount()
		self.elementCount = dict()
		for dragon_type in GameData.DRAGON_TYPES:
			self.elementCount[dragon_type] = GameCount()

	def parse(self, game_data: GameData):
		elders = []
		nashors = []
		dragons_count = [0, 0]
		element = None

		for log in game_data.monster_logs:
			if log.monster_type in GameData.DRAGON_TYPES:
				is_winner = game_data.is_id_winner(log.killer_id)
				dragons_count[is_winner] += 1
				if dragons_count[is_winner] == 4:
					element = log
			elif log.monster_type == GameData.ELDER_DRAGON:
				elders.append(log)
			elif log.monster_type == GameData.BARON_NASHOR:
				nashors.append(log)

		if len(nashors) != 0:
			for nashor in nashors:
				nashor_time = nashor.timestamp / 60000

				if element is not None:
					element_time = element.timestamp / 60000
					if (abs(nashor_time - element_time) < self.padding) and \
						not game_data.is_same_side(nashor.killer_id, element.killer_id):
						self.elementCount[element.monster_type].insert(game_data.is_id_winner(nashor.killer_id), nashor_time)

				for elder in elders:
					elder_time = elder.timestamp / 60000
					if (abs(nashor_time - elder_time) < self.padding) and \
						not game_data.is_same_side(nashor.killer_id, elder.killer_id):
						self.elderCount.insert(game_data.is_id_winner(nashor.killer_id), nashor_time)

	def plot(self):
		for dragon_type in GameData.DRAGON_TYPES:
			self.elementCount[dragon_type].plot("%s_EXCHANGE_WITH_%s_ELEMENT" % (GameData.BARON_NASHOR, dragon_type))
		self.elderCount.plot("%s_EXCHANGE_WITH_%s" % (GameData.BARON_NASHOR, GameData.ELDER_DRAGON))

	def __str__(self):
		s = ""
		for dragon_type in GameData.DRAGON_TYPES:
			s += "%s_EXCHANGE_WITH_%s_ELEMENT: %s\n" % (GameData.BARON_NASHOR, dragon_type, self.elementCount[dragon_type])
		s += "%s_EXCHANGE_WITH_%s: %s\n" % (GameData.BARON_NASHOR, GameData.ELDER_DRAGON, self.elderCount)
		return s


if __name__ == '__main__':
	dragonXHerald = DragonXHerald()
	for data in data_over_diamond():
		dragonXHerald.parse(data)
	dragonXHerald.plot()
	print(dragonXHerald)
	baronXElderOrElement = BaronXElderOrElement()
	for data in data_over_platinum():
		baronXElderOrElement.parse(data)
	baronXElderOrElement.plot()
	print(baronXElderOrElement)
