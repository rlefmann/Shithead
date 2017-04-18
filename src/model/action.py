from enum import Enum

class AType(Enum):
	"""
	The type of action is either play or take.
	"""
	PLAY = 1
	TAKE = 2

class SourceType(Enum):
	"""
	If the actiontype is play, the player can play cards from his hand,
	from his upcards, or from his downcards. If the action is 
	"""
	HAND = 1
	UPCARDS = 2
	DOWNCARDS = 3

class Action:
	"""
	An Action is to either play some cards from your had or to take the
	whole discard pile up into your hand. This class serves as a base
	class for its subclasses TakeAction and PlayAction and should not
	be used by itself.
	"""
	def __init__(self, atype):
		self.atype = atype

class TakeAction(Action):
	def __init__(self):
		super(self.__class__, self).__init__(AType.TAKE)

class PlayAction(Action):
	def __init__(self, srctype, indices):
		super(self.__class__, self).__init__(AType.PLAY)
		if len(indices) == 0:
			raise Exception("action play requires at least one index")
		self.srctype = srctype
		self.indices = indices
