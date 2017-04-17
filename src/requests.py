# Requests are what is send by the controller between the model and the view and are the basic messages of the mvc pattern


class Request:
	"""A generic request that is the base class of all other requests."""
	def __init__(self):
		self.name = "generic request"


class RequestQuit(Request)
	"""
	The program should end after creating this request.

	It is created, when the pygame window is closed or when the escape
	button is pressed.
	"""
	def __init__(self):
		self.name = "Quit request"


class RequestInitialBoard(Request):
	"""
	When started, the view requests the mode to provide
	the initial board setup.
	"""
	def __init__(self):
		self.name = "request initial board"


class RequestPlay(Request):
	"""
	This is a request by the view to the model to play the currently selected cards.

	The cards are handed to the request via the `indices` argument of the constructor.
	"""
	def __init__(self, indices):
		self.name = "request play"
		self.indices = indices


class RequestTake(Request):
	"""
	This is a request by the view to the model to take all the cards from the discard pile into the players hand.
	"""
	def __init__(self):
		self.name = "request take"
