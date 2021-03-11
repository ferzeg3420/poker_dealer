from .ascii import *

class Community_cards:
    def __init__(self):
        self.cards = []

    def __repr__(self):
        if len(self.cards) == 0:
            return "\n\n\n\n\n\n\n\nPre-flop"
        if len(self.cards) == 3:
            return show_cards(self.cards) + "\nFlop"
        elif len(self.cards) == 4:
            return show_cards(self.cards) + "\nTurn"
        elif len(self.cards) == 5:
            return show_cards(self.cards) + "\nRiver"

    def append(self, cards):
        if type(cards) == type(list()):
            for c in cards:
                self.cards.append(c)
        else:
            self.cards.append(cards)

    def reset(self):
        self.cards.clear()
