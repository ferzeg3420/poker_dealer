from .card_h import *

class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []
        self.showdown_hand = ""
        self.chips = 0
        self.wins = 0
        self.blind = Blind.no_blind

    def __repr__(self):
        ret_str = "hand: " + \
         str(self.hand)    + \
         "; chips: "       + \
         str(self.chips)   + \
         "; blind: "       + \
         str(self.blind.name)
        return ret_str

    def fold(self):
        self.hand.clear()

    def get_hand(self):
        return [self.hand[0], self.hand[1]]

    def hand_stringify(self):
        if len(self.hand) != 2: # for texas holdem
            return "ERROR"

        first_card = self.hand[0]
        second_card = self.hand[1]
        
        if first_card.value == '10':
            first_card_str = "| " + str(first_card) + " |"
        else:
            first_card_str = "| " + str(first_card) + "  |"

        if second_card.value == '10':
            second_card_str = "| " + str(second_card) + " |"
        else:
            second_card_str = "| " + str(second_card) + "  |"

        return  "Player "          \
                + str(self.id)     \
                + "\n"             \
                + first_card_str   \
                + " "              \
                + second_card_str

    def __eq__(self, other):
        return self.id == other.id    

    @staticmethod
    def get_num_players_from_user(msg):
        num_players = -1
        while num_players < 0 or num_players > 9:
            print(msg)
            num_players_str = input()
            if num_players_str == "q":
                exit()
            if num_players_str == "":
                continue
            if len(num_players_str) > 1 or num_players_str not in "0123456789":
                continue
            num_players = int(num_players_str)
        return num_players
