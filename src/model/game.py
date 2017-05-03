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
		self.hand = Hand(hero) # if villain, then the hand is hidden
		self.upcards = CardRow(num_up_down, visible = True)
		self.downcards = CardRow(num_up_down, visible = False)
		
	def is_playing_from_hand(self):
		return len(self.hand) > 0
	
	def is_playing_from_upcards(self):
		return len(self.hand) == 0 and not self.upcards.isempty()
		
	def is_playing_from_downcards(self):
		return len(self.hand) == 0 and self.upcards.isempty() and not self.downcards.isempty()


class Game:
	"""
	This class contains all of the game logic.
	"""
	
	def __init__(self, settings):
		self._settings = settings
		
		# create and shuffle deck:
		self._deck = DrawPile.create_deck()
		self._deck.shuffle()
		
		# create other card collections:
		self._discardpile = DiscardPile()
		self._graveyard = Graveyard()
		
		# create players:
		hero = Player(settings["NCARDS_UPDOWN"], True)
		villain = Player(settings["NCARDS_UPDOWN"], False)
		self._players = (hero,villain)
		
		self._deal()
		
		# the minimal value that can be played
		# (in the beginning every card can be played):
		self._minval = 0
		# the player whos turn it is right now:
		self._curplayer = self._findfirstplayer()
		self._curplayer = 0 # TODO: remove
		self._lastplayed = [] # the cardstring representation of the last cards that were played

	def is_possible_move(self, request):
		"""
		Checks whether a request a player has chosen is possible or not.
		"""
		if not isinstance(request, Request):
			raise Exception("something other than a request was sent to is_possible_move")
		elif isinstance(request, RequestTake):
			# the discard pile must contain cards
			return len(self._discardpile) > 0
		elif isinstance(request, RequestPlay):
			return self._is_possible_play(request)
		elif isinstance(request, RequestTakeUpcards):
			return self._is_possible_take_upcards(request)
		else:
			raise TypeError("the game class can only handle take and play requests")

	def play(self, playreq):
		"""
		Places the cards specified in the playreq on the discard pile.
		Note that the validity of the move is NOT checked. You have to
		use is_possible_move first.
		"""
		# get the cardcollection specified by the src of the request:
		src_coll = self._get_collection_from_request(playreq)
		# put cards from src_coll to discardpile:
		cards = src_coll.remove(playreq.indices)
		print "player plays "+str(cards)
		self._discardpile.add(cards)
		self._lastplayed = [str(c) for c in cards]
		rank = cards[0].rank
		if rank == self._settings["BURN"]:
			dead_cards = self._discardpile.removeall()
			self._graveyard.add(dead_cards)
			self._minval = 0
		# adjust minval:
		elif rank != self._settings["INVISIBLE"]: # dont adjust minval if a invisible card is played
			self._minval = rank
		print "new minval: "+str(self._minval) # TODO; remove
		# redraw if src_coll was the players hand and there are cards
		# left in the deck:
		if src_coll == self.curplayer.hand:
			self.redraw() # TODO: this should be inside the controller

	def redraw(self):
		"""
		If the player has less than the number of cards he started the
		game with left in his hand, he redraws the missing number of
		cards or whatever is left in the deck.
		"""
		numcards_missing = self._settings["NCARDS_HAND"] - len(self.curplayer.hand)
		if numcards_missing > 0:
			cards = self._deck.draw(numcards_missing)
			self.curplayer.hand.add(cards)
			print "player has redrawn "+str(len(cards))+" cards"
			self.curplayer.hand.sort()
			
	def take(self):
		"""
		Take all the cards from the discard pile into the current
		players hand.
		"""
		cards = self._discardpile.removeall()
		hand = self.curplayer.hand
		hand.add(cards)
		self._minval = 0

	def take_downcard(self, idx):
		card = self.curplayer.downcards.remove([idx])
		self.curplayer.hand.add(card)
	
	def take_upcards(self, indices):
		cards = self.curplayer.upcards.remove(indices)
		self.curplayer.hand.add(cards)

	def is_win(self): # TODO: we can add the player as an argument and only return for the current player
		"""
		Returns 0 if the current player has won the game.
		"""
		p = self.curplayer
		return len(p.hand) == 0 and p.upcards.isempty() and p.downcards.isempty()

	def _deal(self):
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
		"""
		Determines which player starts the game. Looks for the player
		who's hand contains the smallest card which is not a special card.
		If every player does only have special cards, the lowest special
		card begins.

		Returns 0, if hero starts and 1 otherwise.
		"""
		return 0

	def _is_possible_take_upcards(self, request):
		#if not self.curplayer.is_playing_from_upcards():
		#	print "player does not play from upcards"
		#	return False
		src_coll = self.curplayer.upcards
		return self._is_allowed_card_indexlist(src_coll, request.indices)

	def _is_allowed_card_indexlist(self, src_coll, indices):
		"""
		Checks whether a list of indices has length greater than 0, all
		indices are valid for the provided src_coll and the rank of the
		cards at the indices in src_coll is the same.
		"""
		if len(indices) == 0:
			print "indices must contain at least one index"
		rank = None
		for idx in indices:
			# check if indices are valid:
			if idx<0 or idx>=len(src_coll):
				print "bad index "+str(idx)
				return False
			elif rank == None: # get rank of first chosen card
				rank = src_coll[indices[0]].rank
			elif src_coll[idx].rank != rank:
				print "cards at indices have different ranks"
				return False
		return True

	def _is_possible_play(self, request):
		# get the cardcollection specified by the src of the request:
		src_coll = self._get_collection_from_request(request)
		if not self._is_allowed_source(src_coll):
			return False
		elif not self._is_allowed_card_indexlist(src_coll, request.indices):
			return False
		# check if cards are playable
		rank = src_coll[request.indices[0]].rank
		return rank >= self._minval or rank == self._settings["INVISIBLE"] or rank == self._settings["BURN"]
			
	def _is_allowed_source(self, src_coll):
		"""
		Checks if the collection from which a player wants to play card
		can be chosen currently. For example you cannot play upcards if
		you still have cards in your hand
		"""
		if src_coll == self.curplayer.hand and self.curplayer.is_playing_from_hand():
			return True
		elif src_coll == self.curplayer.upcards and self.curplayer.is_playing_from_upcards():
			return True
		elif src_coll == self.curplayer.downcards and self.curplayer.is_playing_from_downcards():
			return True
		return False

	def _get_collection_from_request(self, request):
		"""
		Get the cardcollection specified by the src of the request
		"""
		if request.src == SourceCollection.HAND:
			return self.curplayer.hand
		elif request.src == SourceCollection.UPCARDS:
			return self.curplayer.upcards
		else:
			return self.curplayer.downcards


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
		#print type(self._deck.cardstrings())
		return self._deck.cardstrings()

	@property
	def discardpile(self):
		"""Returns the discardpile as a list of cardstrings"""
		return self._discardpile.cardstrings()

	@property
	def curhand(self):
		return self._players[self._curplayer].hand.cardstrings()

	@property
	def curupcards(self):
		return self._players[self._curplayer].upcards.cardstrings()

	@property
	def curdowncards(self):
		return self._players[self._curplayer].downcards.cardstrings()

	@property
	def curplayer(self):
		return self._players[self._curplayer]

	@property
	def lastplayed(self):
		return self._lastplayed
