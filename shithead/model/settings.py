import json


class Settings(object):
	"""
	A settings object which contains all the necessary settings for
	the rules of the game of shithead. It specifies for example
	the rank of the special cards as well as the initial amount of cards
	dealed to the players.
	"""
	def __init__(self, filepath=None):
		"""
		Creates a new settings object. If a filepath is specified,
		the settings are loaded from that file. Otherwise default
		values are set
		"""
		# set default values:
		self.ncards_hand = 4
		self.ncards_updown = 3
		self.lower = 7  # Nines are lower
		self.skip = 5  # On Sevens the next player has to skip
		self.invisible = 1
		self.burn = 0
		if filepath:
			self.load(filepath)

	def load(self, filepath):
		"""
		Loads the settings contained in the specified file and
		overwrites the current settings.
		"""
		with open(filepath, 'r') as f:
			for key, val in json.load(f).iteritems():
				if key in self.__dict__:
					self.__dict__[key] = val
				else:
					raise ValueError("invalid parameter {}.".format(key))

	def save(self, filepath):
		"""
		Saves the current state of the settings object to the specified
		file.
		"""
		with open(filepath, 'w') as f:
			json.dump(self.__dict__, f)

	def check(self):
		"""
		Checks whether the current dictionary values are valid w.r.t.
		the game rules and all necessary settings are specified.
		"""
		if self.ncards_hand < 1 or self.ncards_updown < 1:
			return False
		return True # TODO: more checks


if __name__ == "__main__":
	s = Settings()
	print s.lower
	s.burn = 42
	print s.burn
