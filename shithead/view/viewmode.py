from enum import Enum

class ViewMode(Enum):
	HERO_PLAYS_HAND = 1,
	HERO_PLAYS_UPCARDS = 2,
	HERO_PLAYS_DOWNCARDS = 3,
	HERO_TAKES_UPCARDS = 4,
	VILLAIN_MOVE = 5,
	FINISHED = 6
