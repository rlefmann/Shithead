import json


class Settings(dict):
	"""
	A settings object which contains all the necessary settings for
	the rules of the game of shithead. To be more specific it specifies
	the rank of the special cards as well as the initial amount of cards
	dealed to the players.
	"""
	def __init__(self, filepath=None):
		"""
		Creates a new settings object. If a filepath is specified,
		the settings are loaded from that file. Otherwise default
		values are set
		"""
		super(self.__class__, self).__init__()
		if filepath:
			self.load(filepath)
		# set default values:
		else:
			self["NCARDS_HAND"] = 4
			self["NCARDS_UPDOWN"] = 3
			self["LOWER"] = 7  # Nines are lower
			self["SKIP"] = 5  # On Sevens the next player has to skip
			self["INVISIBLE"] = 1
			self["BURN"] = 0

	def load(self, filepath):
		"""
		Loads the settings contained in the specified file and
		overwrites the current settings.
		"""
		with open(filepath, 'r') as f:
			for key, val in json.load(f).iteritems():
				self[key] = val

	def save(self, filepath):
		"""
		Saves the current state of the settings object to the specified
		file.
		"""
		with open(filepath, 'w') as f:
			json.dump(self, f)

	def check(self):
		"""
		Checks whether the current dictionary values are valid w.r.t.
		the game rules and all necessary settings are specified.
		"""
		pass  # TODO


if __name__ == "__main__":
	s = Settings()
	s["BURN"] = 42
