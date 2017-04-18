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
		# this is a separate list of sprites we need to keep:
		# TODO: what for?
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


def SpreadCards(CardSpriteGroup):
	"""
	Cards that are spread out on the table such that they overlap by a certain amount specified in the constant OVERLAP. These can be either hidden (for opponents cards) or visible. The alignment can be either left or right aligned. If it is left aligned the xpos is the x-position of the leftmost card, otherwise the x-position of the rightmost card.
	"""
	def __init__(self,xpos,ypos,alignment=Align.LEFT,visible=True):
		super(SpreadCards, self).__init__(xpos,ypos,alignment,visible)

	def alignment_allowed(self, alignment):
		"""
		Spread out cards can only be aligned to the left or to the right.
		"""
		return alignment in [Align.LEFT, Align.RIGHT]

	def update(self, cards):
		"""
		Draws the cards to the screen. The argument cards is a list of strings representing cards.
		"""
		# empty the sprite list:
		self.spritelist = []
		# remove all previous sprites:
		self.empty()
		# the xpos of the next card to be drawn:
		curxpos = self.xpos 
		for cardstr in cards:
			if self.visible:
				c = CardSprite(cardstr,curxpos,self.ypos)
			else:
				c = HiddenCardSprite(curxpos,self.ypos)
			self.spritelist.append(c)
			self.add(c)
			if self.alignment == Align.LEFT:
				curxpos += OVERLAP
			else:
				curxpos -= OVERLAP
