from common.data_structure import GameCount, BaseParser, GameData
from common.db import data_over_diamond


class ElderAfterElement(BaseParser):
	def __init__(self):
		super().__init__()
		self.elderNoElementCount = GameCount()
		self.elderAndElementCount = GameCount()

	def parse(self, game_data: GameData):
		dragons_count = [0, 0]
		element = None
		elder = None

		for log in game_data.monster_logs:
			if log.monster_type in GameData.DRAGON_TYPES:
				is_winner = game_data.is_id_winner(log.killer_id)
				dragons_count[is_winner] += 1
				if dragons_count[is_winner] == 4:
					element = log
			elif log.monster_type == GameData.ELDER_DRAGON and elder is None:
				elder = log

		if element is not None and elder is not None:
			if not game_data.is_same_side(element.killer_id, elder.killer_id):
				self.elderNoElementCount.insert(game_data.is_id_winner(elder.killer_id), elder.timestamp / 60000)
			else:
				self.elderAndElementCount.insert(game_data.is_id_winner(elder.killer_id), elder.timestamp / 60000)

	def __str__(self):
		s = ""
		s += "ELDER_DRAGON_AFTER_DRAGON_ELEMENT_TAKEN_AWAY: %s\n" % self.elderNoElementCount
		s += "ELDER_DRAGON_AND_DRAGON_ELEMENT: %s\n" % self.elderAndElementCount
		return s

	def plot(self):
		self.elderNoElementCount.plot("ELDER_DRAGON_AFTER_DRAGON_ELEMENT_TAKEN_AWAY")
		self.elderAndElementCount.plot("ELDER_DRAGON_AND_DRAGON_ELEMENT")


if __name__ == '__main__':
	elderAfterElement = ElderAfterElement()
	for data in data_over_diamond():
		elderAfterElement.parse(data)
	elderAfterElement.plot()
	print(elderAfterElement)
