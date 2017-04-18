from constants import *

import pygame as pg


class HiddenCardSprite(pg.sprite.Sprite):
	"""
	A card of which you can only see the back.
	"""
	def __init__(self, pos):
		super(HiddenCardSprite,self).__init__()
		self.image = pg.image.load("./img/Cards/back.png").convert()
		self.image = pg.transform.scale(self.image, CARDSIZE)
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]


class CardSprite(pg.sprite.Sprite):
	"""
	A card of which you can see the rank and suit.
	It can be either highlighted or unhighlighted (=visible). If the card is visible, the highlighted attribute is false.
	"""
	def __init__(self, cardstr, pos, highlighted=False):
		super(CardSprite,self).__init__()
		self.cardstr = cardstr
		self.highlighted = highlighted

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
		self.rect.x = pos[0]
		self.rect.y = pos[1]

	def _get_image_path(self, highlighted=False):
		"""
		Gets the path to the image or highlighted image.
		"""
		filepath = ""
		if not highlighted:
			filepath += "./img/cards/"
		else:
			filepath += "./img/highlighted/"
		filepath += self.cardstr
		filepath += ".png"
		return filepath

	def sethighlighted(self,highlighted):
		"""
		Changes the "highlightedness" of the card sprite and sets the image accordingly.
		"""
		self.image = self.images[highlighted]
		self.highlighted = highlighted
