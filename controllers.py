"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""
import datetime
from datetime import timedelta
import math
import re

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from . models import get_time

from .services.dealer_game.game_service import game_service

# constants

A_code = ord('A')
Z_code = ord('Z')
a_code = ord('a')
z_code = ord('z')
zero_code = ord('0')
nine_code = ord('9')
space_code = ord(' ')
MAX_NAME_SIZE = 50
MAX_PLAYERS = 9

MAX_CASH = 100
BONUS_PER_LIFE = 700000
POINTS_PER_CASH = 7000
MAX_BONUS_FOR_TIME = 7200000

bonus_points_from_lives = 0
bonus_points_from_time = 0
two_hours_timedelta = timedelta(hours=2)

def is_guess_valid(guess):
    if not isinstance(guess, list):
        return False
    if len(guess) > MAX_PLAYERS:
        return False
    return True

def is_character_or_space(char_code):
    return (char_code >= A_code and char_code <= Z_code) \
           or (char_code >= a_code and char_code <= z_code) \
           or (char_code >= zero_code and char_Code <= nine_code) \
           or (char_code == space_code)

def sanitize_words(name):
    clean_words = []
    words = name.split(' ')
    for w in words:
        w_lower = w.lower()
        if w_lower == "table" \
           or w_lower == "drop" \
           or w_lower == "delete" \
           or w_lower == "from" \
           or w_lower == "select":
            continue
        clean_words.append(w)
    return ' '.join(clean_words)

def sanitize_characters(name):
    cleaned_name = []
    cleaned_counter = 0
    for c in name:
        char_code = ord(c)
        if is_character_or_space(char_code):
            cleaned_name.append(c)
            cleaned_counter += 1
        if cleaned_counter > MAX_NAME_SIZE:
            break
    return ''.join(cleaned_name)

def sanitize_leaderboard_name(name):
    clean_chars = sanitize_characters(name)
    clean_words = sanitize_words(clean_chars)
    if len(clean_words) == 0:
       return "NO NAME"
    else:
       return clean_words


def calculate_points(lives, cash, game_duration):
    # add bonus points if cash is max
    points_from_cash = cash * POINTS_PER_CASH
    if cash == MAX_CASH:
        bonus_points_from_lives = lives * BONUS_PER_LIFE
        if game_duration < two_hours:
            miliseconds_game_duration = \
                math.floor(game_duration.total_seconds() * 1000)
            bonus_points_from_time = \
                MAX_BONUS_FOR_TIME - miliseconds_game_duration

    return bonus_points_from_lives + \
           bonus_points_from_time +  \
           points_from_cash 
    

@action('index')
@action.uses('index.html', session, db)
def index():
    db.user.update_or_insert(
        db.user.user_id == session['uuid'],
        user_id=session['uuid'],
    )
    return dict(
        post_guess_url=URL('check_guess'),
        get_cards_url=URL('deal_cards'),
        get_init_game_state_url=URL('get_init_game_state'),
        score_to_leaderboard_url=URL('score_to_leaderboard'),
        get_game_time_url=URL('get_game_time')
    )

@action('leaderboard')
@action.uses('leaderboard.html', session, db)
def leaderboard():
    leaderboard = []
    rows = db(db.leaderboard).select(
        db.leaderboard.ALL,
        orderby=db.leaderboard.score,
    ).as_list()
    j = 0
    for i in rows:
        j += 1
        leaderboard.append(
            {
                'place': j,
                'name': i.get('user_name'),
                'score': i.get('score'),
                'time': str(i.get('end_time') - i.get('start_time')),
            }
        )
    return dict(leaderboard=leaderboard)

@action('deal_cards')
@action.uses(session, db)
def deal():
    rows = db(db.user.user_id == session['uuid']).select()
    current_score = rows.first().running_score
    if current_score is None:
        return #error current score is none. Everything should break now!
    res = game_service(current_score)
    start_time = rows.first().start_time

    if( rows.first().lives == 3 \
        and rows.first().running_score == 0 ):
        start_time = get_time()

    winners = res.get('winners')
    board = res.get('board')
    players = res.get('players')
    best_hand = res.get('best_hand')

    db.user.update_or_insert(
        db.user.user_id == session['uuid'],
        user_id=session['uuid'],
        winners=winners,
        is_solved=False,
        is_saved=False,
        best_hand_name=best_hand,
        start_time=start_time,
    )
              
    return dict(
       board = board,
       players = players,
    )
  
@action('check_guess', method="POST")
@action.uses(session, db)
def check():
    rows = db(db.user.user_id == session['uuid']).select()

    if rows.first().is_solved:
        return #error already been guessed no new cards were loaded

    right_answer = rows.first().winners
    lives = rows.first().lives
    ret_lives = lives
    score = rows.first().running_score
    ret_score = score

    guess = request.json.get('guess')
    if not is_guess_valid(guess):
        guess = []

    is_end = False
    end_time = rows.first().end_time

    if len(right_answer) != len(guess) \
       or sorted(right_answer) != sorted(guess):
        lives -= 1
        ret_lives -= 1
        if lives < 1:
            is_end = True
            lives  = 3
            score  = 0
    else:
        score += 5
        ret_score += 5

    if score >= 100:
        score = 0
        is_end = True 

    if is_end:
        end_time = get_time()

    best_hand = rows.first().best_hand_name
    db.user.update_or_insert(
        db.user.user_id == session['uuid'],
        user_id=session['uuid'],
        running_score=score,
        score_to_save=ret_score,
        lives=lives,
        winners=[],
        is_solved=True,
        is_saved=False,
        is_end=is_end,
        end_time=end_time,
    )

    return dict(
        right_answer=right_answer,
        lives = ret_lives,
        score = ret_score,
        is_end = is_end, 
        best_hand = best_hand
    )

@action('get_init_game_state')
@action.uses(session, db)
def get_init():
    rows = db(db.user.user_id == session['uuid']).select()
              
    return dict(
        lives = rows.first().lives,
        running_score = rows.first().running_score
    )

@action('score_to_leaderboard', method="POST")
@action.uses(session, db)
def score_to_lead():
    user_rows = db(db.user.user_id == session['uuid']).select()
    leaderboard_rows = db(db.leaderboard).select()

    name = request.json.get('name')
    cleaned_name = sanitize_leaderboard_name(name)

    if not user_rows.first().is_end:
        return # error user not finished

    if user_rows.first().is_saved:
        return #error score has already been saved

    t1 = user_rows.first().start_time
    t2 = user_rows.first().end_time
    ret_time = str(t2 - t1)
    #TODO: calculate time
    #TODO: validate the name of the user
    db.user.update_or_insert(
        db.user.user_id == session['uuid'],
        is_saved=True,
    )
    
    db.leaderboard.update_or_insert(
        user_id=session['uuid'],
        user_name=cleaned_name,
        score=calculate_points(user_rows.first().lives,
                               user_rows.first().score_to_save,
                               ret_time,
                             ),
        lives=user_rows.first().lives,
        start_time=t1,
        end_time=t2
    )
    return dict(time=ret_time)
  
@action('get_game_time')
@action.uses(session, db)
def get_game_time():
    user_rows = db(db.user.user_id == session['uuid']).select()

    if not user_rows.first().is_end:
        return #error user hasn't finished.

    if user_rows.first().is_saved:
        return #error time has been saved already

    t1 = user_rows.first().start_time
    t2 = user_rows.first().end_time
    ret_time = str(t2 - t1)
    return dict(time=ret_time)
    
# players = [ all_players[i] for i in range(0, num_players) ]
# deck.deal_player_hands(players)
