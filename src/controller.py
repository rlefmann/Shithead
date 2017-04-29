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
		# update heroes hand, upcards and downcards:
		self.view.update_phand(self.game.phand)
		self.view.update_pupcards(self.game.pupcards)
		self.view.update_pdowncards(self.game.pdowncards)
		# update villains hand, upcards and downcards:
		self.view.update_vhand(self.game.vhand)
		self.view.update_vupcards(self.game.vupcards)
		self.view.update_vdowncards(self.game.vdowncards)
		# update deck and discardpile:
		self.view.update_deck(self.game.deck)
		self.view.update_discardpile(self.game.discardpile)
		
	def _on_request_play(self, req):
		if self.game.is_possible_move(req):
			self.game.play(req)
			if self.game.is_win() != -1:
				print "we have a winrar!"
			self.view.cursor._unhighlight_all() # TODO:
			# update view:
			self.view.update_discardpile(self.game.discardpile)
			if req.src == SourceCollection.HAND:
				self.view.update_phand(self.game.phand)
			elif req.src == SourceCollection.UPCARDS:
				self.view.update_pupcards(self.game.pupcards)
			else:
				self.view.update_pdowncards(self.game.pdowncards)
			self.view.reset_cursor()
		elif req.src == SourceCollection.DOWNCARDS:
			# automatically take all the cards from the discard pile:
			self.game.take()
			# additionally take the downcard you wanted to play:
			self.game.take_downcard(req.indices[0])
			self.view.cursor._unhighlight_all() # TODO:
			self.view.update_phand(self.game.phand)
			self.view.update_pdowncards(self.game.pdowncards)
			self.view.update_discardpile(self.game.discardpile)
			self.view.reset_cursor()
			
	def _on_request_take(self, req):
		if self.game.is_possible_move(req):
			if self.game.curplayer.is_playing_from_upcards():
				print "here we need to take some upcards, too"
			self.game.take()
			self.view.cursor._unhighlight_all() # TODO:
			self.view.update_discardpile(self.game.discardpile)
			self.view.update_phand(self.game.curhand)
			self.view.reset_cursor()
			
	def _on_request_take_upcards(self, req):
		if self.game.is_possible_move(req):
			print "TODO" # TODO
