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
		self.curstep = 0
		self.rect = self.image.get_rect()
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
		
