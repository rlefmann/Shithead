from cards import *
from ..requests import *

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
		self._settings = settings
		
		# create and shuffle deck:
		self._deck = Deck()
		self._deck.shuffle()
		
		# create other card collections:
		self._discardpile = DiscardPile()
		self._graveyard = Graveyard()
		
		# create players:
		hero = Player(settings["NCARDS_UPDOWN"], True)
		villain = Player(settings["NCARDS_UPDOWN"], False)
		self._players = (hero,villain)
		
		self._initialdeal()
		
		# the minimal value that can be played
		# (in the beginning every card can be played):
		self._minval = 0
		# the player whos turn it is right now:
		self._curplayer = self._findfirstplayer()
		self._curplayer = 0 # TODO: remove

		
	def _initialdeal(self):
		"""
		Distributes the initial number of cards specified in the settings
		to the players hands, upcards and downcards.
		"""
		for i in range(2):
			# draw hand cards:
			handcards = self._deck.draw(self._settings["NCARDS_HAND"])
			self._players[i].hand.add(handcards)
			# draw downcards:
			downcards = self._deck.draw(self._settings["NCARDS_UPDOWN"])
			self._players[i].downcards.add(downcards)
			# draw upcards:
			upcards = self._deck.draw(self._settings["NCARDS_UPDOWN"])
			self._players[i].upcards.add(upcards)

	def _findfirstplayer(self):
		# TODO: implement
		return 0

	def is_possible_action(self, request):
		"""
		Checks whether a request a player has chosen is possible or not.
		"""
		if not isinstance(request, Request):
			raise Exception("something other than a request was sent to is_possible_action")
		elif isinstance(request, RequestTake):
			# the discard pile must contain cards
			return len(self._discardpile) > 0
		elif isinstance(request, RequestPlay):
			# get the cardcollection specified by the src of the request:
			src_coll = self._get_collection_from_request(request)
			# check if cardcollection contains cards:
			if len(src_coll) == 0:
				return False
			# get rank of first chosen card:
			rank = src_coll[request.indices[0]].rank
			# iterate over indices:
			for idx in request.indices:
				# check if indices are valid and if rank of all cards is the same
				if idx<0 or idx>= len(src_coll):
					return False
				elif src_coll[idx].rank != rank:
					print "cards at indices have different ranks"
					return False
			# check if cards are playable
			return rank >= self._minval or rank == self._settings["INVISIBLE"] or rank == self._settings["BURN"]
		else:
			raise TypeError("the game class can only handle take and play requests")
			
	def _get_collection_from_request(self, request):
		"""
		Get the cardcollection specified by the src of the request
		"""
		if request.src == SourceCollection.HAND:
			return self._players[self._curplayer].hand
		elif request.src == SourceCollection.UPCARDS:
			return self._players[self._curplayer].upcards
		else:
			return self._players[self._curplayer].downcards

	def play(self, playreq):
		"""
		Places the cards specified in the playreq on the discard pile.
		Note that the validity of the move is NOT checked. You have to
		use is_possible_action first.
		"""
		print "play! "+str(playreq.indices) # TODO: implement
		# get the cardcollection specified by the src of the request:
		src_coll = self._get_collection_from_request(playreq)
		# put cards from src_coll to discardpile:
		cards = src_coll.remove(playreq.indices)
		self._discardpile.add(cards)
		# adjust minval:
		self._minval = cards[0].rank # TODO: adjust, when a special card is played
		print "new minval: "+str(self._minval) # TODO; remove
		# redraw if src_coll was the players hand and there are cards
		# left in the deck:
		if src_coll == self._players[self._curplayer].hand:
			numcards_missing = self._settings["NCARDS_HAND"] - len(src_coll)
			if numcards_missing > 0:
				cards = self._deck.draw(numcards_missing)
				src_coll.add(cards)
				print "player has redrawn "+str(len(cards))+" cards"
			# sort hand:
			src_coll.sort()
		

	@property
	def phand(self):
		"""Returns the players hand as a list of cardstrings."""
		return self._players[0].hand.cardstrings()

	@property
	def pupcards(self):
		"""Returns the players upcards as a list of cardstrings."""
		return self._players[0].upcards.cardstrings()

	@property
	def pdowncards(self):
		"""Returns the players downcards as a list of cardstrings."""
		return self._players[0].downcards.cardstrings()

	@property
	def vhand(self):
		"""Returns the villains hand as a list of cardstrings."""
		return self._players[1].hand.cardstrings()

	@property
	def vupcards(self):
		"""Returns the villains upcards as a list of cardstrings."""
		return self._players[1].upcards.cardstrings()

	@property
	def vdowncards(self):
		"""Returns the villains downcards as a list of cardstrings."""
		return self._players[1].downcards.cardstrings()

	@property
	def deck(self):
		"""Returns the deck as a list of cardstrings"""
		return self._deck.cardstrings()

	@property
	def discardpile(self):
		"""Returns the discardpile as a list of cardstrings"""
		return self._discardpile.cardstrings()
