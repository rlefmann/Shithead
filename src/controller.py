from model.settings import Settings
from model.game import *
from model.ai import *

from view.mainwindow import *

class Controller:
	"""
	The Controller is the center piece of the program. It creates an
	instance of the game model and the view (mainwindow). The computer
	player (ai) is initialized here, too.
	"""
	def __init__(self):
		"""
		Sets up a new controller and creates model and view.

		A Game object is created, as well as a view object. The class
		method `on_view_event` is added as listener and the main loop
		of the PyGame window is started by calling `run`.
		"""
		# Create a settings object with default values
		# TODO: allow to change these values?
		settings = Settings()
		# the model:
		self.game = Game(settings)
		# create the ai that simulates the opponent player:
		# TODO: maybe other ai's should be allowed, too
		self.ai = StraightforwardAI(self.game)
		self.view = MainWindow()
		# set the listener function:
		self.view.listener = self.on_request
		# start the game loop:
		self.view.run()
		
	def on_request(self, request):
		"""
		Here all the message handling is performed. The method determines what type of request was given to it and then performs the appropriate actions.
		"""
		
		# Check if a request was send and not sth else:
		if not isinstance(request, Request):
			raise Exception("something other than a request was send to the controller")

		print request.name

		# handle the different requests:
		if isinstance(request, RequestQuit):
			self.view.running = False
		elif isinstance(request, RequestInitialBoard):
			self._on_request_initial_board()
		elif isinstance(request, RequestPlay):
			pass # TODO: handle request
		elif isinstance(request, RequestTake):
			pass # TODO: handle request
		else:
			raise Exception("the controller can't handle this request")

	def _on_request_initial_board(self):
		phand = self.game.players[0].hand # get heroes hand
		cards = [str(c) for c in phand] # get list of cardstrings
		self.view.phand.update(cards)
		pdown = self.game.players[0].downcards
		cards = [str(c) for c in pdown]
		self.view.pdown.update(cards)
		pup = self.game.players[0].upcards
		cards = [str(c) for c in pup]
		self.view.pup.update(cards)
