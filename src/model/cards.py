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

	def getvalue(self):
		"""
		Creates a unique integer value for each pair of rank and suit
		to compare the cards. This is for example necessary when finding
		the player who begins the game.
		"""
		return self.rank*4 + self.suit
    
    
class CardCollection(object):
    """
    A collection of zero or more cards. This is the base class for specific
    collections like hands, stacks, or the deck of the game.
    
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
        hidden (boolean): Determines wether the cards are visible to the
            player or not. Influences for example what happens, if you
            print the cards
    """
    def __init__(self, hidden = False):
        self.cards = []
        self.hidden = hidden

    def __getitem__(self,idx):
		"""
		For accessing the elements of the CardCollection via square brackets.
		"""
		return self.cards[idx]
        
    def add(self, cards):
        """
        Adds more cards to the collection.
        
        Args:
            cards (list of Card): the new cards, that should be added.
        """
        self.cards.extend(cards)
        
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
            c = self.cards[idx]
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
        del self.cards[idx]
        
    def __len__(self):
        """
        The number of cards in the CardCollection is simply the length
        of self.cards.
        """
        return len(self.cards)
        
    
    
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
        self.cards.sort(key = lambda c: c.getvalue())

    def add(self, newcards):
        """
        Extends the regular add method by sorting the hand afterwards.
        """
        super(Hand, self).add(newcards)
        self.sort()

    def __repr__(self):
        """
        Returns a string representation of the cards in the hand.
        If the cards are hidden a string representation of a list of 
        ?? entries of appropriate length is returned. 
        """
        if self.hidden:
            return str(["??"]*len(self))
        else:
            return str(self.cards)


class Stack(CardCollection):
    """
    A generic stack of cards. This is the basis for the deck, the
    discard pile and the graveyard.

    If a stack is hidden, no card is visible. If not, you can see
    only the last card of the deck.
    """
    def __repr__(self):
        """
        Only the top card of a stack is shown. The filler variable
        contains what is displayed and depends on whether the
        stack is empty, hidden or visible. Also the number of cards
        in the stack is displayed.
        """
        if len(self.cards) == 0:
            filler = "  "
        elif self.hidden:
            filler = "??"
        else:
            # string representation of the last card.
            filler = str(self.cards[-1])
        # display the filler and how many cards the stack contains
        return "[%s], %d cards" % (filler, len(self.cards))


class Deck(Stack):
    """
    The initial deck of cards. This CardCollection is different from the
    others because when creating it, all the cards for the game are
    set up, too.
    """
    def __init__(self):
        super(Deck, self).__init__(True) # The deck is hidden
        # create cards:
        tuples = itertools.product(range(13),range(4))
        for t in tuples:
            c = Card(t[0],t[1])
            self.cards.append(c)

    def shuffle(self):
        """
        Shuffle the cards of the deck.
        """
        shuffle(self.cards)
        
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
			c = self.cards.pop()
			drawn.append(c)
		return drawn
			


class DiscardPile(Stack):
    """
    You can either play cards of the same rank or you have to take the whole
    pile.
    """
    def removeall(self):
        """
        Take the whole pile. This method is used when a player has to take it
        and when the DiscardPile is burnt.
        """
        allindices = range(len(self.cards)) 
        return self.remove(allindices)
    
class Graveyard(Stack):
    """
    This is where burned cards from the discard pile go. Eventually we do not
    need to have a data structure for this and could just let the cards disappear,
    but an AI might want to use the information of the cards in here.
    """
    pass
    # TODO: probably should not inherit from stack, but from CardCollection
    
    
class UpDownCards(CardCollection):
    """
    This CardCollection is different from the others, because each card has a
    fixed position, that is not changed if a card is added or removed.
    """
    def __init__(self, numcards, hidden=False):
        """
        Creates numcards slots, which are filled with None entries.
        """
        super(self.__class__, self).__init__(hidden)
        if numcards<=0:
            raise ValueError("the number of cards must be positive")
        # add none entries (probably not necessary):
        super(self.__class__, self).add([None]*numcards)
        self.numcards = numcards
        
    def add(self, newcards):
        """
        We only have to add cards once and the number of cards added must
        be equal to numcards
        """
        if len(newcards) == self.numcards:
            self.cards = newcards
        else:
            raise Error("the number of cards must be equal to %d" % self.numcards)
            
    def delete(self, idx):
        """
        Instead of deleting the entry with del, it is replaced by a None entry.
        This allows to use the generic remove method in CardCollection.
        """
        self.cards[idx] = None
        
    def __repr__(self):
        """
        Returns a string representation of the cards in the slots.
        None entries are represented by xx, hidden cards by ??.
        """
        res = "["
        for card in self.cards:
            if card == None:
                res += "xx, "
            elif self.hidden:
                res += "??, "
            else:
                res += str(card)
                res += ", "
        res = res[:-2] + "]" # remove the last comma and whitespace
        return res

        
if __name__ == "__main__":
    c1 = Card(10,3)
    c2 = Card(8,0)
    c3 = Card(11,2)
    
    upcards = UpDownCards(3)
    upcards.add([c1,c2,c3])
    upcards.remove([0,2])
    print upcards
