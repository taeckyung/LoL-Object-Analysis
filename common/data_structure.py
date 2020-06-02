from typing import Union, Dict, List
import matplotlib.pylab as plt
from pprint import pformat
import numpy as np
import csv


class GameCount:
	def __init__(self, interval=1):
		"""
		GameCount class to record data with win|lose information (and time as optional).
		:param interval: Interval for time histogram.
		"""
		self.max_minute = 60
		self.count = [0, 0]
		self.hist = [np.zeros(self.max_minute // interval + 1) for _ in range(2)]
		self.interval = interval

	def insert(self, win: bool, minute: Union[int, float, None] = None):
		"""
		Insert new data.
		:param win: Boolean value.
		:param minute: Minute in number (optional).
		:return:
		"""
		if minute is not None:
			minute = min(int(minute), self.max_minute)
			self.hist[win][minute // self.interval] += 1
		self.count[win] += 1

	def total(self):
		return self.count[False] + self.count[True]

	def win_rate(self) -> float:
		if self.total() == 0:
			return 0
		return self.count[True] / self.total()

	def score(self) -> float:
		"""
		Score to measure time-dependent influence on win rate.
		:return: Score value.
		"""
		if self.total() == 0:
			return 0
		diff = [(self.hist[True][i] - self.hist[False][i]) / self.total() for i in range(0, self.max_minute + 1, self.interval)]
		return 100.0 * np.trapz(diff, dx=self.interval)

	def __str__(self):
		return "%.3f%% (%d / %d); %.1f" % (100*self.win_rate(), self.count[True], self.total(), self.score())

	def to_csv(self, file_name: str):
		with open(file_name, 'w', encoding='utf-8', newline='') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow([i for i in range(0, self.max_minute + 1, self.interval)])
			writer.writerow(self.hist[True])
			writer.writerow(self.hist[False])

	def plot(self, name: str):
		x_axis = [i for i in range(0, self.max_minute + 1, self.interval)]
		plt.title("%s: %.1f%% (%.1f)" % (name, 100*self.win_rate(), self.score()))
		if self.total() != 0:
			plt.plot(x_axis, self.hist[True] / self.total(), 'red', label="win")
			plt.plot(x_axis, self.hist[False] / self.total(), 'blue', label="lose")
			plt.legend(loc=1)
		plt.show()


class BaseStructure:
	def __init__(self, data: Dict):
		"""
		Base data structure to store dictionary data as a class.
		:param data: Raw dictionary from database.
		"""
		self.data = data

	def __str__(self):
		return pformat(self.data)


class GameDataStructure(BaseStructure):
	class Teams(BaseStructure):
		class Team(BaseStructure):
			class Participant(BaseStructure):
				class Stats(BaseStructure):
					def __init__(self, data: Dict):
						super().__init__(data)
						self.dict: Dict = data
						self.kills: int = data['kills']
						self.deaths: int = data['deaths']
						self.assists: int = data['assists']
						self.largestMultiKill: int = data['largestMultiKill']
						self.longestTimeSpentLiving: int = data['longestTimeSpentLiving']
						self.doubleKills: int = data['doubleKills']
						self.tripleKills: int = data['tripleKills']
						self.quadraKills: int = data['quadraKills']
						self.pentaKills: int = data['pentaKills']
						self.unrealKills: int = data['unrealKills']
						self.totalDamageDealt: int = data['totalDamageDealt']
						self.magicDamageDealt: int = data['magicDamageDealt']
						self.physicalDamageDealt: int = data['physicalDamageDealt']
						self.trueDamageDealt: int = data['trueDamageDealt']
						self.totalDamageDealtToChampions: int = data['totalDamageDealtToChampions']
						self.magicDamageDealtToChampions: int = data['magicDamageDealtToChampions']
						self.physicalDamageDealtToChampions: int = data['physicalDamageDealtToChampions']
						self.trueDamageDealtToChampions: int = data['trueDamageDealtToChampions']
						self.totalHeal: int = data['totalHeal']
						self.totalUnitsHealed: int = data['totalUnitsHealed']
						self.visionScore: int = data['visionScore']
						self.timeCCingOthers: int = data['timeCCingOthers']
						self.totalDamageTaken: int = data['totalDamageTaken']
						self.magicalDamageTaken: int = data['magicalDamageTaken']
						self.physicalDamageTaken: int = data['physicalDamageTaken']
						self.trueDamageTaken: int = data['trueDamageTaken']
						self.goldEarned: int = data['goldEarned']
						self.goldSpent: int = data['goldSpent']
						self.champLevel: int = data['champLevel']
						self.firstBloodKill: bool = data['firstBloodKill']
						self.perk0: int = data['perk0']
						self.perk1: int = data['perk1']
						self.perk2: int = data['perk2']
						self.perk3: int = data['perk3']
						self.perk4: int = data['perk4']
						self.perk5: int = data['perk5']
						self.participantId: int = data['participantId']

				def __init__(self, data: Dict):
					super().__init__(data)
					self.dict: Dict = data
					self.championId: int = data['championId']
					self.lane: str = data['lane']
					self.spells: List[int] = [spell for spell in data['spells']]
					self.items: List[int] = [item for item in data['items']]
					self.stats: GameData.Teams.Team.Participant.Stats = self.Stats(data['stats'])
					self.summonerId: str = data['summonerId']
					self.summonerName: str = data['summonerName']
					self.profileIcon: int = data['profileIcon']

			def __init__(self, data: Dict):
				super().__init__(data)
				self.participants: List[GameData.Teams.Team.Participant] = \
					[self.Participant(data['participants'][i]) for i in range(5)]
				self.bans: List[int] = [data['bans'][i] for i in range(5)]
				self.side: str = data['side']
				self.first_dragon: bool = data['first_dragon']
				self.first_inhibitor: bool = data['first_inhibitor']
				self.baron_kills: int = data['baron_kills']
				self.first_rift_herald: bool = data['first_rift_herald']
				self.first_baron: bool = data['first_baron']
				self.rift_herald_kills: int = data['rift_herald_kills']
				self.first_blood: bool = data['first_blood']
				self.first_tower: bool = data['first_tower']
				self.vilemaw_kills: int = data['vilemaw_kills']
				self.inhibitor_kills: int = data['inhibitor_kills']
				self.dominion_victory_score: int = data['dominion_victory_score']
				self.dragon_kills: int = data['dragon_kills']

		def __init__(self, data: Dict):
			super().__init__(data)
			self.win: GameData.Teams.Team = self.Team(data['win'])
			self.lose: GameData.Teams.Team = self.Team(data['lose'])

	class MonsterLog(BaseStructure):
		def __init__(self, monster_log: Dict):
			super().__init__(monster_log)
			self.timestamp: int = monster_log['timestamp']
			self.killer_id: int = monster_log['killer_id']
			self.monster_type: str = monster_log['monster_type']

	def __init__(self, data: Dict):
		super().__init__(data)
		self.game_id: int = data['game_id']
		self.game_mode: str = data['game_mode']
		self.game_type: str = data['game_type']
		self.game_duration: int = data['game_duration']
		self.timestamp: int = data['timestamp']
		self.version: str = data['version']
		self.teams: GameData.Teams = self.Teams(data['teams'])
		self.monster_logs: List[GameData.MonsterLog] = [self.MonsterLog(log) for log in data['monster_logs']]
		self.total_gold_logs: Dict[int, List[int]] = {str(i): data['total_gold_logs'][str(i)] for i in range(1, 11)}
		self.xp_logs: Dict[int, List[int]] = {i: data['xp_logs'][str(i)] for i in range(1, 11)}
		self.minions_killed_logs: Dict[int, List[int]] = {i: data['minions_killed_logs'][str(i)] for i in range(1, 11)}
		self.jungle_minions_killed_logs: Dict[int, List[int]] = \
			{i: data['jungle_minions_killed_logs'][str(i)] for i in range(1, 11)}


class GameData(GameDataStructure):
	AIR_DRAGON = 'AIR_DRAGON'
	WATER_DRAGON = 'WATER_DRAGON'
	EARTH_DRAGON = 'EARTH_DRAGON'
	FIRE_DRAGON = 'FIRE_DRAGON'
	DRAGON_TYPES = [AIR_DRAGON, WATER_DRAGON, EARTH_DRAGON, FIRE_DRAGON]
	BARON_NASHOR = 'BARON_NASHOR'
	RIFT_HERALD = 'RIFTHERALD'
	ELDER_DRAGON = 'ELDER_DRAGON'

	def __init__(self, data: Dict):
		"""
		Wrapper data structure for rank game data.
		Provides additional helper functions.
		:param data: Raw dictionary from database.
		"""
		super().__init__(data)
		self._is_monster_log_valid = True
		self.killer_id_zero_side = None
		self.parse_monster_log()

	def winner_side(self) -> str:
		"""
		Return the winner side of the current rank game.
		:return: 'blue' | 'red'
		"""
		return 'blue' if self.teams.win.side == 'blue' else 'red'

	def get_side(self, user_id: int) -> str:
		"""
		Get side from user id.
		:param user_id: User id. Should be in the range from 1 to 10.
		:return: 'blue' | 'red'
		"""
		assert(user_id in range(1, 11))
		if user_id < 6:
			return 'blue'
		else:
			return 'red'

	def is_same_side(self, id1: int, id2: int) -> bool:
		"""
		Check if two user id is from same side.
		:param id1: User id. Zero can be accepted.
		:param id2: User id. Zero can be accepted.
		:return: True | False
		"""
		assert(id1 in range(0, 11) and id2 in range(0, 11))
		side1 = self.get_side(id1) if id1 != 0 else self.killer_id_zero_side
		side2 = self.get_side(id2) if id2 != 0 else self.killer_id_zero_side
		return side1 == side2

	def is_id_winner(self, user_id: int) -> bool:
		"""
		Check if user id is in the winner side.
		:param user_id: User id. Zero can be accepted.
		:return: True | False
		"""
		assert(user_id in range(0, 11))
		side = self.get_side(user_id) if user_id != 0 else self.killer_id_zero_side
		return side == self.winner_side()

	def is_monster_log_valid(self):
		"""
		Function to check if data contains unprocessable killer_id = 0.
		About 20% of data consists of one killer_id = 0,
		and a few data consists of two (or maybe more) killer_id = 0.
		For simplicity, we only accept data consists of up to one killer_id = 0.
		:return:
		"""
		return self._is_monster_log_valid

	def parse_monster_log(self):
		"""
		Function to handle monster logs with killer_id = 0.
		:return:
		"""
		invalid = []
		for log in self.monster_logs:
			if log.killer_id == 0:
				invalid.append(log)
		if len(invalid) == 0:
			pass
		elif len(invalid) == 1:
			kills = [self.teams.lose.rift_herald_kills + self.teams.lose.dragon_kills + self.teams.lose.baron_kills,
					self.teams.win.rift_herald_kills + self.teams.win.dragon_kills + self.teams.win.baron_kills]
			for log in self.monster_logs:
				if log.killer_id != 0:
					kills[self.is_id_winner(log.killer_id)] -= 1
			self.killer_id_zero_side = kills[0] == 0
		else:
			self._is_monster_log_valid = False


class BaseParser:
	def __init__(self):
		"""
		Base parser class for analyzing the data.
		"""
		pass

	def parse(self, data: GameData):
		pass

	def to_csv(self):
		pass

	def plot(self):
		pass
