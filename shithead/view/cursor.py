import pygame as pg

from shithead.view.constants import *
from shithead.view.cardspritegroups import CardSpriteGroup, CardStack, LaidOutCards, SpreadCards
from shithead.view.viewmode import ViewMode

class Cursor(pg.sprite.Sprite):
	"""
	A cursor for selecting cards from a CardSpriteGroup.
	The CardSpriteGroup
	"""
	def __init__(self, handgroup, upgroup, downgroup, dpilegroup):
		super(Cursor, self).__init__()
		self._spritegroups = [handgroup, upgroup, downgroup, dpilegroup]
		# index of the current group:
		self._groupidx = 0
		# index of the card the cursor is pointing to:
		self._cardidx = 0
		# The indices of the cards that are currently selected:
		self._selected_indices = []
		# the indices of inactive groups, which means you cannot access them with the cursor:
		self._inactive_groups = []
		
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
		self.mode = ViewMode.HERO_PLAYS_HAND

	@property
	def mode(self):
		return self._mode

	@mode.setter
	def mode(self, vmode):
		self._mode = vmode
		if vmode == ViewMode.HERO_PLAYS_HAND:
			self._set_active([0,3])
		elif vmode == ViewMode.HERO_PLAYS_UPCARDS:
			self._set_active([1,3])
		elif vmode == ViewMode.HERO_PLAYS_DOWNCARDS:
			self._set_active([2]) # you must try to play a downcard
		elif vmode == ViewMode.HERO_TAKES_UPCARDS:
			self._set_active([1])
		elif vmode == ViewMode.FINISHED or vmode == ViewMode.VILLAIN_MOVE:
			self._set_active([])
			return # do not update the cursor when finished
		groupidx, cardidx = self._first_allowed_pos()
		if groupidx != -1 and cardidx != -1:
			self._move(groupidx, cardidx)

	@property
	def deactivated(self):
		return self._mode == ViewMode.FINISHED or self._mode == ViewMode.VILLAIN_MOVE

	@property
	def curgroup(self):
		return self._spritegroups[self._groupidx]
		
	@property
	def cursprite(self):
		return self.curgroup[self._cardidx]
		
	@property
	def selected_indices(self):
		return self._selected_indices

	def moveleft(self):
		"""
		Moves the cursor one position to the left.
		"""
		if not self.deactivated and self._cardidx > 0:
			if isinstance(self.curgroup, SpreadCards):
				self._move(self._groupidx, self._cardidx-1)
			elif isinstance(self.curgroup, LaidOutCards):
				# move the cursor one position to the left, but skip empty slots:
				#emptyslots = self.curgroup.empty_slots
				i = self._cardidx - 1
				#while i in emptyslots:
				while self.curgroup[i] == None:
					i-=1
				if i>=0:
					self._move(self._groupidx, i)

	def moveright(self):
		"""
		Moves the cursor one position to the right.
		"""
		if not self.deactivated and self._cardidx < len(self.curgroup)-1:
			if isinstance(self.curgroup, SpreadCards):
				self._move(self._groupidx, self._cardidx+1)
			elif isinstance(self.curgroup, LaidOutCards):
				# move the cursor one position to the left, but skip empty slots:
				emptyslots = self.curgroup.empty_slots
				i = self._cardidx + 1
				while i in emptyslots:
					i+=1
				if i < len(self.curgroup):
					self._move(self._groupidx, i)
	
	def next_group(self):
		if not self.deactivated and len(self._selected_indices) == 0: # cursor is blocked to the current group if at least one sprite is highlighted. If the cursor is blocked it cannot switch between groups anymore
			self._groupidx = (self._groupidx+1)%len(self._spritegroups)
			if len(self.curgroup) == 0 or self._groupidx in self._inactive_groups:
				self.next_group()
			else:
				self._move(self._groupidx,self.curgroup.first_nonempty_slot()) # this must be the first non-empty

	def toggle_highlighted(self):
		"""
		Highlights the currently selected CardSprite.
		"""
		#sprite = self.cursprite
		if not self.deactivated:
			if not self.cursprite.highlighted:
				self._selected_indices.append(self._cardidx)
			else:
				self._selected_indices.remove(self._cardidx)
			self.cursprite.sethighlighted(not self.cursprite.highlighted)

	def _move(self, groupidx, cardidx):
		if not self._is_valid_idx(groupidx, self._spritegroups):
			raise ValueError("called the _move method with an invalid groupidx")
		group = self._spritegroups[groupidx]
		if not self._is_valid_idx(cardidx, group):
			raise ValueError("called the _move method with an invalid cardidx {}".format(cardidx))
		self.rect.x = group[cardidx].xpos
		self.rect.y = group[cardidx].ypos
		self._groupidx = groupidx
		self._cardidx = cardidx
		# change the width of the frame depending on whether we have
		# selected an overlapped card or not:
		if isinstance(self.curgroup, SpreadCards) and len(self.curgroup)>1 and cardidx < len(group)-1:
			self.image = self._images[True]
		else:
			self.image = self._images[False]
			
			
	def _first_allowed_pos(self):
		if self.deactivated:
			return -1,-1
		groupidx, cardidx = 0,0
		# find groupidx:
		while groupidx in self._inactive_groups:
			groupidx += 1
			if groupidx >= len(self._spritegroups): # there is no active group
				raise Exception("cannot place the cursor, because all groups are inactive")
		# "groupidx: {}".format(groupidx)
		# find cardidx:
		group = self._spritegroups[groupidx]
		if len(group) == 0:
			raise Exception("cannot place the cursor, because the group is empty")
		elif isinstance(group, LaidOutCards):
			while cardidx in group.empty_slots:
				cardidx += 1
				if cardidx >= len(group):
					raise Exception("cannot place the cursor, because all slots in the group are empty") # TODO: deal with empty groups
		return groupidx, cardidx

	def _is_valid_idx(self,idx,lst):
		return 0<=idx<len(lst)

	def unhighlight_all(self):
		"""
		Unhighights all highlighted cards.
		"""
		for idx in self._selected_indices:
			sprite = self.curgroup[idx]
			sprite.sethighlighted(False)
		self._selected_indices = []

	def _is_active(self, groupidx):
		return groupidx not in self._inactive_groups

	def reset(self):
		"""
		Resets the cursor to the initial position.
		If the spritegroup is of type LaidOutCards it picks the first
		non-empty slot.
		TODO: what happens if all the slots are empty?
		TODO: does this make sense or should we also jump back to group 0?
		"""
		groupidx, cardidx = self._first_allowed_pos()
		self._move(groupidx, cardidx)

	def _set_active(self, indices):
		self._inactive_groups = []
		for groupidx in range(len(self._spritegroups)):
			if groupidx not in indices:
				self._inactive_groups.append(groupidx)
