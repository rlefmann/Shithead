from game import Game
from requests import *


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
		if self.game._curplayer == 0: # change to not access local var
			raise Exception("the computer player is always player 1, but it is player 0s turn")
		if self.game.mode == GameMode.DOWNCARDS:
			playsrc = self.game.curupcards
			# return the first downcard slot that is not empty:
			i = 0
			while i < len(playsrc) and playsrc[i] is None:
				i+=1
			if i == len(playsrc):
				raise Exception("all downcards were already played")
			return RequestMove.play_from_downcards([i])
		else:
			src_collection, smallestplayable = self.findsmallestplayableindices()
			if len(smallestplayable) == 0:
				return RequestMove.take()
			else:
				if self.game.mode == GameMode.HAND:
					return RequestMove.play_from_hand(smallestplayable)
				elif self.game.mode == GameMode.UPCARDS:
					return RequestMove.play_from_upcards(smallestplayable)
		
	def findsmallestplayableindices(self):
		"""
		Finds the index of the smallest playable card, or indices,
		if there are several cards with the same rank
		"""
		 # TODO: here: get collection depending on gamemode
		if self.game.mode == GameMode.HAND:
			src_coll = self.game.curhand
		elif self.game.mode == GameMode.UPCARDS:
			src_coll = self.game.curupcards
		elif self.game.mode == GameMode.DOWNCARDS:
			raise Exception("we cannot find the smallest playable index from downcards")

		# create an order of the ranks:
		special = [self.game.settings["INVISIBLE"], self.game.settings["BURN"]]
		#regular = range(13)
		#for s in special:
		#	regular.remove(s)
		if self.game.minval == self.game.settings["LOWER"]:
			r = range(self.game.settings["LOWER"]+1) # 0,1,...,minval
		else:
			r = range(self.game.minval,13) # minval,minval+1,...,12
		order = [i for i in r if i not in special]
		order.extend(special) # special cards are last

		indices = []
		for rank in order:
			indices = [i for i,x in enumerate(src_coll) if x is not None and x.rank==rank]
			# the src_coll contains cards of this rank:
			if len(indices)>0:
				break
		return src_coll, indices
