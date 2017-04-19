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
		
		
