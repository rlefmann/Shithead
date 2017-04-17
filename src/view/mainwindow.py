import pygame as pg

from constants import *
from 

class MainWindow:
	"""
	The main window of the application.
	"""
	def __init__(self):
		# The listener function. Will be set by the controller.
		self.listener = None
		# The clock allows the game to run at a fixed framerate
		self.clock = pg.time.Clock()
		# create Surface object for displaying content:
		self.screen = pg.display.set_mode(SCREENSIZE)
		pg.display.set_caption(TITLE)
		# determines whether the main loop (see method run)
		# is executed further. Will be set to false by the
		# controller, when a QuitRequest is send.
		self.running = True
		self._create_sprites()

	def _create_sprites(self):
		"""
		"""
		pass # TODO: implement

	def run(self):
		"""
		The main loop of the game and handling of key presses.
		"""
		# The first thing that is send to the controller
		# is the request for the initial board:
		self.listener(RequestInitialBoard())
		# Main loop:
		while self.running:
			self.clock.tick(FRAMERATE)
			for event in pg.event.get():
				pass
