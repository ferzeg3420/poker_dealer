import random
from .card_h import *

class Deck:
    def __init__(self):
        self.reset()
        
    def reset(self):
        #values = ['A'] + list(map(str, range(2, 11))) + [ 'J', 'Q', 'K' ]
        self.cards = \
            [ Card(value, suit) for suit in Suit for value in values ]

    def shuffle(self):
        self.reset()
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)
    
    def deal_specific_card(self, card):
        for i, c in enumerate(self.cards):
            if c.is_same(card):
                temp = c
                self.cards.pop(i)
                return temp
        assert False
        return Card('0', Suit.spades)

    def deal_player_hands(self, players):
        for i in range(len(players)):
            players[i].hand.append( self.deal_card() )
            players[i].hand.append( self.deal_card() )

    def deal_flop_as_list(self):
        return [ self.deal_card() for i in range(3) ]

    def __repr__(self):
        return str([ c for c in self.cards ])
