from shithead.view.constants import *
from shithead.util.resources import get_resource_path

import pygame as pg
from os.path import join

class CardSprite(pg.sprite.Sprite):
	"""
	A card of which you can see the rank and suit.
	It can be either highlighted or unhighlighted (=visible). If the card is visible, the highlighted attribute is false.
	"""
	def __init__(self, cardstr, xpos, ypos, hidden=False):
		"""
		Attributes:
			cardstr: a string representation of the card, eg "qh" for the queen of hearts
		"""
		super(CardSprite,self).__init__()
		self.cardstr = cardstr
		self._hidden = hidden
		self.highlighted = False

		# The images dictionary assigns to each value of highlighted (true or false) an image
		self.images = {}

		# The image for the unhighlighted (=visible) card:
		unhighlighted_imagepath = self._get_image_path()
		unhighlighted_image = pg.image.load(unhighlighted_imagepath).convert()
		self.images[False] = pg.transform.scale(unhighlighted_image, CARDSIZE)

		# The image for the highlighted card
		highlighted_imagepath = self._get_image_path(True)
		highlighted_image = pg.image.load(highlighted_imagepath).convert()
		self.images[True] = pg.transform.scale(highlighted_image, CARDSIZE)

		# set the appropriate image for the current highlighted status of the sprite:
		self.image = self.images[self.highlighted]

		self.rect = self.image.get_rect()
		self.rect.x = xpos
		self.rect.y = ypos

	@property
	def xpos(self):
		return self.rect.x

	@property
	def ypos(self):
		return self.rect.y

	def _get_image_path(self, highlighted=False):
		"""
		Gets the path to the image or highlighted image.
		"""
		filepath = ""
		if not highlighted:
			filepath = join("img","cards")
		else:
			filepath = join("img","cards-highlighted")
		if not self._hidden:
			filepath = join(filepath, self.cardstr+".png")
		else:
			filepath = join(filepath, "back.png")
		return get_resource_path(filepath)

	def sethighlighted(self,highlighted):
		"""
		Changes the "highlightedness" of the card sprite and sets the image accordingly.
		"""
		self.image = self.images[highlighted]
		self.highlighted = highlighted


class HiddenCardSprite(CardSprite):
	"""
	A card of which you can only see the back.
	"""
	def __init__(self, xpos, ypos):
		super(HiddenCardSprite,self).__init__("??", xpos, ypos, hidden=True)
