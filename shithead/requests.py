# These are the classes needed for communication between the components
# of the MVC framework.

from enum import Enum


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

	def __init__(self, playeridx, move, indices):
		self.name = "request move"
		if not isinstance(move, Move):
			raise TypeError("the move parameter must be of type Move")
		self.playeridx = playeridx
		self.move = move
		self.indices = indices

	@classmethod
	def play_from_hand(cls, playeridx, indices):
		if len(indices) == 0:
			raise Exception("a play request requires at least one index")
		return cls(playeridx, Move.PLAY_HAND, indices)

	@classmethod
	def play_from_upcards(cls, playeridx, indices):
		if len(indices) == 0:
			raise Exception("a play request requires at least one index")
		return cls(playeridx, Move.PLAY_UPCARDS, indices)

	@classmethod
	def play_from_downcards(cls, playeridx, indices):
		if len(indices) == 0:
			raise Exception("a play request requires at least one index")
		return cls(playeridx, Move.PLAY_DOWNCARDS, indices)

	@classmethod
	def take(cls, playeridx):
		"""
		This is a request by the view to the model to take all of the cards
		from the discard pile into the players hand.
		"""
		return cls(playeridx, Move.TAKE, [])

	@classmethod
	def take_upcards(cls, playeridx, indices):
		"""
		This is a request by the view to the model to take cards of the same
		rank from the upcards into the players hand.
		"""
		if len(indices) == 0:
			raise Exception("a take upcards request requires at least one index")
		return cls(playeridx, Move.TAKE_UPCARDS, indices)


class RequestAIMove(Request):
	def __init__(self):
		self.name = "request ai move"


class RequestQuit(Request):
	"""
	The program should end after creating this request.

	It is created, when the pygame window is closed or when the escape
	button is pressed.
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
