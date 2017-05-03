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
		if self.game._curplayer == 0:
			raise Exception("the computer player is always player 1, but it is player 0s turn")
		src_collection, smallestplayable = self.findsmallestplayableindices()
		if len(smallestplayable) == 0:
			return RequestTake()
		else:
			return RequestPlay(AType.PLAY, smallestplayable)
		
	def findsmallestplayableindices(self):
		"""
		Finds the index of the smallest playable card, or indices,
		if there are several cards with the same rank
		"""
		src_coll = self.game.curplayer # TODO: here: get collection depending on gamemode
		pcards = self.game.players[1].hand

		# create a order which is different 
		order = []
		special = [self.game.settings["INVISIBLE"], self.game.settings["BURN"]]
		if self.game.minval == self.game.settings["LOWER"]:
			r = range(self.game.settings["LOWER"]+1)
		else:
			r = range(self.game.minval,13)
		for i in r:
			if i not in special:
				order.append(i)
		order.extend(special) # special cards are last

		indices = []
		for rank in order:
			indices = [i for i,x in enumerate(pcards) if x.rank==rank]
			if len(indices)>0:
				break
		return indices
