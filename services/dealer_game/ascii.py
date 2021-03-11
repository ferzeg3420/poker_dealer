# 30 chars per line.
import sys
from .util import *

is_windows = hasattr(sys, 'getwindowsversion')

def print_welcome():
    print("\n\n\n\nFERNANDO'S SUPER POKER SIMULATOR 3000\n\n\n\n")
    input()
    clear_screen()

def show_rankings():
    if is_windows:
        show_rankings_windows()
    else:
        show_rankings_unix()

def show_rankings_windows():

    clear_screen()
    print()
    print("     ♠ ♥ ♦ ♣ Hand Rankings ♠ ♥ ♦ ♣")
    print()
    
    print(" Royal Flush")
    print(" | A♠  | | K♠  | | Q♠  | | J♠  | | 10♠ |")
    print()
    
    print(" Straight Flush")
    print(" | 9♦  | | 8♦  | | 7♦  | | 6♦  | | 5♦  |")
    print()
    
    print(" Four of a Kind")
    print(" | A♣  | | A♥  | | A♠  | | A♦  | | 10♠ |")
    print()
    
    print(" Full House")
    print(" | Q♥  | | Q♠  | | Q♦  | | J♣  | | J♦  |")
    print()
    
    print(" Flush")
    print(" | A♥  | | J♥  | | 9♥  | | 6♥  | | 3♥  |")
    print()
    
    print(" Straight")
    print(" | 9♣  | | 8♦  | | 7♠  | | 6♦  | | 5♠  |")
    print()
    
    print(" Three of a Kind")
    print(" | 5♦♢  | | Q♣  | | 2♥  | | 2♠  | | 2♦  |")
    print()
    
    print(" Two Pair")
    print(" | A♥  | | A♣  | | Q♥  | | Q♠  | | 9♦  |")
    print()
    
    print(" One Pair")
    print(" | 4♥  | | 5♠  | | 8♣  | | A♦  | | A♠  |")
    print()
    
    print(" High Card")
    print(" | 5♠  | | 6♦  | | J♣  | | Q♦  | | A♠  |")
    print()
    
    input()
    clear_screen()

def show_rankings_unix():
    clear_screen()
    print()
    print("     ♤ ♡ ♢ ♧ Hand Rankings ♠ ♥ ♦ ♣")
    print()
    
    print(" Royal Flush")
    print(" | A♠  | | K♠  | | Q♠  | | J♠  | | 10♠ |")
    print()
    
    print(" Straight Flush")
    print(" | 9♢  | | 8♢  | | 7♢  | | 6♢  | | 5♢  |")
    print()
    
    print(" Four of a Kind")
    print(" | A♣  | | A♡  | | A♠  | | A♢  | | 10♠ |")
    print()
    
    print(" Full House")
    print(" | Q♡  | | Q♠  | | Q♢  | | J♣  | | J♢  |")
    print()
    
    print(" Flush")
    print(" | A♡  | | J♡  | | 9♡  | | 6♡  | | 3♡  |")
    print()
    
    print(" Straight")
    print(" | 9♣  | | 8♢  | | 7♠  | | 6♢  | | 5♠  |")
    print()
    
    print(" Three of a Kind")
    print(" | 5♢  | | Q♣  | | 2♡  | | 2♠  | | 2♢  |")
    print()
    
    print(" Two Pair")
    print(" | A♡  | | A♣  | | Q♡  | | Q♠  | | 9♢  |")
    print()
    
    print(" One Pair")
    print(" | 4♡  | | 5♠  | | 8♣  | | A♢  | | A♠  |")
    print()
    
    print(" High Card")
    print(" | 5♠  | | 6♢  | | J♣  | | Q♢  | | A♠  |")
    print()
    
    input()
    clear_screen()

def get_suit(card):
    return str(card)[-1]

def get_card_len(card):
    return len(str(card))

def show_cards(cards):
    len_bw_cards = 10
    if len(cards) == 3:
        top_left_first_card  = 31
        center_first_card  = 94
        bottom_right_first_card  = 158
        res_str  = "+-------+ +-------+ +-------+\n"
        res_str += "|       | |       | |       |\n"
        res_str += "|       | |       | |       |\n"
        res_str += "|       | |       | |       |\n"
        res_str += "|       | |       | |       |\n"
        res_str += "|       | |       | |       |\n"
        res_str += "+-------+ +-------+ +-------+\n"
    elif len(cards) == 4:
        top_left_first_card  = 41
        center_first_card  = 124
        bottom_right_first_card  = 208
        res_str  = "+-------+ +-------+ +-------+ +-------+\n"
        res_str += "|       | |       | |       | |       |\n"
        res_str += "|       | |       | |       | |       |\n"
        res_str += "|       | |       | |       | |       |\n"
        res_str += "|       | |       | |       | |       |\n"
        res_str += "|       | |       | |       | |       |\n"
        res_str += "+-------+ +-------+ +-------+ +-------+\n"
    elif len(cards) == 5:
        top_left_first_card  = 51
        center_first_card  = 154
        bottom_right_first_card  = 258
        res_str  = "+-------+ +-------+ +-------+ +-------+ +-------+\n"
        res_str += "|       | |       | |       | |       | |       |\n"
        res_str += "|       | |       | |       | |       | |       |\n"
        res_str += "|       | |       | |       | |       | |       |\n"
        res_str += "|       | |       | |       | |       | |       |\n"
        res_str += "|       | |       | |       | |       | |       |\n"
        res_str += "+-------+ +-------+ +-------+ +-------+ +-------+\n"
    

    for i, c in enumerate(cards, start = 0):
        top_left = top_left_first_card + i * len_bw_cards
        center = center_first_card + i * len_bw_cards
        bottom_right = bottom_right_first_card + i * len_bw_cards
        len_card = get_card_len(c)
        res_str = res_str[:top_left]                \
                        + str(c)                                       \
                        + res_str[top_left + len_card:]
        
        res_str = res_str[:center]         \
                        + get_suit(c)                             \
                        + res_str[center + 1:]
        
        res_str = res_str[:bottom_right - len_card]   \
                        + str(c)                                           \
                        + res_str[bottom_right:]
    return res_str
