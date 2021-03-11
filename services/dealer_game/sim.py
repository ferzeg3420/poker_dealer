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
NUM_SIMULATIONS = 10000
CARDS_IN_FLOP = 3

def setup_known_hands(deck, all_players, players_cards):
	for i, pc in enumerate(players_cards, start=0):
		card1 = pc[0]
		card2 = pc[1]
		new_hand = \
			[ deck.deal_specific_card(card1), \
			 deck.deal_specific_card(card2) ]
		all_players[i].hand = new_hand

def display_wins(num_simulations, all_players, num_known_hands):
	print("Win percentage after",         \
		  NUM_SIMULATIONS,                \
		  "simulations (includes ties)")

	for i in range(num_known_hands):
		p = all_players[i]
		print("Player ", p.id, ":", sep='') 
		print('~' + str(int((p.wins / num_simulations) * 100)) + '%')
		p.wins = 0
	print()

def sim_street(deck, all_players, player_cards, comm_cards):
	wins = 0
	num_simulations = NUM_SIMULATIONS
	num_players = 0
	while num_players < len(player_cards) or num_players == 0:
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

		for p in winners:
			p[0].wins += 1
		util.clear_player_hands(players)
	display_wins(num_simulations, all_players, len(player_cards))

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
	print("q to exit")
	print("r for random cards")
	print("10h = ten of hearts")
	print("as = ace of spades")
	print("2c = 2 of clubs, d diamonds, and so on (case insensitive).")
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
		print("Preflop")
		sim_street(deck, all_players, players_cards, community_cards)

		community_cards = get_player_flop(taken_cards)

		print(community_cards)
		sim_street(deck, all_players, players_cards, community_cards)

		card = Card.get_card_from_user("Turn card: ", taken_cards)
		taken_cards.append( card )
		community_cards.append( card )
		print(community_cards)
		sim_street(deck, all_players, players_cards, community_cards)

		card = Card.get_card_from_user("River card: ", taken_cards)
		taken_cards.append( card )
		community_cards.append( card )
		print(community_cards)
		sim_street(deck, all_players, players_cards, community_cards)
