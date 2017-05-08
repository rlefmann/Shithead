Classes
=======
:toc: left

## Module Game

### Public Methods

* can_play_handcards(indices)
* can_play_upcards(indices)
* can_play_downcards(indices)
* play_handcards(indices)
* play_upcards(indices)
* play_downcards(indices)
* can_take()
* can_take_upcards(indices)
* take()
* take_upcards(indices)
* take_downcard()
* redraw()
* is_win()
* switch_player()

Also the `Game` class has several properties for returning cardstring
representations of the various `CardCollections`:

* curhand
* curupcards
* curdowncards
* phand
* pupcards
* pdowncards
* vhand
* vupcards
* vdowncards
* deck
* discardpile

## Module cards

### Card

A card has a suit and a rank. Both are integers starting at 0:

* rank: 0->2, 1->3, ..., 9->J, 10->Q, 11->K, 12->A
* suit: 0->diamonds, 1->hearts, 2->spades, 3->clubs

It has also a property value which computes
a value that is unique for each value combination of suit and rank. It is
used for sorting a list of cards (which is done in the Hand class).

### CardCollection

Represents a set of cards and is the base class for most game objects like a players hand, the discard pile, and the deck from which the players replenish their hands. The inheritance hierarchy looks like this:

* CardCollection
** Hand
** Pile
*** DrawPile (HiddenPile, Deck)
*** DiscardPile (the discard pile of the game and the graveyard)
** CardRow

A CardCollection is basically a list of cards which can be either visible
or hidden (the effect of this varies by subclass).

### Hand

The hand are the cards held by one player. If it is the human player, all
cards are visible to him, if it is a computer opponent you cannot see any of the cards.

* The hand is sortable, because we want the player to easily see what ranks his cards have. The `sort` method uses the `value` property of the `Card` class.
* The `add` method of the superclass `CardCollection` is extended by calling the sort method such that the hand is always sorted.

### Pile

A pile or stack is a set of cards that are placed on top of each other. A pile is visible if its last card is visbile and he other cards are covered by it. If the pile is hidden, all the cards are placed face-down. Because at most one card is visible, the `Pile` class overrides the `__repr__` and `cardstrings` methods of the base class.

### DrawPile

A draw pile is a pile of cards that is placed face down.


The deck is a special draw pile that contains all of the cards in the
beginning of the game. A deck is created via the class method `create_deck`, such that that we can do

----
deck = DrawPile.create_deck()
----

### DiscardPile

A discard pile is a pile of cards that is placed face up, such that you can see the top card (but not the cards underneath it).

### CardRow

A `CardRow` object is a set of a fixed number of places, each of which can be `None` or hold a `Card`. Either all of the cards are visible (this is the case for the upcards in Shithead) or all of the cards are hidden (this is the case for the downcards).
