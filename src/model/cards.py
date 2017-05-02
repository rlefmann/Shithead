import itertools
from random import shuffle

# Maps from integers representing ranks to a more read friendly
# string representation.
ranks = {0:"2",1:"3",2:"4",3:"5",4:"6",5:"7",6:"8",7:"9",8:"t",9:"j",10:"q",11:"k",12:"a"}
# The same for the suits (diamonds, hearts, spades, clubs).
suits = {0:"d",1:"h",2:"s",3:"c"}

class Card:
	"""
	A playing card, defined by its rank and suit.
	"""
	def __init__(self, rank, suit):
		"""
		Creates a new playing card.
		"""
		self.rank = rank
		self.suit = suit
	
	def __repr__(self):
		"""
		Uses the dictionaries above to create a read friendly string
		representation of the card for printing to the screen.
		"""
		return ranks[self.rank] + suits[self.suit]

	@property
	def value(self):
		"""
		Creates a unique integer value for each pair of rank and suit
		to compare the cards. This is for example necessary when finding
		the player who begins the game.
		"""
		return self.rank*4 + self.suit
    
# TODO: we most certainly need to implement the cardstrings method for some specific collections. We can then use the result for __repr__

class CardCollection(object):
    """
    A collection of zero or more cards. This is the base class for specific
    collections like hands, stacks, or the deck of the game.
    
    # TODO: change
    Inheritance hierarchy:
    -CardCollection
        -Hand
        -Stack
            -Deck
            -DiscardPile
            -Graveyard
        -UpDownCards
    
    Attributes:
        cards (list of Card): This is where the cards are stored
        visible (boolean): Determines wether the cards are visible to the
            player or not. Influences for example what happens, if you
            print the cards
    """
    def __init__(self, visible = True):
        self._cards = []
        self._visible = visible

    def __getitem__(self,idx):
		"""
		For accessing the elements of the CardCollection via square brackets.
		"""
		return self._cards[idx]
        
    def add(self, cards):
        """
        Adds more cards to the collection.
        
        Args:
            cards (list of Card): the new cards, that should be added.
        """
        self._cards.extend(cards)
        
    def remove(self, indices):
        """
        Removes the cards at the specified indices of the collection.

        Args:
            indices (list of Int): the indices of cards to be removed.

        Returns:
            A list of the removed cards.
        """
        # check if indices is of correct type and contains at least one index.
        if not isinstance(indices,(list,range)):
            raise ValueError("remove: indices must be a list or range")
        elif len(indices) == 0:
            raise ValueError("remove: you must provide at least one index")
        # collect removed cards:
        removed_cards = []
        # last index first to avoid messing the indices up by removing elements
        for idx in sorted(indices, reverse=True): 
            c = self._cards[idx]
            if c == None:
                raise ValueError("remove: index %d contains no card" % idx)
            removed_cards.append(c)
            self.delete(idx)
        return removed_cards
    
    def delete(self, idx):
        """
        Deletes the card at the specified index.
        
        Args:
            idx (Int): the index of the card that should be deleted.
        """
        del self._cards[idx]
        
    def __len__(self):
        """
        The number of cards in the CardCollection is simply the length
        of self.cards.
        """
        return len(self._cards)
        
    def cardstrings(self):
	"""
	Returns a list of string representations of the cards in the
	collection. If the collection is hidden, "??"s are put in the
	list instead of the actual card rank and value.
	"""
	if self._visible:
	    return [str(c) for c in self._cards]
	else:
	    return ["??" for c in self._cards]
    
    def __repr__(self):
	return str(self.cardstrings())
    
class Hand(CardCollection):
    """
    The hand of a player. This extends the CardCollection by being
    sortable (to more easily select cards) and having a nice string
    representation, which depends on whether the hand's visible
    attribute is set or not.
    """

    def sort(self):
        """
        Sorts the cards in the hand in increasing order by their
        value.
        """
        self._cards.sort(key = lambda c: c.value)

    def add(self, newcards):
        """
        Extends the regular add method by sorting the hand afterwards.
        """
        super(Hand, self).add(newcards)
        self.sort()


