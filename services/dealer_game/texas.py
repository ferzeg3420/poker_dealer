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

def get_level(score):
	return (score // 10) + 1

def get_num_players_from_level(level):
	if level > 8:
		return MAX_PLAYERS
	else:
		return level + 1

def draw_screen(screen, is_pause):
	user = screen[0]
	playing_hands = screen[1]
	community_cards = screen[2]
	tutorial_msg = screen[3]

	util.clear_screen()
	to_draw = str(user) + playing_hands + str(community_cards) + tutorial_msg
	print(to_draw)
	if is_pause:
		util.process_continuation_input(to_draw)

def get_user_guess(screen):
	guess = ""
	draw_screen(screen, is_pause=False)
	while guess not in list("123456789") :
		guess =  \
			input("Who's the winner? (use the player's number as your guess) ")
		if guess == "q":
			exit()
		if guess == "r":
			ascii.show_rankings()
			draw_screen(screen, is_pause=False)
	return int(guess)

def is_guess_in_players(guess, players):
	for p in players:
		if p[0].id == guess:
			return True
	return False

def is_right_guess(guess, winners):
	return is_guess_in_players(guess, winners)

def process_user_guess(guess, user, winners):
	if is_right_guess(guess, winners):
		user.score += 2
		result_message = "\n\nYou're right!"
	else:
		user.lives -= 1
		result_message = "\n\nSorry, keep trying!"
	return result_message

def congratulate_winner(screen, winners, guess_msg):
	winner_message = guess_msg + "\n" + get_showdown(winners)	
	if len(winners) == 1:
		winner_message += "has the best hand!"
	else:
		winner_message += "have the best hand!"
		
	screen[3] += winner_message                       
	draw_screen(screen, is_pause=True)

def get_showdown(players):
	res_str = ""
	for p in players:
		res_str += p[0].showdown_hand + "\n"
	return res_str

def setup_blinds(dealer, num_players):
	return dealer
		
if __name__ == "__main__":
	util.clear_screen()
	util.clear_logs()
	ascii.print_welcome()
	user = User(score=0, lives=3)
	deck = Deck()
	level = 1
	game_round = 1
	dealer = 1
	small_blind = 0
	is_tutorial = util.is_tutorial_mode()
	if is_tutorial:
		util.show_tutorial()
	else:
		start_time = time.perf_counter()
	all_players = [ Player(p_id) for p_id in range(1, MAX_PLAYERS + 1) ]
	
	while True:	
		level = get_level(user.score)
		num_players = get_num_players_from_level(level)
		dealer = (dealer % num_players) + 1
		if num_players == 2:
			small_blind = dealer
		else:
			small_blind = dealer % num_players + 1
		big_blind = small_blind % num_players + 1
		community_cards = Community_cards()
		deck.shuffle()
		players = [ all_players[i] for i in range(0, num_players) ]
		deck.deal_player_hands(players)
		tutorial_msg = ""
			
		playing_hands = ""
		for player in players:
			playing_hands += player.hand_stringify()
			if player.id == dealer:
				playing_hands += "  Dealer"
			if player.id == small_blind:
				playing_hands += "  Small Blind"
			elif player.id == big_blind:
				playing_hands += "  Big Blind"
			playing_hands += "\n\n"

		screen = [user, playing_hands, community_cards, tutorial_msg]

		#preflop
		draw_screen(screen, is_pause=True)

		#flop
		community_cards.append(deck.deal_flop_as_list())
		draw_screen(screen, is_pause=True)

		#turn
		community_cards.append(deck.deal_card())
		draw_screen(screen, is_pause=True)

		#river
		community_cards.append(deck.deal_card())
		draw_screen(screen, is_pause=True)

		winners = ranker.find_winners(players, community_cards)
		if is_tutorial:
			screen[3] = "\n\nBest hands:\n" + get_showdown(players)	
		guess = get_user_guess(screen)
		guess_msg = process_user_guess(guess, user, winners)
		congratulate_winner(screen, winners, guess_msg)

		util.record_hands(players, winners, game_round)
		util.clear_player_hands(players)
		game_round += 1
		if user.lives <= 0 or user.score >= 100:
			break

	print( "Final score:", user.score, "great Job!" )
	if not is_tutorial:
		play_time = (time.perf_counter() - start_time)/60 #in minutes
	input()
	if not is_tutorial:
		util.save_score(user, play_time)
