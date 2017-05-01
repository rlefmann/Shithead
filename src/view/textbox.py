# A colored box showing text.

import pygame as pg

class Textbox(object):
	def __init__(self, xpos, ypos, width, height, fontsize, fgcolor, bgcolor):
		self._rect = pg.Rect(xpos,ypos,width,height)
		self._font = pg.font.SysFont("Arial", fontsize)
		self._fgcolor = fgcolor
		self._bgcolor = bgcolor
		self.text = ""

	@property
	def text(self):
		return self._text

	@text.setter
	def text(self, textstr):
		self._text = textstr
		if self.text:
			self._textrender = self._font.render(self._text,True,pg.Color("white"))
		else:
			self._textrender = None

	def update(self,surface):
		surface.fill(self._bgcolor, self._rect)
		if self.text:
			text_rect = self._textrender.get_rect(center=self._rect.center)
			surface.blit(self._textrender, text_rect)