class Pile(CardCollection):
    """
    A generic pile of cards. This is the basis for discard piles and drawpiles.

    If a pile is hidden, no card is visible. If it is visible, you can see
    only its last card.
    """
    def __repr__(self):
        """
        Only the top card of a stack is shown. The filler variable
        contains what is displayed and depends on whether the
        stack is empty, hidden or visible. Also the number of cards
        in the stack is displayed.
        """
        if len(self._cards) == 0:
            filler = "  "
        elif not self._visible:
            filler = "??"
        else:
            # string representation of the last card.
            filler = str(self._cards[-1])
        # display the filler and how many cards the stack contains
        return "[%s], %d cards" % (filler, len(self._cards))

	def cardstrings(self):
	    # first set all to ??:
	    res = ["??" for c in self._cards]
	    # then change the last one to the card value, because it
	    # is the only card that is visible (in case of the deck
	    # which inherits from Stack, the top card cannot be seen
	    # and therefore it has its own cardstrings method):
	    if len(self._cards)>0:
		    res[-1] = str(self._cards[-1])


class DrawPile(Pile):
    """
    A draw pile is a pile of cards that is placed face down.
    
    The initial deck of cards. This CardCollection is different from the
    others because when creating it, all the cards for the game are
    set up, too.
    """
    def __init__(self):
        super(DrawPile, self).__init__(False) # The deck is hidden

    def shuffle(self):
        """
        Shuffle the cards of the deck.
        """
        shuffle(self._cards)
        
    def draw(self, numcards=1):
	"""
	Draws numcards many cards from the end of the deck.
	The process stops if there are no cards left in the deck,
	but no error is thrown.
	"""
	drawn = []
	for _ in range(numcards):
	    # you can only draw another card if there are still cards
	    # left in the deck:
	    if len(self) == 0:
		break
	    c = self._cards.pop()
	    drawn.append(c)
	return drawn
    
    @classmethod
    def create_deck(cls):
	"""
	The deck is a special draw pile that contains all of the cards in the beginning of the game. This class method creates the deck with all of its cards.
	"""
	drawpile = cls()
	# create cards:
        tuples = itertools.product(range(6),range(4)) # TODO: change back to 13
        for t in tuples:
            c = Card(t[0],t[1])
            drawpile._cards.append(c)
	return drawpile


class DiscardPile(Pile):
    """
    A discard pile is a pile of cards that is placed face up, such that you can see the top card (but not the cards underneath it).
    """
    def removeall(self):
        """
        Take the whole pile. This method is used when a player has to take it
        and when the DiscardPile is burnt.
        """
        allindices = range(len(self._cards)) 
        return self.remove(allindices)


# TODO: is this really necessary?
class Graveyard(Pile):
    """
    This is where burned cards from the discard pile go. Eventually we do not
    need to have a data structure for this and could just let the cards disappear,
    but an AI might want to use the information of the cards in here.
    """
    pass
    # TODO: probably should not inherit from stack, but from CardCollection
    
    
class CardRow(CardCollection):
	"""
	A CardRow object is a set of a fixed number of places, each of which can be None or hold a Card. Either all of the cards are visible (this is the case for the upcards in Shithead) or all of the cards are hidden (this is the case for the downcards).
	"""
	def __init__(self, numcards, visible=True):
		"""
		Creates numcards slots, which are filled with None entries.
		"""
		super(self.__class__, self).__init__(visible)
		if numcards<=0:
			raise ValueError("the number of cards must be positive")
		# add none entries:
		super(self.__class__, self).add([None]*numcards)
		self.numcards = numcards

	def add(self, newcards):
		"""
		We only have to add cards once and the number of cards added must
		be equal to numcards
		"""
		if len(newcards) == self.numcards:
			self._cards = newcards
		else:
			raise Exception("the number of cards must be equal to %d" % self.numcards)

	def delete(self, idx):
		"""
		Instead of deleting the entry with del, it is replaced by a None entry.
		This allows to use the generic remove method in CardCollection.
		"""
		self._cards[idx] = None

	def __repr__(self):
		"""
		Returns a string representation of the cards in the slots.
		None entries are represented by xx, hidden cards by ??.
		"""
		return str(self.cardstrings())

	def cardstrings(self):
		res = []
		for card in self._cards:
			if card == None:
				res.append("xx")
			elif not self._visible:
				res.append("??")
			else:
				res.append(str(card))
		return res

	def isempty(self):
		"""
		CardRow is empty, if every slot is None.
		"""
		return self._cards.count(None) == len(self._cards)

if __name__ == "__main__":
	c1 = Card(10,3)
	c2 = Card(8,0)
	c3 = Card(11,2)

	upcards = CardRow(3)
	upcards.add([c1,c2,c3])
	upcards.remove([0,2])
	print upcards
