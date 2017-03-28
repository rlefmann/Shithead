
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
		return ranks[self.rank] + suits[self.suits]

	def getvalue(self):
		"""
		Creates a unique integer value for each pair of rank and suit
		to compare the cards. This is for example necessary when finding
		the player who begins the game.
		"""
		return self.rank*4 + self.suit
    
    
class CardCollection:
    """
    A collection of zero or more cards. This is the base class for specific
    collections like hands, stacks, or the deck of the game.
    
    Attributes:
        cards (list of Card): This is where the cards are stored
        hidden (boolean): Determines wether the cards are visible to the
            player or not. Influences for example what happens, if you
            print the cards
    """
    def __init__(self, hidden = False):
        self.cards = []
        self.hidden = hidden
        
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
        pass # TODO: implement
    
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
        pass