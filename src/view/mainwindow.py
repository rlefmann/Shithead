import pygame as pg

from constants import *
from ..requests import *
from cardspritegroups import *

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
		self.screen = pg.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
		pg.display.set_caption(TITLE)
		# determines whether the main loop (see method run) is executed further. Will be set to false by the controller, when a QuitRequest is send.
		self.running = True
		self._create_sprites()

	def _create_sprites(self):
		"""
		"""
		# we start at the bottom with the player hand:
		xpos = MARGIN
		ypos = SCREENHEIGHT - 2*MARGIN - CARDHEIGHT
		self.phand = SpreadCards(xpos, ypos)
		xpos = int(SCREENWIDTH/2)
		ypos -= (CARDHEIGHT+MARGIN)
		self.pdown = LaidOutCards(xpos,ypos,alignment=Align.CENTER,visible=False)
		ypos -= OVERLAP
		self.pup = LaidOutCards(xpos,ypos,alignment=Align.CENTER,visible=True)
		self.update()

	def run(self):
		"""
		The main loop of the game and handling of key presses.
		"""
		# The first thing that is send to the controller is the request for the initial board:
		self.listener(RequestInitialBoard())
		# Main loop:
		while self.running:
			self.clock.tick(FRAMERATE)
			for event in pg.event.get():
				req = None
				if event.type == pg.QUIT:
					req = RequestQuit()
				elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					req = RequestQuit()
				if req:
					self.listener(req)
				self.update()

	def update(self):
		"""
		Updates all the spritegroups and redraws the screen:
		"""
		self.screen.fill(GREEN)
		self.phand.draw(self.screen)
		self.pdown.draw(self.screen)
		self.pup.draw(self.screen)
		# draw the new frame:
		pg.display.flip()
