from enum import Enum
from .util import *
import sys
import random

is_windows = hasattr(sys, 'getwindowsversion')

class Blind(Enum):
    dealer = 1
    big_blind = 2
    small_blind = 3
    no_blind = 4

class Suit(Enum):
    spades = 1
    hearts = 2
    diamonds = 3
    clubs = 4

valid_suits = [ 'D', 'H', 'S', 'C' ]

values = [ 'A' , \
           '2' , \
           '3' , \
           '4' , \
           '5' , \
           '6' , \
           '7' , \
           '8' , \
           '9' , \
           '10', \
           'J' , \
           'Q' , \
           'K' ]

def preprocess_user_card(card):
    return ''.join(c for c in card if c not in ' ofOF')

def get_pos_value(card):
    val = card.get_value_as_int()
    if val == 14:
        val = 0
    else:
        val = val - 1
    st = card.suit
    if st == Suit.spades:
        st_val = 0
    elif st == Suit.hearts:
        st_val = 1
    elif st == Suit.diamonds:
        st_val = 2
    elif st == Suit.clubs:
        st_val = 3
    return st_val * 13 + val

def is_taken(card, taken):
    for c in taken:
        if card.is_same(c):
            return True
    return False

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return self.display_card()

    def display_card(self):
        if self.suit == Suit.spades:
            suit = "♠"
        elif self.suit == Suit.hearts:
            if is_windows:
                suit = "♥"
            else: #unix-like
                suit = "♡"
        elif self.suit == Suit.diamonds:
            if is_windows:
                suit = "♦"
            else: #unix-like
                suit = "♢"
        elif self.suit == Suit.clubs:
            suit = "♣"
        else:
            print ("ERROR")    
        return self.value + suit

    def get_value_as_int(self):
        value = 0
        if self.value == 'A':
            value = 14
        elif self.value == 'J':
            value = 11
        elif self.value == 'Q':    
            value = 12
        elif self.value == 'K':    
            value = 13
        else:
            value = int(self.value)
        return value

    def is_same(self, other):
        return self.get_value_as_int() == other.get_value_as_int() \
                 and self.suit == other.suit

    def is_same_value(self, other):
        return self.get_value_as_int() == other.get_value_as_int()

    def __lt__(self, other):
        return self.get_value_as_int() < other.get_value_as_int()    

    def __eq__(self, other):
        return self.get_value_as_int() == other.get_value_as_int()    

    @staticmethod
    def get_random_card(taken):
        taken = sorted(taken, key=lambda c: get_pos_value(c), reverse=True)
        #print("getting random card")
        all_cards = [ Card(value, suit) for suit in Suit for value in values ]
        for tc in taken:
            to_pop = get_pos_value(tc)
            all_cards.pop( to_pop )
        #print(all_cards)
        random.shuffle(all_cards)
        #print(all_cards)
        return all_cards.pop(0) 

    @staticmethod
    def get_card_from_user(msg, taken):
        while True:
            card = preprocess_user_card(input(msg))
            card = card.upper()
            if card == '':
                continue
            if card[0] == 'Q' and len(card) == 1:
                exit()
            if card[0] == 'R':
                return Card.get_random_card(taken)

            if len(card) < 2:
                continue
            elif card[0] == '1' and card[1] == '0':
                value = '10'
                suit = card[2]
            elif card[0] == '1':
                continue
            else:
                value = card[0]
                suit = card[1]
    
            if value not in values:
                continue
            if suit not in valid_suits:
                continue
    
            if suit == 'D':
                ret_card = Card(value, Suit.diamonds)
            elif suit == 'H':
                ret_card = Card(value, Suit.hearts)
            elif suit == 'S':
                ret_card = Card(value, Suit.spades)
            elif suit == 'C':
                ret_card = Card(value, Suit.clubs)
            else: continue

            if is_taken(ret_card, taken):
                continue
            return ret_card
