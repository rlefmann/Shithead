from game import Game
from ..requests import RequestMove
from ..gamemode import GameMode


class AI(object):
	"""
	This is a base class for all specific AI implementations.
	"""
	def __init__(self, game):
		self.game = game

	def think(self):
		raise NotImplementedError("do not use the AI base class but a class that inherits from it")


class StraightforwardAI(AI):
	"""
	This is a basic AI that always plays all the cards of lowest possible
	playable rank. This is indeed the basic strategy for shithead.
	"""
	def __init__(self, game):
		super(StraightforwardAI, self).__init__(game)

	def think(self):
		if self.game.curplayeridx == 0: # change to not access local var
			raise Exception("the computer player is always player 1, but it is player 0s turn")
		if self.game.mode == GameMode.DOWNCARDS:
			playsrc = self.game.curplayer.downcards
			# return the first downcard slot that is not empty:
			i = 0
			while i < len(playsrc) and playsrc[i] is None:
				i+=1
			if i == len(playsrc):
				raise Exception("all downcards were already played")
			return RequestMove.play_from_downcards(1, [i])
		else:
			src_collection, smallestplayable = self.findsmallestplayableindices()
			if len(smallestplayable) == 0:
				return RequestMove.take(1)
			else:
				if self.game.mode == GameMode.HAND:
					return RequestMove.play_from_hand(1, smallestplayable)
				elif self.game.mode == GameMode.UPCARDS:
					return RequestMove.play_from_upcards(1, smallestplayable)
				elif self.game.mode == GameMode.TAKE_UPCARDS:
					return RequestMove.take_upcards(1, smallestplayable)
		
	def findsmallestplayableindices(self):
		"""
		Finds the index of the smallest playable card, or indices,
		if there are several cards with the same rank
		"""
		 # get collection depending on gamemode:
		if self.game.mode == GameMode.HAND:
			src_coll = self.game.curplayer.hand
		elif self.game.mode in [GameMode.UPCARDS, GameMode.TAKE_UPCARDS]:
			src_coll = self.game.curplayer.upcards
		elif self.game.mode == GameMode.DOWNCARDS:
			raise Exception("we cannot find the smallest playable index from downcards")

		# create an order of the ranks:
		special = [self.game._settings["INVISIBLE"], self.game._settings["BURN"]]

		if self.game._minval == self.game._settings["LOWER"]:
			r = range(self.game._settings["LOWER"]+1) # 0,1,...,minval
		else:
			r = range(self.game._minval,13) # minval,minval+1,...,12
		order = [i for i in r if i not in special]
		order.extend(special) # special cards are last

		indices = []
		for rank in order:
			indices = [i for i,x in enumerate(src_coll) if x is not None and x.rank==rank]
			# the src_coll contains cards of this rank:
			if len(indices)>0:
				break
		return src_coll, indices
