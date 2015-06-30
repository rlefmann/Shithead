import itertools
from random import shuffle

num_values = 13
num_suits = 4

class Cards:
	def __init__(self):
		self.cards = []
		
	def __str__(self):
		return str(self.cards)
	
	def shuffle(self):
		shuffle(self.cards)
		
	def pop_last(self):
		return self.cards.pop()
	
	def pop_first(self):
		return self.cards.pop(0)
	
	def add_card(self,card):
		pass

	def add_cards(self,cards):
		pass
	
	def remove_card(self,index): 
		pass
	
	def remove_cards(self,indices):
		pass


class Pile(Cards):
	def __init__(self):
		Cards.__init__(self)
		# Create all pairs of number values:
		i = itertools.product(range(num_values),range(num_suits))
		self.cards = list(i)


class Hand(Cards):
	def __init__(self):
		Cards.__init__(self)
		
	# Returns the positions of all cards in the hand, that have the
	# specified value.
	def pos_of_cards_with_value(self,value):
		pass # TODO
	
	def pop_cards_at_positions(self,positions):
		pass # TODO
	
	
	
	

class DiscardPile(Cards):
	# Peaks in the top cards of the deck until a card
	# does not have the specified value. The number
	# of cards having the specified value is returned.
	def peak_until_other_value(self,value):
		pass # TODO: implement


class UpAndDownCards:
	def reachableUp(self):
		pass
	def reachableDown(self):
		pass


if __name__ == "__main__":	
	cards = Pile()
	cards.shuffle()
	print cards
