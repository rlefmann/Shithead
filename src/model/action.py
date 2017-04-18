from enum import Enum

class AType(Enum):
	PLAY = 1
	TAKE = 2

class Action:
	"""
	An Action is to either play some cards from your had or to take the whole discard pile up into your hand.
	"""
	def __init__(self, atype, indices = []):
		if atype == AType.TAKE and len(indices)>0:
			raise Exception("action take requires an empty list of indices")
		elif atype == AType.PLAY and len(indices) == 0:
			raise Exception("action play requires at least one index")
		self.atype = atype
		self.indices = indices
