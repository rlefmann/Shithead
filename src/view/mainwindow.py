import pygame as pg

from constants import *
from ..requests import *
from cardspritegroups import *
from cursor import *

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
		#self.update()

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
		
	def _create_cursor(self):
		spritegroups_with_cursor = [self.phand, self.pup, self.pdown, self.dpile]
		self.cursor = Cursor(spritegroups_with_cursor)
		self.cursor.toggle_inactive(2) # downcards inactive
		# This is the spritegroup necessary to display the cursor:
		self.current_cursor = pg.sprite.Group()
		self.current_cursor.add(self.cursor)
		# TODO: this can be put into a global spritegroup
		
	def run(self):
		"""
		The main loop of the game and handling of key presses.
		"""
		# The first thing that is send to the controller is the request for the initial board:
		self.listener(RequestInitialBoard())
		self._create_cursor()
		# Main loop:
		while self.running:
			self.clock.tick(FRAMERATE)
			for event in pg.event.get():
				req = None
				if event.type == pg.QUIT:
					req = RequestQuit()
				elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					req = RequestQuit()
				# switch between active cursors using the tab key:
				elif event.type == pg.KEYDOWN and event.key == pg.K_TAB:
					self.cursor.next_group()
				# move cursor to the left:
				elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
					self.cursor.moveleft()
					self.update()
				# move cursor to the right:
				elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
					self.cursor.moveright()
					self.update()
				elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
					self.cursor.toggle_highlighted()
				elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
					indices = self.cursor.selected_indices
					if len(indices) > 0:
						g = self.cursor.curgroup 
						if g == self.phand:
							req = RequestPlay(SourceCollection.HAND, indices)
						elif g == self.pup:
							req = RequestPlay(SourceCollection.UPCARDS, indices)
						elif g == self.pdown:
							req = RequestPlay(SourceCollection.DOWNCARDS, indices)
						elif g == self.dpile:
							req = RequestTake()
						else:
							raise Error("you cannot do this!") # TODO: more descriptive message
				# send request to controller:
				if req:
					self.listener(req)
				self.update()	
	
	def update_phand(self, cardstrs):
		"""
		Updates the players hand with a new list of cardstrings.
		"""
		self.phand.update(cardstrs)

	def update_pupcards(self, cardstrs):
		"""
		Update the players upcards with a new list of cardstrings.
		"""
		self.pup.update(cardstrs)

	def update_pdowncards(self, cardstrs):
		"""
		Update the players downcards with a new list of cardstrings.
		"""
		self.pdown.update(cardstrs)
		#self.pdowncursor.empty_slots = self.pdown.empty_slots
		#self.pdowncursor.setnumsteps(len(cardstrs))

	def update_vhand(self, cardstrs):
		"""Updates the villains hand with a new list of cardstrings."""
		self.vhand.update(cardstrs)

	def update_vupcards(self, cardstrs):
		"""Update the villains upcards with a new list of cardstrings."""
		self.vup.update(cardstrs)

	def update_vdowncards(self, cardstrs):
		"""Update the villains downcards with a new list of cardstrings."""
		self.vdown.update(cardstrs)

	def update_deck(self, cardstrs):
		"""Updates the deck with a new list of cardstrings."""
		self.deck.update(cardstrs)

	def update_discardpile(self, cardstrs):
		"""Updates the discardpile with a new list of cardstrings."""
		self.dpile.update(cardstrs)
	
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
		self.current_cursor.update() # TODO: necessary?
		self.current_cursor.draw(self.screen)
		# draw the new frame:
		pg.display.flip()

	def reset_cursor(self):
		self.cursor.reset()
