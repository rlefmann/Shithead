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
		elif isinstance(request, RequestMove):
			if request.move == Move.PLAY_HAND:
				self._on_request_play_handcards(request.indices)
			elif request.move == Move.PLAY_UPCARDS:
				self._on_request_play_upcards(request.indices)
			elif request.move == Move.PLAY_DOWNCARDS:
				self._on_request_play_downcards(request.indices)
			elif request.move == Move.TAKE:
				self._on_request_take(request)
			elif request.move == Move.TAKE_UPCARDS:
				self._on_request_take_upcards(request)
			else:
				raise Exception("the controller can't handle the move {}".format(request.move))
		else:
			raise Exception("the controller can't handle the request {}".format(request.name))

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
	
	def _on_request_play_handcards(self, indices):
		if self.game.can_play_handcards(indices):
			self.game.play_handcards(indices)
			self._after_play()
			self.view.update(self.game.mode,phand=self.game.phand,deck=self.game.deck,discardpile=self.game.discardpile)

	def _on_request_play_upcards(self, indices):
		if self.game.can_play_upcards(indices):
			self.game.play_upcards(indices)
			self._after_play()
			self.view.update(self.game.mode,pupcards=self.game.pupcards,discardpile=self.game.discardpile)

	def _on_request_play_downcards(self, indices):
		if self.game.can_play_downcards(indices):
			self.game.play_downcards(indices)
			self._after_play()
			self.view.update(self.game.mode,pdowncards=self.game.pdowncards,discardpile=self.game.discardpile)
		elif len(indices) == 1: # failed to play downcard
			# automatically take all the cards from the discard pile:
			self.game.take()
			# additionally take the downcard you wanted to play:
			self.game.take_downcard(indices[0])
			self.game.switch_player()
			self.view.update(self.game.mode,phand=self.game.phand,pdowncards=self.game.pdowncards,discardpile=self.game.discardpile)
			self.view.show_message("downcard doesnt fit")

	def _after_play(self):
		"""
		After a player has played a card, the following things happen.
		"""
		# show a message what cards were played:
		self.view.show_message("hero played {}".format(self.game.lastplayed))
		# check if the game is finished:
		if self.game.is_win():
			self.view.show_message("we have a winner!")
			self.view.update(GameMode.FINISHED)
		# switch the player:
		self.game.switch_player()

	def _on_request_take(self, req):
		if self.game.can_take():
			plays_from_up = self.game.curplayer.is_playing_from_upcards() # TODO: necessary?
			self.game.take()
			if self.game.mode == GameMode.TAKE_UPCARDS:
				self.view.show_message("take upcards, too")
			else:
				self.game.switch_player()
			self.view.update(self.game.mode,phand=self.game.curhand,discardpile=self.game.discardpile)

	def _on_request_take_upcards(self, req):
		if self.game.can_take_upcards(req.indices):
			self.game.take_upcards(req.indices)
			self.view.update(GameMode.HAND,
				phand=self.game.curhand, # TODO: this should update also computer players hand
				pupcards=self.game.pupcards)
			self.view.show_message("")
			self.game.switch_player()

	def _villainmove(self):
		pass # TODO
