import pygame as pg

from constants import *
from cardspritegroups import CardSpriteGroup

class Cursor(pg.sprite.Sprite):
	"""
	A cursor for selecting cards from a CardSpriteGroup.
	"""
	def __init__(self, xpos, ypos, stepwidth=OVERLAP, numsteps=1):
		super(Cursor, self).__init__()
		self.image = pg.image.load("./img/cursor.png").convert_alpha()
		self.image = pg.transform.scale(self.image, (CURSORWIDTH,CURSORHEIGHT))
		self.stepwidth = stepwidth
		self.numsteps = numsteps
		self.active = True
		self.curstep = 0
		self.rect = self.image.get_rect()
		self.basex = xpos # we keep this for resetting the cursor
		self.rect.x = xpos
		self.rect.y = ypos
		self._cardspritegroup = None

	@property
	def cardspritegroup(self):
		return self._cardspritegroup

	@cardspritegroup.setter
	def cardspritegroup(self, newgroup):
		if not isinstance(newgroup, CardSpriteGroup):
			raise TypeError("you need to assign a cardspritegroup to the cursor")
		self._cardspritegroup = newgroup
		
	def setnumsteps(self,numsteps):
		"""
		Sets the number of positions the cursor can have.
		"""
		self.numsteps = numsteps
		
	def moveleft(self):
		"""
		Moves the cursor one position to the left.
		"""
		if self.curstep > 0:
			self.rect.x -= self.stepwidth
			self.curstep -= 1
			
	def moveright(self):
		"""
		Moves the cursor one position to the right.
		"""
		if self.curstep < self.numsteps-1:
			self.rect.x += self.stepwidth
			self.curstep += 1

	def reset(self):
		"""
		Resets the cursor to the initial position.
		"""
		self.rect.x = self.basex
		self.curstep = 0

class SlotCursor(Cursor):
	"""
	A special cursor for CardSpriteGroups which may have empty slots
	(in the case of shithead those are just LaidOutCards)
	"""
	def __init__(self, xpos, ypos, stepwidth=OVERLAP, numsteps=1):
		super(SlotCursor, self).__init__(xpos, ypos, stepwidth, numsteps)
		# the indices of the empty slots:
		self.empty_slots = []

	def moveleft(self):
		i = self.curstep - 1
		while i in self.empty_slots:
			i-=1
		if i >= 0:
			self.rect.x -= self.stepwidth*(self.curstep-i)
			self.curstep = i

	def moveright(self):
		i = self.curstep+1
		while i in self.empty_slots:
			i+=1
		if i < self.numsteps:
			self.rect.x += self.stepwidth*(i-self.curstep)
			self.curstep = i

	def reset(self):
		"""
		Resets the cursor to point at the leftmost nonempty slot.
		TODO: what happens if all the slots are empty?
		"""
		super(SlotCursor,self).reset()
		i = 0
		while i in self.empty_slots:
			self.moveright() 


class CursorManager(object):
	
	def __init__(self):
		self.cursors = []
		self.current_cursor_idx = 0
		self.selected = [] # TODO
		# if the cursormanager is blocked you cannot switch between
		# cursors:
		self.blocked = False
			
	def add(self, cursor):
		self.cursors.append(cursor)
	
	@property
	def current_cursor(self):
		return self.cursors[self.current_cursor_idx]
	
	@property
	def current_idx(self):
		return self.current_cursor_idx
		
	def switchcursor(self):
		"""
		Switches to the next cursor in self.cursors. If we are already at
		the last one, we begin again with the first.
		"""
		self.current_cursor_idx = (self.current_cursor_idx+1)%len(self.cursors)
		if self.cursors[self.current_cursor_idx].active:
			self.cursors[self.current_cursor_idx].reset()
		else:
			self.switchcursor() # TODO: avoid infinite loop when all cursors are deactivated

	def select_card(self):
		cardspritegroup = self.current_cursor.cardspritegroup
		if cardspritegroup == None:
			raise ValueError("Cardspritegroup of current cursor is None")
		idx = self.current_cursor.curstep
		sprite = cardspritegroup[idx]
		sprite.sethighlighted(not sprite.highlighted)
		
		
	
