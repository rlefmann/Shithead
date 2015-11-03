#coding: utf-8

import itertools
from random import shuffle

num_values = 13
num_suits = 4

#class Card(tuple):
#	def value(self):
#		return self[0]
#	def suit(self):
#		return self[1]

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

	def pop_card(self,pos):
		if pos<0 or pos>=len(self.cards):
			#TODO: throw exception
			pass
		else:
			popped_card = self.cards[pos]
			del self.cards[pos]
			return popped_card
	
	def add_card(self,card):
		self.cards.append(card)

	def add_cards(self,new_cards):
		for card in new_cards:
			self.add_card(card)
	
	def remove_card(self,index): 
		if index<0 or index>=len(self.cards):
			#TODO: throw exception
			pass
		else:
			del self.cards[index]
	
	def remove_cards(self,indices):
		for index in indices:
			self.remove_card(index)


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
		positions=[]
		for i in range(len(self.cards)):
			if self.cards[i][0] == value:
				positions.append(i)
		return positions
	
	def pop_cards_at_positions(self,positions):
		popped_cards =[]
		for pos in positions:
			p = self.pop_card(pos)
			popped_cards.append(p)
		return popped_cards
	

class DiscardPile(Cards):
	# Peaks in the top cards of the deck until a card
	# does not have the specified value. The number
	# of cards having the specified value is returned.
	def peak_until_other_value(self,value):
		counter=0
		while self.cards[counter][0] == value:
			counter+=1
		return counter
	
	def clear(self):
		self.cards=[]
		


#class UpAndDownCards:
#	def reachableUp(self):
#		pass
#	def reachableDown(self):
#		pass


if __name__ == "__main__":	
	cards = Pile()
	cards.shuffle()
	print cards
	d = cards.pop_card(3)
	print d
	print cards
	
