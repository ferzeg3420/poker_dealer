from os import system
from .ascii import *
import sys

is_windows = hasattr(sys, 'getwindowsversion')
MAX_TIME = 999999.99
MAX_SCORE = 99999

winning_hand_log_filename = "winning_hands.log"
losing_hand_log_filename = "losing_hands.log"

suitToName = [
  "None",
  "Spades",
  "Hearts",
  "Diamonds",
  "Clubs"
]

#def suitToName(suitEnum):
#    print(suitEnum._value_)
#    if suitEnum == "Suit.spades":
#        return "Spades"
#    elif suitEnum == "Suit.hearts":
#        return "Hearts"
#    elif suitEnum == "Suit.diamonds":
#        return "Diamonds"
#    elif suitEnum == "Suit.clubs":
#        return "Clubs"
#    else:
#        return None

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

def get_hand_name(hand_score):
    if hand_score == ROYAL_FLUSH:
        return "Royal flush"
    if hand_score > STRAIGHT_FLUSH:
        return "Straight Flush"
    if hand_score > FOUR_OF_A_KIND:
        return "Four of a Lind"
    if hand_score > FULL_HOUSE:
        return "Full House"
    if hand_score > FLUSH:
        return "Flush"
    if hand_score > STRAIGHT:
        return "Straight"
    if hand_score > THREE_OF_A_KIND:
        return "Three of a Kind"
    if hand_score > TWO_PAIR:
        return "Two Pair"
    if hand_score > PAIR:
        return "Pair"
    if hand_score > HIGH_CARD:
        return "High Card"
    return "ERROR"

def clear_screen():
    if is_windows:
        system('cls')
    else:
        system('clear')

def lives_2_hearts(lives):
    hearts_str = ""
    if is_windows:
        for i in range(lives):
            hearts_str += "♥"
        for i in range(lives):
            hearts_str += " "
    else:
        for i in range(lives):
            hearts_str += "♥"
        for i in range(3 - lives):
            hearts_str += "♡"
    return hearts_str    

def pause(page):
    while True:
        user_input = input("")
        if user_input == 'q':
            clear_screen()
            exit()
        elif user_input == 'r':
            show_rankings()
        else:
            break
        print(page)

def show_tutorial():
    page1 = open("tutorial_page_1.txt", "r")
    page1_str = page1.read()
    page2 = open("tutorial_page_2.txt", "r")
    page2_str = page2.read()
    clear_screen()
    print(page1_str)
    pause(page1_str)
    clear_screen()
    print(page2_str)
    pause(page2_str)

def show_instructions():
    page1 = open("instructions_page_1.txt", "r")
    page1_str = page1.read()
    page2 = open("instructions_page_2.txt", "r")
    page2_str = page2.read()
    clear_screen()
    print(page1_str)
    pause(page1_str)
    clear_screen()
    print(page2_str)
    pause(page2_str)

def is_tutorial_mode(): 
    answer = 'x'
    while answer != 'y' and answer != 'n':
        print("Would you like to play in tutorial mode? (y/n) q to exit")
        answer = input()
        if answer == "":
            continue
        if answer == "q":
            exit()
    return answer == 'y'

def clear_player_hands(players):
    for player in players:
        player.fold()

def process_continuation_input(state):
    while True:
        user_input = input("")
        if user_input == 'q':
            clear_screen()
            exit()
        elif user_input == 'r':
            show_rankings()
        elif user_input == 'i':
            show_instructions()
        else:
            break
        print(state)
    
def print_preflop(board_state):
    print(board_state + "\n\n\n\n\n\n\n\nPre-flop")

def clear_logs():
    f = open(winning_hand_log_filename, 'w', encoding='utf-8')
    f.close()
    f = open(losing_hand_log_filename, 'w', encoding='utf-8')
    f.close()

def write_to_file(filename, text):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(text)

def record_hands(players, winners, game_round):
    for p in players:
        is_winner = False
        for w in winners:
            if w[0].id == p.id:
                is_winner = True
                break
        msg = "R " + str(game_round) + ", "
        if is_winner:
            msg += p.hand_stringify() + "\n"
            write_to_file(winning_hand_log_filename, msg)
        else:
            msg += p.hand_stringify() + "\n"
            write_to_file(losing_hand_log_filename, msg)
            

def get_user_name():
    name = ""
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz" 
    digits = "1234567890"
    allowed_characters = uppercase + lowercase + digits + " " + "_"
    while(True):
        bad_chars = False
        name = input("Your name:")
        if len(name) > 20:
            continue
        if len(name) == 0:
            continue
        for c in name:
            if c not in allowed_characters:
                bad_chars = True
                break
        if not bad_chars:
            break
    return name

def draw_scoreboard(entries):
    clear_screen()
    print()
    print("                 HIGHEST CASH-INS")
    print("######################################################## ")
    print('|    {:<30}{:>6} {:>10}   |'.format("Name", "Made", "In"))
    print("######################################################## ")
    for i, e in enumerate(entries, start=1):
        print('| {:<2} {:<30}{:>6} {:>10}   |'.format(str(i),               \
                                                      e.get("name"),        \
                                                      '$' + e.get("score"), \
                                                      e.get("time") + 'm'))
        print("+------------------------------------------------------+ ")

def save_score(user, play_time):
    if play_time > MAX_TIME:
        play_time = MAX_TIME
    if user.score > MAX_SCORE:
        user.score = MAX_SCORE
    entries = []
    with open("score_board.csv", "r") as file:
        for line in file:
            print(line)
            name, score, time = line.split(',')
            time = time[:-1] # get rid of new line
            entries.append({"name": name, "score": score, "time": time})

    draw_scoreboard(entries)
    name = get_user_name()
    entries.append({"name": name,             \
                    "score": str(user.score), \
                    "time": '{:.2f}'.format(play_time)})

    entries.sort(reverse=True, \
                 key=lambda e: (float(e.get('score')), float(e.get('time'))))
    score_board_w = open("score_board.csv", "w")
    for e in entries[:10]:
        score_board_w.write(e.get("name")  + "," +\
                            e.get("score") + "," + \
                            e.get("time")  + "\n")
    draw_scoreboard(entries)
    input()

def formatted_best_hand(winners):
    highest_score = 0
    for w in winners:
        player = w[0]
        score = w[1]
        if score > highest_score:
            highest_score = score
    print("israeli fiance:", get_hand_name(highest_score))
    return get_hand_name(highest_score)
     

def formatted_winners(winners):
    winners_res = [ i[0].id for i in winners ]
    return winners_res

def formatted_community_cards(community_cards):
    community_cards_res = []
    for card in community_cards.cards:
        community_cards_res.append(
            'card{}{}.png'.format(suitToName[card.suit._value_],
                                  card.value)
        )
    return community_cards_res

def formatted_players(players):
    players_res = []
    for player in players:
        card1 = player.hand[0]
        card2 = player.hand[1]
        card1Str = 'card{}{}.png'.format(suitToName[card1.suit._value_],
                                  card1.value)
        card2Str = 'card{}{}.png'.format(suitToName[card2.suit._value_],
                                  card2.value)
        formatted_player = { 'card1': card1Str, 'card2': card2Str }
        players_res.append(formatted_player)
    return players_res
