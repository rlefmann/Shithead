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


class CardSpriteGroup(pg.sprite.OrderedUpdates):
	"""
	A basic group of card sprites. Inherits from OrderedUpdates so that the overlapping of cards is displayed correctly.
	"""
	def __init__(self,xpos,ypos,alignment=Align.LEFT,visible=True):
		super(CardSpriteGroup, self).__init__()
		self.xpos = xpos
		self.ypos = ypos
		# this is a separate list of sprites we need to keep:
		self.spritelist = []
		self.visible = visible
		if not self.alignment_allowed(alignment):
			raise Exception("alignment not allowed for this CardSpriteGroup")
		self.alignment = alignment

	def __getitem__(self,idx):
		"""
		For accessing the sprites of the CardSpriteGroup via square brackets.
		"""
		return self.spritelist[idx]

	def __len__(self):
		return len(self.spritelist)

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


class SpreadCards(CardSpriteGroup):
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


class LaidOutCards(CardSpriteGroup):
	"""
	Cards that lay next to each other, divided by a gap specified in the
	constant MARGIN. The alignment can be either left, right or center
	and the cards can be either visible (example: upcards) or hidden
	(example: downcards).
	"""
	def __init__(self,xpos,ypos,alignment=Align.CENTER,visible=True):
		super(LaidOutCards, self).__init__(xpos,ypos,alignment,visible)
		self.empty_slots = []
		
	def alignment_allowed(self, alignment):
		"""
		The alignment can be either left, right or center.
		"""
		return alignment in [Align.LEFT, Align.CENTER, Align.RIGHT]
	
	def update(self, cards):
		print cards
		# empty the sprite list:
		self.spritelist = []
		# remove all previous sprites:
		self.empty()
		# remove the information about the empty slots:
		self.empty_slots = []
		
		# Detect the leftmost vertical position:
		
		# the vertical space the laid out cards take on the screen:
		verticalspace = len(cards)*(MARGIN+CARDWIDTH)-MARGIN
		if self.alignment == Align.LEFT:
			assert self.xpos + verticalspace < SCREENWIDTH
			curxpos = self.xpos
		elif self.alignment == Align.RIGHT:
			assert self.xpos - verticalspace > 0
			curxpos = self.xpos - verticalspace
		else: # Align.CENTER
			# TODO: Assert
			n=len(cards)
			if n%2 == 0: # even number of cards
				curxpos = self.xpos - int(MARGIN/2) - n/2*CARDWIDTH - (n/2-1)*MARGIN
			else: # odd number of cards
				curxpos = self.xpos - int(CARDSIZE[0]/2) - int(n/2)*(CARDSIZE[0]+MARGIN)
		for idx, cardstr in enumerate(cards):
			# a gap because of an empty slot:
			if cardstr == "xx":
				self.empty_slots.append(idx)
			elif self.visible:
				if cardstr == "??":
					raise ValueError("the cardstring ?? is not allowed to be handed to visible LaidOutCards")
				c = CardSprite(cardstr, curxpos, self.ypos)
				self.spritelist.append(c)
				self.add(c)
			else:
				c = HiddenCardSprite(curxpos, self.ypos)
				self.spritelist.append(c)
				self.add(c)
			curxpos += (CARDWIDTH+MARGIN)
		

class CardStack(CardSpriteGroup):
	"""
	Only the top card of a stack can be seen.
	"""
	def __init__(self,xpos,ypos,visible=True):
		super(CardStack, self).__init__(xpos,ypos,Align.STACK,visible)
		
	def alignment_allowed(self, alignment):
		return alignment == Align.STACK
		
	def update(self, cards):
		self.spritelist = []
		self.empty()
		if len(cards) > 0:
			if self.visible:
				c = CardSprite(cards[-1], self.xpos, self.ypos)
			else:
				c = HiddenCardSprite(self.xpos, self.ypos)
			self.spritelist.append(c)
			self.add(c)
				
# TODO: what happens if there are no cards to display?
