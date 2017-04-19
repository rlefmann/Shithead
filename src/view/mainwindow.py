import pygame as pg

from constants import *
from ..requests import *
from cardspritegroups import *
from cursor import Cursor

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
		self._create_cursors()
		self.update()

	def _create_sprites(self):
		"""
		"""
		# we start at the bottom with the player hand, downcards and upcards:
		self.phand = SpreadCards(PHAND_X, PHAND_Y)
		self.pdown = LaidOutCards(PDOWN_X,PDOWN_Y,alignment=Align.LEFT,visible=False)
		self.pup = LaidOutCards(PUP_X,PUP_Y,alignment=Align.LEFT,visible=True)
		
		# deck and discardpile:
		self.deck = CardStack(DECK_X,DECK_Y,visible=False)
		self.dpile = CardStack(DPILE_X,DPILE_Y,visible=True)
		
		# now we display villains hand, downcards and upcards:
		self.vhand = SpreadCards(VHAND_X, VHAND_Y, alignment=Align.RIGHT, visible=False)
		self.vdown = LaidOutCards(VDOWN_X,VDOWN_Y,alignment=Align.RIGHT,visible=False)
		self.vup = LaidOutCards(VUP_X,VUP_Y,alignment=Align.RIGHT,visible=True)
		
	def _create_cursors(self):
		# SpriteGroup for all cursors:
		self.cursors = pg.sprite.Group()
		xpos = MARGIN
		ypos = PHAND_Y - CURSORHEIGHT
		self.phand_cursor = Cursor(xpos,ypos)
		self.cursors.add(self.phand_cursor)

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
		self.cursors.update()
		self.cursors.draw(self.screen)
		self.phand.draw(self.screen)
		self.pdown.draw(self.screen)
		self.pup.draw(self.screen)
		self.deck.draw(self.screen)
		self.dpile.draw(self.screen)
		self.vhand.draw(self.screen)
		self.vdown.draw(self.screen)
		self.vup.draw(self.screen)
		# draw the new frame:
		pg.display.flip()
