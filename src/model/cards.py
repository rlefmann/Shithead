
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
