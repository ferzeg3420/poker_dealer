# Attributions to slideshare for the neat list comprehensions
# more attributions

from card_h import Card, Suit, Blind
from community_cards_h import *
from deck_h import *
from player_h import *
from user_h import *
import util
import ranker
import ascii
import time

MAX_PLAYERS = 9
NUM_COMMUNITY_CARDS = 5
NUM_SIMULATIONS = 100000
CARDS_IN_FLOP = 3

ROYAL_FLUSH = 91413121110
STRAIGHT_FLUSH = 90000000000
FOUR_OF_A_KIND = 80000000000
FULL_HOUSE = 70000000000 
FLUSH = 60000000000 
STRAIGHT = 50000000000
THREE_OF_A_KIND = 40000000000 
TWO_PAIR = 30000000000 
PAIR = 20000000000 
HIGH_CARD = 10000000000 

def setup_known_hands(deck, all_players, players_cards):
	for i, pc in enumerate(players_cards, start=0):
		card1 = pc[0]
		card2 = pc[1]
		new_hand = \
			[ deck.deal_specific_card(card1), \
			 deck.deal_specific_card(card2) ]
		all_players[i].hand = new_hand

def get_hand_name(hand_score):
	if hand_score == ROYAL_FLUSH:
		return "royal flush"
	if hand_score > STRAIGHT_FLUSH:
		return "straight flush"
	if hand_score > FOUR_OF_A_KIND:
		return "four of a kind"
	if hand_score > FULL_HOUSE:
		return "full house"
	if hand_score > FLUSH:
		return "flush"
	if hand_score > STRAIGHT:
		return "straight"
	if hand_score > THREE_OF_A_KIND:
		return "three of a kind"
	if hand_score > TWO_PAIR:
		return "two pair"
	if hand_score > PAIR:
		return "pair"
	if hand_score > HIGH_CARD:
		return "high card"
	return "ERROR"

def display_winning_hand_ranking(winners):
	first_winner = winners[0]
	winning_hand_score = first_winner[1]
	print(get_hand_name(winning_hand_score))

def sim_street(deck, all_players, player_cards, comm_cards):
	wins = 0
	num_simulations = NUM_SIMULATIONS
	num_players = -1
	while num_players < len(player_cards):
		num_players = Player.get_num_players_from_user('Number of players: ')
	for i in range(num_simulations):
		community_cards = Community_cards()
		deck.shuffle()
		setup_known_hands(deck, all_players, players_cards)
		players = [ all_players[i] for i in range(0, num_players) ]
		other_players = \
			[ all_players[i] for i in range(len(players_cards), num_players) ]

		for i in range(NUM_COMMUNITY_CARDS):
			if i < len(comm_cards):
				community_cards.append(deck.deal_specific_card(comm_cards[i]))
			else:
				community_cards.append(deck.deal_card())

		deck.deal_player_hands(other_players)

		if len(players_cards) == 0:
			winners = ranker.find_winners(other_players, community_cards)
		else:
			winners = ranker.find_winners(players, community_cards)

		display_winning_hand_ranking(winners)

		util.clear_player_hands(players)

def get_player_flop(taken):
	flop = [] 
	for i in range(1, CARDS_IN_FLOP + 1):
		card =  Card.get_card_from_user("Flop " + str(i) + ": ", taken)
		flop.append( card )
		taken.append( card )
	return flop

def get_player_hand(taken, player_id):
	print("Player ", player_id, ":", sep='')
	player_hand = []
	card1 = Card.get_card_from_user("First card:", taken)
	taken.append(card1)
	player_hand.append(card1)
	card2 = Card.get_card_from_user("Second card:", taken)
	player_hand.append(card2)
	taken.append(card2)
	
	print("your hand:")
	print(card1)
	print(card2)
	print()
	return player_hand

if __name__ == "__main__":
	util.clear_logs()
	util.clear_screen()
	print("Texas hold'em simulations")
	if input() == 'q': exit()
	deck = Deck()
	all_players = [ Player(p_id) for p_id in range(1, MAX_PLAYERS + 1) ]
	get_user_msg = "Number of players with known hands: "
	util.clear_screen()

	while True:
		taken_cards = []
		num_known_hands = Player.get_num_players_from_user(get_user_msg)
		players_cards = []
		for i in range(1, num_known_hands + 1):
			hand = get_player_hand(taken_cards, i)
			players_cards.append(hand)

		community_cards = []
		sim_street(deck, all_players, players_cards, community_cards)
