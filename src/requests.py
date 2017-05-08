# These are the classes needed for communication between the components
# of the MVC framework.

from enum import Enum

# TODO: remove?
#collectionstrings = ["phand","pupcards","pdowncards","vhand","vdowncards","deck","discardpile","graveyard"]

# Requests are what is send by the controller between the model and the view and are the basic messages of the mvc pattern


#~ class SourceCollection(Enum):
	#~ """
	#~ For a play request, the player can play cards from his hand,
	#~ from his upcards, or from his downcards.
	#~ """
	#~ HAND = 1
	#~ UPCARDS = 2
	#~ DOWNCARDS = 3

class Request:
	"""A generic request that is the base class of all other requests."""
	def __init__(self):
		self.name = "generic request"

class Move(Enum):
	PLAY_HAND = 1
	PLAY_UPCARDS = 2
	PLAY_DOWNCARDS = 3
	TAKE = 4
	TAKE_UPCARDS = 5

class RequestMove(Request):
	def __init__(self, move, indices):
		self.name = "request move"
		if not isinstance(move, Move):
			raise TypeError("the move parameter must be of type Move")
		self.move = move
		self.indices = indices

	@classmethod
	def play_from_hand(cls, indices):
		if len(indices) == 0:
			raise Exception("a play request requires at least one index")
		return cls(Move.PLAY_HAND, indices)

	@classmethod
	def play_from_upcards(cls, indices):
		if len(indices) == 0:
			raise Exception("a play request requires at least one index")
		return cls(Move.PLAY_UPCARDS, indices)

	@classmethod
	def play_from_downcards(cls, indices):
		if len(indices) == 0:
			raise Exception("a play request requires at least one index")
		return cls(Move.PLAY_DOWNCARDS, indices)

	@classmethod
	def take(cls):
		"""
		This is a request by the view to the model to take all of the cards 
		from the discard pile into the players hand.
		"""
		return cls(Move.TAKE, [])

	@classmethod
	def take_upcards(cls, indices):
		"""
		This is a request by the view to the model to take cards of the same
		rank from the upcards into the players hand.
		"""
		if len(indices) == 0:
			raise Exception("a take upcards request requires at least one index")
		return cls(Move.TAKE_UPCARDS, indices)


class RequestQuit(Request):
	"""
	The program should end after creating this request.

	It is created, when the pygame window is closed or when the escape button is pressed.
	"""
	def __init__(self):
		self.name = "request quit"


class RequestInitialBoard(Request):
	"""
	When started, the view requests the mode to provide
	the initial board setup.
	"""
	def __init__(self):
		self.name = "request initial board"


#~ class RequestPlay(Request):
	#~ """
	#~ This is a request by the view to the model to play the currently selected cards.

	#~ The cards are handed to the request via the `indices` argument of the constructor.
	#~ represents playing a certain amount of indices
	#~ (specified by indices) from a players hand, his upcards or
	#~ downcards (specified by srctype)
	#~ """
	#~ def __init__(self, src, indices):
		#~ self.name = "request play"
		#~ if not isinstance(src, SourceCollection):
			#~ raise TypeError("the src of a request must be of type SourceCollection")
		#~ if len(indices) == 0:
			#~ raise Exception("a play request requires at least one index")
		#~ self.src = src
		#~ self.indices = indices

#~ class RequestTake(Request):
	#~ """
	#~ This is a request by the view to the model to take all of the cards 
	#~ from the discard pile into the players hand.
	#~ """
	#~ def __init__(self):
		#~ self.name = "request take"


#~ class RequestTakeUpcards(Request):
	#~ """
	#~ This is a request by the view to the model to take cards of the same
	#~ rank from the upcards into the players hand.
	#~ """
	#~ def __init__(self, indices):
		#~ self.name = "request take upcards"
		#~ if len(indices) == 0:
			#~ raise Exception("a take upcards request requires at least one index")
		#~ self.indices = indices
