# SIZES:
SCREENWIDTH = 800
SCREENHEIGHT = 650
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)
CARDWIDTH = 80
CARDHEIGHT = 100
CARDSIZE = (CARDWIDTH, CARDHEIGHT)
OVERLAP = int(CARDWIDTH/4) # one can see at least 1/4 of each card
MARGIN = 5
CURSORWIDTH = 20
CURSORHEIGHT = 20
CURSORSIZE = (CURSORWIDTH, CURSORHEIGHT)


# Positions of the various objects on the screen:
VHAND_X = SCREENWIDTH-CARDWIDTH-MARGIN
VHAND_Y = MARGIN
VDOWN_X = SCREENWIDTH-MARGIN
VDOWN_Y = 2*MARGIN + CARDHEIGHT
VUP_X = SCREENWIDTH-MARGIN
VUP_Y = 2*MARGIN + CARDHEIGHT + OVERLAP

DECK_X = int(SCREENWIDTH/2) - CARDWIDTH - MARGIN
DECK_Y = VUP_Y + MARGIN + int(CARDHEIGHT*3/4)
DPILE_X = int(SCREENWIDTH/2) + CARDWIDTH - MARGIN
DPILE_Y = DECK_Y

PUP_X = MARGIN
PUP_Y = DECK_Y + int(CARDHEIGHT*3/4) + MARGIN
PDOWN_X = MARGIN
PDOWN_Y = PUP_Y+OVERLAP
PHAND_X = MARGIN
PHAND_Y = PDOWN_Y+CURSORHEIGHT+CARDHEIGHT+MARGIN

# TODO: experimental, adapts the height of the window:
SCREENHEIGHT = PHAND_Y + CARDHEIGHT + MARGIN 

# COLORS:
GREEN = (0,100,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

# OTHER:
TITLE = "Shithead"
FRAMERATE = 30
