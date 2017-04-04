from cards import *


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
        self.hand = Hand(hidden = !hero) # if villain, then the hand is hidden
        self.upcards = UpDownCards(num_up_down, hidden = False)
        self.downcards = UpDownCards(num_up_down, hidden = True)


class Game:
    """
    This class contains all of the game logic.
    """
    
    def __init__(self, settings):
        self.settings = settings
        
        # create and shuffle deck:
        self.deck = Deck()
        self.deck.shuffle()
        
        # create other card collections:
        self.discardpile = DiscardPile()
        self.graveyard = Graveyard()
        
        # create players:
        hero = Player(settings["NCARDS_UPDOWN"], True)
        villain = Player(settings["NCARDS_UPDOWN"], False)
        self.players = (hero,villain)
        
        self.initialdeal()
        
        # the minimal value that can be played
        # (in the beginning every card can be played):
        self.minval = 0
        # the player whos turn it is right now:
        self.curplayer = self.findfirstplayer()
        self.curplayer = 0 # TODO: remove
        
    def initialdeal(self):
        pass