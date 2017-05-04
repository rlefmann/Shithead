from model.settings import Settings
from model.game import *
#from model.ai import *

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
		#self.ai = StraightforwardAI(self.game) # TODO: uncomment
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
			self._on_request_play(request)
		elif isinstance(request, RequestTake):
			self._on_request_take(request)
		elif isinstance(request, RequestTakeUpcards):
			self._on_request_take_upcards(request)
		else:
			raise Exception("the controller can't handle this request")

	def _on_request_initial_board(self):
		self.view.update(self.game.mode,
			# update heroes hand, upcards and downcards:
			phand=self.game.phand,
			pupcards=self.game.pupcards,
			pdowncards=self.game.pdowncards,
			# update villains hand, upcards and downcards:
			vhand=self.game.vhand,
			vupcards=self.game.vupcards,
			vdowncards=self.game.vdowncards,
			# update deck and discardpile:
			deck=self.game.deck,
			discardpile=self.game.discardpile)
		self.view.show_message("Good Luck")
		
	def _on_request_play(self, req):
		if self.game.is_possible_move(req):
			self.game.play(req)
			self.view.show_message("hero played {}".format(self.game.lastplayed))
			if self.game.is_win():
				self.view.show_message("we have a winner!")
				self.view.update(GameMode.FINISHED)
			self.game.switch_player()
			# update view:
			if req.src == SourceCollection.HAND:
				self.view.update(self.game.mode,phand=self.game.phand,deck=self.game.deck,discardpile=self.game.discardpile)
			elif req.src == SourceCollection.UPCARDS:
				self.view.update(self.game.mode,pupcards=self.game.pupcards,discardpile=self.game.discardpile)
			else:
				self.view.update(self.game.mode,pdowncards=self.game.pdowncards,discardpile=self.game.discardpile)
		elif req.src == SourceCollection.DOWNCARDS:
			# automatically take all the cards from the discard pile:
			self.game.take()
			# additionally take the downcard you wanted to play:
			self.game.take_downcard(req.indices[0])
			self.game.switch_player()
			self.view.update(self.game.mode,phand=self.game.phand,pdowncards=self.game.pdowncards,discardpile=self.game.discardpile)
			self.view.show_message("downcard doesnt fit")
			
	def _on_request_take(self, req):
		if self.game.is_possible_move(req):
			plays_from_up = self.game.curplayer.is_playing_from_upcards()
			self.game.take()
			if self.game.mode == GameMode.TAKE_UPCARDS:
				self.view.show_message("take upcards, too")
			else:
				self.game.switch_player()
			self.view.update(self.game.mode,phand=self.game.curhand,discardpile=self.game.discardpile)

	def _on_request_take_upcards(self, req):
		if self.game.is_possible_move(req):
			self.game.take_upcards(req.indices)
			self.view.update(GameMode.HAND,
				phand=self.game.curhand, # TODO: this should update also computer players hand
				pupcards=self.game.pupcards)
			self.view.show_message("")
			self.game.switch_player()

	def _villainmove(self):
		pass # TODO
