import pygame as pg

from constants import *
from cardspritegroups import CardSpriteGroup, CardStack, LaidOutCards, SpreadCards

class Cursor(pg.sprite.Sprite):
	"""
	A cursor for selecting cards from a CardSpriteGroup.
	The CardSpriteGroup
	"""
	def __init__(self, spritegroup):
		super(Cursor, self).__init__()
		self._blocked = False

		self._images = {}
		# create cursor image for when the whole card is visible:
		img = pg.image.load("./img/frame.png").convert_alpha()
		img = pg.transform.scale(img, CARDSIZE)
		self._images[False] = img

		# create cursor image for when the card is overlapped:
		img = pg.image.load("./img/frameoverlap.png").convert_alpha()
		img = pg.transform.scale(img, CARDSIZE)
		self._images[True] = img

		self.image = self._images[False]
		
		self.rect = self.image.get_rect()
		self.cardspritegroup = spritegroup
		self.move(self.cardspritegroup,0) # TODO: is this okay (idx=0)?

	@property
	def cardspritegroup(self):
		return self._cardspritegroup

	@cardspritegroup.setter
	def cardspritegroup(self, newgroup):
		if not isinstance(newgroup, CardSpriteGroup):
			raise TypeError("you need to assign a cardspritegroup to the cursor")
		self._cardspritegroup = newgroup

	def move(self, spritegroup, idx):
		if not isinstance(self.cardspritegroup, CardStack): # TODO: where is this for? Makes no sense to me
			self.rect.x = spritegroup[idx].xpos
			self.rect.y = spritegroup[idx].ypos
			self.cardspritegroup = spritegroup
			self._idx = idx
			# change the width of the frame depending on whether we have
			# selected an overlapped card or not:
			if isinstance(self.cardspritegroup, SpreadCards) and idx < len(self.cardspritegroup)-1:
				self.image = self._images[True]
			else:
				self.image = self._images[False]
				

	def moveleft(self):
		"""
		Moves the cursor one position to the left.
		"""
		if isinstance(self.cardspritegroup, SpreadCards) and self._idx > 0:
			self.move(self.cardspritegroup, self._idx-1)
		elif isinstance(self.cardspritegroup, LaidOutCards):
			# move the cursor one position to the left, but skip empty slots:
			emptyslots = self.cardspritegroup.empty_slots
			i = self._idx - 1
			while i in emptyslots:
				i-=1
			if i>=0:
				self.move(self.cardspritegroup, i)

	def moveright(self):
		"""
		Moves the cursor one position to the right.
		"""
		if isinstance(self.cardspritegroup, SpreadCards) and self._idx < len(self.cardspritegroup)-1:
			self.move(self.cardspritegroup, self._idx+1)
		elif isinstance(self.cardspritegroup, LaidOutCards):
			# move the cursor one position to the left, but skip empty slots:
			emptyslots = self.cardspritegroup.empty_slots
			i = self._idx + 1
			while i in emptyslots:
				i+=1
			if i < len(self.cardspritegroup):
				self.move(self.cardspritegroup, i)

	def reset(self):
		"""
		Resets the cursor to the initial position.
		If the spritegroup is of type LaidOutCards it picks the first
		non-empty slot.
		TODO: what happens if all the slots are empty?
		"""
		if isinstance(self.cardspritegroup, SpreadCards) or isinstance(self.cardspritegroup, CardStack):
			self.move(self.cardspritegroup, 0)
		elif isinstance(self.cardspritegroup, LaidOutCards):
			emptyslots = self.cardspritegroup.empty_slots
			self._idx = 0
			if self._idx in emptyslots:
				self.moveright()

	def toggle_highlighted(self):
		"""
		Highlights the currently selected CardSprite.
		"""
		sprite = self.cardspritegroup[self._idx]
		sprite.sethighlighted(not sprite.highlighted)


class CursorManager(object):
	def __init__(self, spritegroups):
		if len(spritegroups) == 0:
			raise ValueError("you need to give the CursorManager at least 1 SpriteGroup")
		self._spritegroups = spritegroups
		self._groupidx = 0
		print len(self.curgroup)
		self._cursor = Cursor(self.curgroup)
		self._inactive = [] # the indices of inactive groups
		
	@property
	def curgroup(self):
		return self._spritegroups[self._groupidx]

	@property
	def cursor(self):
		return self._cursor

	# TODO: needed?
	def toggle_inactive(self, groupidx):
		if groupidx in self._inactive:
			self._inactive.remove(groupidx)
		else:
			self._inactive.append(groupidx)
	
	def next_group(self):
		self._groupidx = (self._groupidx+1)%len(self._spritegroups)
		if len(self.curgroup) == 0 or self._groupidx in self._inactive:
			self.next_group()
		else:
			self._cursor.move(self.curgroup,0) # this must be the first non-empty
