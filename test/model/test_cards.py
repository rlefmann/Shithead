import unittest
from shithead.model.cards import *

class CardTest(unittest.TestCase):
    """
    Tests the card class.
    """
    def test_card1(self):
        c = Card(10,3)
        self.assertEqual(c.value, 43)
        self.assertEqual(c.__repr__(), "qc")
        # The repr function returns a KeyError when the rank or suit are
        # smaller than 0 or larger than 12/3
        c = Card(13,5)
        self.assertRaises(KeyError, c.__repr__)

        
#~ class CardCollectionTest(unittest.TestCase):
    #~ def setUp(self):
        #~ """
        #~ Creates a CardCollection and three Cards.
        #~ """
        #~ self.cc = CardCollection()
        #~ self.c1 = Card(10,3)
        #~ self.c2 = Card(5,0)
        #~ self.c3 = Card(8,1)
    
    #~ def test_cc_1(self):
        #~ """
        #~ Tests adding cards to the collection.
        #~ """
        #~ self.assertEqual(self.cc.hidden, False)
        #~ self.assertEqual(len(self.cc), 0)
        #~ self.cc.add([self.c1, self.c2, self.c3])
        #~ self.assertEqual(len(self.cc), 3)
        #~ # only a list of cards can be added:
        #~ self.assertRaises(TypeError, self.cc.add, self.c1)
    
    #~ def test_cc_2(self):
		#~ """
		#~ Tests removing cards from the collection.
		#~ """
		#~ self.cc.add([self.c1, self.c2, self.c3, self.c3, self.c2, self.c1])
		#~ # you must remove a list or range of indices:
		#~ self.assertRaises(TypeError, self.cc.remove, self.c1)
		#~ self.assertRaises(TypeError, self.cc.remove, 0)
		#~ # you have to remove at least one index:
		#~ self.assertRaises(ValueError, self.cc.remove, [])
		#~ # removing a range:
		#~ self.cc.remove(range(3))
		#~ self.assertEqual(len(self.cc), 3)
		#~ self.assertEqual(self.cc.cards[0].rank, 8)
		#~ # now remove list of indices:
		#~ self.cc.remove([1,2])
		#~ self.assertEqual(len(self.cc), 1)
		#~ self.assertEqual(self.cc.cards[0].rank, 8)
		
		
if __name__ == "__main__":
    unittest.main(exit=False)
