# A colored box showing text.

import pygame as pg

class Textbox(pg.sprite.Sprite):
	def __init__(self, xpos, ypos, width, height, fontsize, color):
		pg.sprite.Sprite.__init__(self)
		self.font = pg.font.SysFont("Arial", fontsize)
		self.surf = pg.Surface((width,height))
		self.surf.blit(self.font.render("bla",1,color),[0,0])
		
		self.rect = self.surf.get_rect()
		self.rect.x = xpos
		self.rect.y = ypos
