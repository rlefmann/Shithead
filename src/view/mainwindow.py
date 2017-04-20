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
		self.phandcursor = Cursor(PHANDCURSOR_X,PHANDCURSOR_Y)
		self.pupcursor = SlotCursor(PUPCURSOR_X,PUPCURSOR_Y, stepwidth=PUPDOWNCURSOR_STEPWIDTH)
		self.pdowncursor = SlotCursor(PDOWNCURSOR_X,PDOWNCURSOR_Y, stepwidth=PUPDOWNCURSOR_STEPWIDTH)
		self.pdowncursor.active = False
		self.dpilecursor = Cursor(DPILECURSOR_X, DPILECURSOR_Y) # stepwidth doesnt matter because there is only one cursor position
		self.dpilecursor.active = False
		# create list of all cursors:
		self.cursors = [self.phandcursor, self.pupcursor, self.pdowncursor, self.dpilecursor]
		self.cur_cursor_idx = 0 # the index of the current cursor
		# This spritegroup only contains the active cursor:
		self.activecursor = pg.sprite.Group()
		self.activecursor.add(self.phandcursor)
		
		
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
				# switch the cursor with tab key:
				elif event.type == pg.KEYDOWN and event.key == pg.K_TAB:
					self.switchcursor()
				elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
					self.cursors[self.cur_cursor_idx].moveleft()
					self.update()
				elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
					self.cursors[self.cur_cursor_idx].moveright()
					self.update()
				if req:
					self.listener(req)
				self.update()

	def update_phand(self, cardstrs):
		"""
		Updates the players hand with a new list of cardstrings.
		"""
		self.phand.update(cardstrs)
		self.cursors[0].setnumsteps(len(cardstrs))

	def update_pupcards(self, cardstrs):
		"""
		Update the players upcards with a new list of cardstrings.
		"""
		cardstrs[2] = "xx" # TODO: remove
		self.pup.update(cardstrs)
		self.pupcursor.empty_slots = self.pup.empty_slots
		self.pupcursor.setnumsteps(len(cardstrs))

	def update_pdowncards(self, cardstrs):
		"""
		Update the players downcards with a new list of cardstrings.
		"""
		self.pdown.update(cardstrs)
		self.pdowncursor.empty_slots = self.pdown.empty_slots
		self.pdowncursor.setnumsteps(len(cardstrs))

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
		self.activecursor.update() # TODO: necessary?
		self.activecursor.draw(self.screen)
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
		
	def switchcursor(self):
		"""
		Switches to the next cursor in self.cursors. If we are already at
		the last one, we begin again with the first.
		"""
		self.cur_cursor_idx = (self.cur_cursor_idx+1)%len(self.cursors)
		if self.cursors[self.cur_cursor_idx].active:
			self.activecursor.empty()
			self.activecursor.add(self.cursors[self.cur_cursor_idx])
			self.cursors[self.cur_cursor_idx].reset()
		else:
			self.switchcursor() # TODO: avoid infinite loop when all cursors are deactivated
		
