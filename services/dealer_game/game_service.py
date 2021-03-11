from .card_h import Card, Suit, Blind
from .community_cards_h import *
from .deck_h import *
from .player_h import *
from .user_h import *
from .ranker import *
from .util import *
import time

MAX_PLAYERS = 9

def get_level(score):
    return (score // 10) + 1

def get_num_players_from_level(level):
    if level > 8:
        return MAX_PLAYERS
    else:
        return level + 1

def is_guess_in_players(guess, players):
    for p in players:
        if p[0].id == guess:
              return True
    return False

def is_right_guess(guess, winners):
    return is_guess_in_players(guess, winners)
    
# should return score modifier
def process_user_guess(guess, user, winners):
    if is_right_guess(guess, winners):
        user.score += 2
        result_message = "\n\nYou're right!"
    else:
        user.lives -= 1
        result_message = "\n\nSorry, keep trying!"
    return result_message

def game_service(score):
    deck = Deck()
    all_players = [ Player(p_id) for p_id in range(1, MAX_PLAYERS + 1) ]
    level = get_level(score)
    num_players = get_num_players_from_level(level)
    community_cards = Community_cards()
    deck.shuffle()
    players = [ all_players[i] for i in range(0, num_players) ]
    deck.deal_player_hands(players)
    community_cards.append(deck.deal_flop_as_list())
    community_cards.append(deck.deal_card())
    community_cards.append(deck.deal_card())
    winners = find_winners(players, community_cards)
    res = {
        "players": formatted_players(players),
        "board": formatted_community_cards(community_cards),
        "winners": formatted_winners(winners),
    }
    return res
