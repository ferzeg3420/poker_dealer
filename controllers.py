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

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from . models import get_time

# Not part of _scaffold
from .services.dealer_game.game_service import game_service

#@unauthenticated("index", "index.html")
#def index():
#    user = auth.get_user()
#    message = T("Hello {first_name}".format(**user) if user else "Hello")
#    return dict(message=message)

def calculate_points(lives, cash, game_duration):
    MAX_CASH = 100
    BONUS_PER_LIFE = 700000
    POINTS_PER_CASH = 7000
    MAX_BONUS_FOR_TIME = 7200000
    
    bonus_points_from_lives = 0
    bonus_points_from_time = 0
    points_from_cash = cash * POINTS_PER_CASH
    two_hours_timedelta = timedelta(hours=2)

    # add bonus points if cash is max
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
        print("current score is none. Everything should break now!") 
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
      return #error
    right_answer = rows.first().winners
    lives = rows.first().lives
    ret_lives = lives
    score = rows.first().running_score
    ret_score = score
    guess = request.json.get('guess')
    is_end = False
    end_time = rows.first().end_time

    print("right answer:", right_answer)
    print("right answer type:", type(right_answer))
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

    if not user_rows.first().is_end:
        return #error

    if user_rows.first().is_saved:
        return #error

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
        user_name=name,
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
        return #error

    if user_rows.first().is_saved:
        return #error

    t1 = user_rows.first().start_time
    t2 = user_rows.first().end_time
    ret_time = str(t2 - t1)
    return dict(time=ret_time)
    
# players = [ all_players[i] for i in range(0, num_players) ]
# deck.deal_player_hands(players)
