#!/usr/bin/env python

import os
import pygame as pg

from .controller import Controller

def main():
	# open the window in the center of the screen:
	os.environ["SDL_VIDEO_CENTERED"] = '1'
	pg.init()
	Controller()

if __name__ == "__main__":
	main()
