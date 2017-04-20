import pygame as pg

from constants import *

class Cursor(pg.sprite.Sprite):
	"""
	A cursor for selecting cards from a CardSpriteGroup.
	"""
	def __init__(self, xpos, ypos, stepwidth=OVERLAP, numsteps=1):
		super(Cursor, self).__init__()
		self.image = pg.image.load("./img/cursor.png").convert_alpha()
		self.image = pg.transform.scale(self.image, (20,20))
		self.stepwidth = stepwidth
		self.numsteps = numsteps
		self.active = True
		self.curstep = 0
		self.rect = self.image.get_rect()
		self.basex = xpos # we keep this for resetting the cursor
		self.rect.x = xpos
		self.rect.y = ypos
	
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
