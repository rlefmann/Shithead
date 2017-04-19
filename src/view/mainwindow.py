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
		# we start at the bottom with the player hand, downcards and upcards:
		xpos = MARGIN
		ypos = SCREENHEIGHT - 2*MARGIN - CARDHEIGHT
		self.phand = SpreadCards(xpos, ypos)
		xpos = int(SCREENWIDTH/2)
		ypos -= (CARDHEIGHT+MARGIN)
		self.pdown = LaidOutCards(xpos,ypos,alignment=Align.CENTER,visible=False)
		ypos -= OVERLAP
		self.pup = LaidOutCards(xpos,ypos,alignment=Align.CENTER,visible=True)
		
		# deck and discardpile:
		xpos = int(SCREENWIDTH/2) - CARDWIDTH - MARGIN
		ypos = int(SCREENHEIGHT/2) - int(CARDHEIGHT/2)
		self.deck = CardStack(xpos,ypos,visible=False)
		xpos += (CARDWIDTH + 2*MARGIN)
		self.dpile = CardStack(xpos,ypos,visible=True)
		
		# now we display villains hand, downcards and upcards:
		xpos = SCREENWIDTH - CARDWIDTH - MARGIN
		ypos = MARGIN
		self.vhand = SpreadCards(xpos, ypos, alignment=Align.RIGHT, visible=False)
		xpos = int(SCREENWIDTH/2)
		ypos += (CARDHEIGHT+MARGIN)
		self.vdown = LaidOutCards(xpos,ypos,alignment=Align.CENTER,visible=False)
		ypos += OVERLAP
		self.vup = LaidOutCards(xpos,ypos,alignment=Align.CENTER,visible=True)
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
		self.deck.draw(self.screen)
		self.dpile.draw(self.screen)
		self.vhand.draw(self.screen)
		self.vdown.draw(self.screen)
		self.vup.draw(self.screen)
		# draw the new frame:
		pg.display.flip()
