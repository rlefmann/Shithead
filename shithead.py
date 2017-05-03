import os
import pygame as pg

from src.controller import Controller

if __name__ == "__main__":
	# open the window in the center of the screen:
	os.environ["SDL_VIDEO_CENTERED"] = '1'
	pg.init()
	Controller()
