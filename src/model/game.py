from cards import *
from action import *

class Player:
	"""
	A player has 3 CardCollections: a hand, upcards and downcards
	"""
	def __init__(self, num_up_down, hero=False):
		"""
		Creates a new player.
		Attrs:
			num_up_down: the number of upcards and docwncards
			villain: True, if the Player is villain, False if he is hero
		"""
		self.hero = hero
		self.hand = Hand(not hero) # if villain, then the hand is hidden
		self.upcards = UpDownCards(num_up_down, hidden = False)
		self.downcards = UpDownCards(num_up_down, hidden = True)


class Game:
	"""
	This class contains all of the game logic.
	"""
	
	def __init__(self, settings):
		self.settings = settings
		
		# create and shuffle deck:
		self.deck = Deck()
		self.deck.shuffle()
		
		# create other card collections:
		self.discardpile = DiscardPile()
		self.graveyard = Graveyard()
		
		# create players:
		hero = Player(settings["NCARDS_UPDOWN"], True)
		villain = Player(settings["NCARDS_UPDOWN"], False)
		self.players = (hero,villain)
		
		self._initialdeal()
		
		# the minimal value that can be played
		# (in the beginning every card can be played):
		self.minval = 0
		# the player whos turn it is right now:
		self.curplayer = self._findfirstplayer()
		self.curplayer = 0 # TODO: remove
		
	def _initialdeal(self):
		"""
		Distributes the initial number of cards specified in the settings
		to the players hands, upcards and downcards.
		"""
		for i in range(2):
			# draw hand cards:
			handcards = self.deck.draw(self.settings["NCARDS_HAND"])
			self.players[i].hand.add(handcards)
			# draw downcards:
			downcards = self.deck.draw(self.settings["NCARDS_UPDOWN"])
			self.players[i].downcards.add(downcards)
			# draw upcards:
			upcards = self.deck.draw(self.settings["NCARDS_UPDOWN"])
			self.players[i].upcards.add(upcards)

	def _findfirstplayer(self):
		# TODO: implement
		return 0

	def is_possible_action(self, action):
		"""
		Checks whether an action a player has chosen is valid or not.
		"""
		if not isinstance(action, Action):
			raise Exception("something other than an action was senf to possibleaction")
		elif isinstance(action, TakeAction):
			print "take action"
		elif isinstance(action, PlayAction):
			print "play action"
		return True # TODO: implement. This is just a skeleton
