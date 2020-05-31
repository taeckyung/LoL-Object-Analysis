import matplotlib.pylab as plt
from pprint import pformat
from typing import Union
import numpy as np
import csv


class GameCount:
	def __init__(self, interval=1):
		self.max_minute = 60
		self.win = 0
		self.lose = 0
		self.win_hist = np.array([0 for _ in range(self.max_minute // interval + 1)])
		self.lose_hist = np.array([0 for _ in range(self.max_minute // interval + 1)])
		self.interval = interval

	def update(self, win: bool, minute: Union[int, None] = None):
		if minute is not None:
			minute = min(minute, self.max_minute)
		if win:
			self.win += 1
			if minute is not None:
				self.win_hist[minute // self.interval] += 1
		else:
			self.lose += 1
			if minute is not None:
				self.lose_hist[minute // self.interval] += 1

	def total(self):
		return self.win + self.lose

	def win_rate(self) -> float:
		if (self.win + self.lose) == 0:
			return 0
		return self.win / self.total()

	def score(self) -> float:
		if self.total() == 0:
			return 0
		diff = [(self.win_hist[i] - self.lose_hist[i]) / self.total() for i in range(0, self.max_minute + 1, self.interval)]
		return 100.0 * np.trapz(diff, dx=self.interval)

	def __str__(self):
		return "%.3f%% (%d / %d)" % (self.win_rate(), self.win, self.total())

	def to_csv(self, file_name: str):
		with open(file_name, 'w', encoding='utf-8', newline='') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow([i for i in range(0, self.max_minute + 1, self.interval)])
			writer.writerow(self.win_hist)
			writer.writerow(self.lose_hist)

	def plot(self, name: str):
		x_axis = [i for i in range(0, self.max_minute + 1, self.interval)]
		plt.title("%s: %.1f" % (name, self.score()))
		if self.total() != 0:
			plt.plot(x_axis, self.win_hist / self.total(), 'red', label="win")
			plt.plot(x_axis, self.lose_hist / self.total(), 'blue', label="lose")
			plt.legend(loc=1)
		plt.show()
