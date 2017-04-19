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
		self._update_cardspritegroup(self.game.players[0].hand, self.view.phand)
		self._update_cardspritegroup(self.game.players[0].downcards, self.view.pdown)
		self._update_cardspritegroup(self.game.players[0].upcards, self.view.pup)
		self._update_cardspritegroup(self.game.deck, self.view.deck)
		self._update_cardspritegroup(self.game.discardpile, self.view.dpile)
		self._update_cardspritegroup(self.game.players[1].hand, self.view.vhand)
		self._update_cardspritegroup(self.game.players[1].downcards, self.view.vdown)
		self._update_cardspritegroup(self.game.players[1].upcards, self.view.vup)
		
	def _update_cardspritegroup(self, modelsrc, viewdest):
		"""
		Creates a list of cardstrings from the modelsrc (a CardCollection)
		and updates the viewdest (a CardSpriteGroup) with them.
		"""
		cards = modelsrc.cardstrings() # get list of cardstrings
		viewdest.update(cards)
