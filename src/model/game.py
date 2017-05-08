from cards import *
from ..gamemode import *

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
		# the cardstring representation of the last cards that were played:
		self._lastplayed = []
		# the current game mode:
		self._mode = GameMode.HAND
		# the lower card was played and the game direction is reversed:
		self._lower = False
		
	def can_play_handcards(self, indices):
		if not self._mode == GameMode.HAND:
			return False
		playsrc = self.curplayer.hand
		return self._can_play(playsrc, indices)

	def can_play_upcards(self, indices):
		if not self._mode == GameMode.UPCARDS:
			return False
		playsrc = self.curplayer.upcards
		return self._can_play(playsrc, indices)
		
	def can_play_downcards(self, indices):
		if not self._mode == GameMode.DOWNCARDS:
			return False
		elif len(indices) != 1: # you can only play one downcard at a time
			return False
		playsrc = self.curplayer.downcards
		return self._can_play(playsrc, indices)

	def can_take(self):
		if self._mode in [GameMode.FINISHED, GameMode.TAKE_UPCARDS]:
			return False
		else:
			return len(self._discardpile) > 0

	def can_take_upcards(self, indices):
		if self._mode != GameMode.TAKE_UPCARDS:
			print "player does not play from upcards"
			return False
		takesrc = self.curplayer.upcards
		return self._is_allowed_card_indexlist(takesrc, indices)

	def play_handcards(self, indices):
		playsrc = self.curplayer.hand
		self._play(playsrc, indices)
		# redraw if playsrc was the players hand and there are cards
		# left in the deck:
		self.redraw() # TODO: this should be inside the controller
		
	def play_upcards(self, indices):
		playsrc = self.curplayer.upcards
		self._play(playsrc, indices)
		
	def play_downcards(self, indices):
		playsrc = self.curplayer.downcards
		self._play(playsrc, indices)

	def take(self):
		"""
		Take all the cards from the discard pile into the current
		players hand.
		"""
		plays_from_up = self.curplayer.is_playing_from_upcards()
		cards = self._discardpile.removeall()
		hand = self.curplayer.hand
		hand.add(cards)
		self._minval = 0
		if plays_from_up:
			self._mode = GameMode.TAKE_UPCARDS

	def take_upcards(self, indices):
		cards = self.curplayer.upcards.remove(indices)
		self.curplayer.hand.add(cards)

	def take_downcard(self, idx):
		card = self.curplayer.downcards.remove([idx])
		self.curplayer.hand.add(card)

	def is_win(self): # TODO: we can add the player as an argument and only return for the current player
		"""
		Returns 0 if the current player has won the game.
		"""
		p = self.curplayer
		if len(p.hand) == 0 and p.upcards.isempty() and p.downcards.isempty():
			self._mode = GameMode.FINISHED
			return True
		return False

	def switch_player(self):
		"""
		Switches to the next player and sets the GameMode depending on
		his cards.
		"""
		#self._curplayer = (self._curplayer+1)%2 # TODO: uncomment!
		# set the mode correctly:
		if len(self.curplayer.hand) > 0:
			self._mode = GameMode.HAND
		elif not self.curplayer.upcards.isempty():
			self._mode = GameMode.UPCARDS
		elif not self.curplayer.downcards.isempty():
			self._mode = GameMode.DOWNCARDS
		else:
			self._mode = GameMode.FINISHED # TODO: maybe we can make the win check obsolete!

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

	def _can_play(self, playsrc, indices):
		if not self._is_allowed_card_indexlist(playsrc, indices):
			return False
		# check if cards are playable
		rank = playsrc[indices[0]].rank
		return rank >= self._minval or rank == self._settings["INVISIBLE"] or rank == self._settings["BURN"]

	def _play(self, playsrc, indices):
		"""
		Places the cards with the given indices from playsrc on the discard pile.
		Note that the validity of the move is NOT checked. You have to
		use the appropriate can_play_* method first.
		"""
		# put cards from playsrc to discardpile:
		cards = playsrc.remove(indices)
		print "player plays "+str(cards)
		self._discardpile.add(cards)
		self._lastplayed = [str(c) for c in cards]
		rank = cards[0].rank
		if self._is_burn(rank):
			dead_cards = self._discardpile.removeall()
			self._graveyard.add(dead_cards)
			self._minval = 0
		# adjust minval:
		elif rank != self._settings["INVISIBLE"]: # dont adjust minval if a invisible card is played
			self._minval = rank
		print "new minval: "+str(self._minval) # TODO; remove

	def _is_allowed_card_indexlist(self, playsrc, indices):
		"""
		Checks whether a list of indices has length greater than 0, all
		indices are valid for the provided playsrc and the rank of the
		cards at the indices in playsrc is the same.
		"""
		if len(indices) == 0:
			print "indices must contain at least one index"
		rank = None
		for idx in indices:
			# check if indices are valid:
			if idx<0 or idx>=len(playsrc):
				print "bad index "+str(idx)
				return False
			elif rank == None: # get rank of first chosen card
				rank = playsrc[indices[0]].rank
			elif playsrc[idx].rank != rank:
				print "cards at indices have different ranks"
				return False
		return True

	def _is_burn(self, rank): # TODO: maybe we can just look at the top cards of the pile and dont need the rank
		"""
		Checks whether the cards in the discard pile get burned. This
		happens if either the burn card is played or four cards of
		equal rank lie on top of the discard pile.
		"""
		if rank == self._settings["BURN"]:
			return True
		if len(self._discardpile) > 3:
			# look at the last 4 cards of the discardpile and check if they all have the same rank
			return all(c.rank == rank for c in self._discardpile[-4:])
		return False

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

	@property
	def mode(self):
		return self._mode
