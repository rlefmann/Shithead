from shithead.model.settings import Settings
from shithead.model.game import *
from shithead.model.ai import StraightforwardAI
from shithead.gamemode import GameMode

from shithead.view.viewmode import ViewMode
from shithead.view.mainwindow import *

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
		self.game = Game(settings,numplayers=2)
		# create the ai that simulates the opponent player:
		# TODO: maybe other ai's should be allowed, too
		self.ai = StraightforwardAI(self.game) # TODO: uncomment
		self.view = MainWindow()
		# set the listener function:
		self.view.listener = self.on_request
		# start the game loop:
		self.view.run()
		
	def on_request(self, request):
		"""
		Here all the message handling is performed. The method determines
		what type of request was given to it and then performs the
		appropriate actions.
		"""
		# Check if a request was send and not sth else:
		if not isinstance(request, Request):
			raise Exception("something other than a request was send to the controller")

		# handle the different requests:
		if isinstance(request, RequestQuit):
			self.view.running = False
		elif isinstance(request, RequestInitialBoard):
			self._on_request_initial_board()
		elif isinstance(request, RequestAIMove):
			self._villainmove()
		elif isinstance(request, RequestMove):
			if request.move == Move.PLAY_HAND:
				self._on_request_play_handcards(request.playeridx, request.indices)
			elif request.move == Move.PLAY_UPCARDS:
				self._on_request_play_upcards(request.playeridx, request.indices)
			elif request.move == Move.PLAY_DOWNCARDS:
				self._on_request_play_downcards(request.playeridx, request.indices)
			elif request.move == Move.TAKE:
				self._on_request_take(request.playeridx)
			elif request.move == Move.TAKE_UPCARDS:
				self._on_request_take_upcards(request.playeridx, request.indices)
			else:
				raise Exception("the controller can't handle the move {}".format(request.move))
		else:
			raise Exception("the controller can't handle the request {}".format(request.name))

	def _on_request_initial_board(self):
		self._update_view()
		#~ self.view.update(self.game.mode,
			#~ # update heroes hand, upcards and downcards:
			#~ phand=self.game.phand,
			#~ pupcards=self.game.pupcards,
			#~ pdowncards=self.game.pdowncards,
			#~ # update villains hand, upcards and downcards:
			#~ vhand=self.game.vhand,
			#~ vupcards=self.game.vupcards,
			#~ vdowncards=self.game.vdowncards,
			#~ # update deck and discardpile:
			#~ deck=self.game.deck,
			#~ discardpile=self.game.discardpile)
		self.view.show_message("Good Luck")
	
	def _on_request_play_handcards(self, pidx, indices):
		if self.game.can_play_handcards(pidx, indices):
			self.game.play_handcards(pidx, indices)
			#self._update_view()
			self._after_play(pidx)
			#self.view.update(self.game.mode,phand=self.game.phand,deck=self.game.deck,discardpile=self.game.discardpile)

	def _on_request_play_upcards(self, pidx, indices):
		if self.game.can_play_upcards(pidx, indices):
			self.game.play_upcards(pidx, indices)
			#self._update_view()
			self._after_play(pidx)
			#self.view.update(self.game.mode,pupcards=self.game.pupcards,discardpile=self.game.discardpile)
			

	def _on_request_play_downcards(self, pidx, indices):
		if self.game.can_play_downcards(pidx, indices):
			self.game.play_downcards(pidx, indices)
			#self._update_view()
			self._after_play(pidx)
			#self.view.update(self.game.mode,pdowncards=self.game.pdowncards,discardpile=self.game.discardpile)
		elif len(indices) == 1: # failed to play downcard
			# automatically take all the cards from the discard pile:
			self.game.take()
			# additionally take the downcard you wanted to play:
			self.game.take_downcard(indices[0])
			#self.game.switch_player()
			#self.view.update(self.game.mode,phand=self.game.phand,pdowncards=self.game.pdowncards,discardpile=self.game.discardpile)
			self._update_view()
			self.view.show_message("downcard doesnt fit")
			if self.game.curplayeridx == 1:
				self._villainmove()

	def _after_play(self, pidx):
		"""
		After a player has played a card, the following things happen.
		"""
		# show a message what cards were played:
		if pidx == 0:
			self.view.show_message("hero played {}".format(self.game.lastplayed))
		else:
			self.view.show_message("villain played {}".format(self.game.lastplayed))
		# check if the game is finished:
		if self.game.has_won(pidx):
			if pidx == 0:
				self.view.show_message("hero wins!")
			else:
				self.view.show_message("villain wins!")
			self.view.update(ViewMode.FINISHED)
			self._update_view()
			return
		self._update_view()
		if self.game.curplayeridx == 1:
			self._villainmove()
			#self.game.switch_player()
		
	def _on_request_take(self, pidx):
		if self.game.can_take(pidx):
			#plays_from_up = self.game.curplayer.is_playing_from_upcards() # TODO: necessary?
			turn_ended = self.game.take()
			#if self.game.mode == GameMode.TAKE_UPCARDS:
			if not turn_ended:
				self.view.show_message("take upcards, too")
				if self.game.curplayeridx == 1:
					self._villainmove()
			#else:
				#self.game.switch_player()
			if pidx == 0:
				self.view.show_message("hero takes")
			else:
				self.view.show_message("villain takes")
			self._update_view()
			if self.game.curplayeridx == 1:
				self._villainmove()
			#self.view.update(self.game.mode,phand=self.game.curhand,discardpile=self.game.discardpile)

	def _on_request_take_upcards(self, pidx, indices): # TODO: remove req
		if self.game.can_take_upcards(pidx, indices):
			self.game.take_upcards(indices)
			self._update_view()
			self.view.show_message("")
			if self.game.curplayeridx == 1:
				self._villainmove()

	def _villainmove(self):
		req = self.ai.think()
		if not isinstance(req, RequestMove):
			raise TypeError("ai should always return a move request, but got {}.".format(type(req)))
		self.on_request(req)

	def _update_view(self):
		if self.game.curplayeridx == 1:
			m = ViewMode.VILLAIN_MOVE
		elif self.game.mode == GameMode.HAND:
			m = ViewMode.HERO_PLAYS_HAND
		elif self.game.mode == GameMode.UPCARDS:
			m = ViewMode.HERO_PLAYS_UPCARDS
		elif self.game.mode == GameMode.DOWNCARDS:
			m = ViewMode.HERO_PLAYS_DOWNCARDS
		elif self.game.mode == GameMode.TAKE_UPCARDS:
			m = ViewMode.HERO_TAKES_UPCARDS
		else:
			m = ViewMode.FINISHED
		
		self.view.update(m,
			phand = self.game.phand,
			pupcards = self.game.pupcards,
			pdowncards = self.game.pdowncards,
			vhand = self.game.vhand,
			vupcards = self.game.vupcards,
			vdowncards = self.game.vdowncards,
			deck = self.game.deck,
			discardpile = self.game.discardpile
		)

	def next_player(self): # TODO: remove?
		self.game.switch_player()
		if self.game.curplayeridx == 1:
			# villain move:
			req = self.ai.think()
			if not isinstance(req, RequestMove):
				raise TypeError("ai should always return a move request, but got {}.".format(type(req)))
			self.on_request(req)
