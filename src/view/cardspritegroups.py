import pygame as pg
from enum import Enum

from cardsprite import *
from constants import *

# a card sprite group has only got to be updated, if a card from it is removed or a new card is added

class Align(Enum):
	"""
	The different alignments a card sprite group can have
	"""
	LEFT=1
	RIGHT=2
	CENTER=3
	STACK=4


def CardSpriteGroup(pg.sprite.OrderedUpdates):
	"""
	A basic group of card sprites. Inherits from OrderedUpdates so that the overlapping of cards is displayed correctly.
	"""
	def __init__(self,xpos,ypos,alignment=Align.LEFT,visible=True):
		super(CardSpriteGroup, self).__init__()
		self.xpos = xpos
		self.ypos = ypos
		self.spritelist = []
		self.visible = visible
		if not self.alignment_allowed(alignment):
			raise Exception("alignment not allowed for this CardSpriteGroup")
		self.alignment = alignment

	def alignment_allowed(self, alignment):
		"""
		Not all alignments are allowed for every type of
		CardSpriteGroup. For the base class all alignments
		are allowed.
		"""
		return True
		
	def update(self, cards):
		# TODO: do we have to implement this?
		pass
