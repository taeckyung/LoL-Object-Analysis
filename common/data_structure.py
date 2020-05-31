from typing import Union
from pprint import pformat


class GameCount:
	def __init__(self, interval=5):
		self.max_minute = 60
		self.win = 0
		self.lose = 0
		self.win_hist = [0 for _ in range(self.max_minute//interval + 1)]
		self.lose_hist = [0 for _ in range(self.max_minute//interval + 1)]
		self.interval = 5

	def update(self, win: bool, minute: Union[int, None] = None):
		if minute is not None:
			minute = min(minute, self.max_minute)
		if win:
			self.win += 1
			if minute is not None:
				self.win_hist[minute//self.interval] += 1
		else:
			self.lose += 1
			if minute is not None:
				self.lose_hist[minute//self.interval] += 1

	def win_rate(self) -> float:
		if (self.win + self.lose) == 0:
			return 0
		return self.win / (self.win + self.lose)

	def __str__(self):
		return "%.3f%% (%d / %d)\n" % (self.win_rate(), self.win, self.win + self.lose) + \
				"\t" + pformat(self.win_hist) + "\n\t" + pformat(self.lose_hist)
