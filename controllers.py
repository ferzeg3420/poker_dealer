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

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash

# Not part of _scaffold
from .services.dealer_game.game_service import game_service

#@unauthenticated("index", "index.html")
#def index():
#    user = auth.get_user()
#    message = T("Hello {first_name}".format(**user) if user else "Hello")
#    return dict(message=message)

@action('index')
@action.uses('index.html', session, db)
def index():
#   print("session type:", type(session))
#   print("session :", vars(session))
#   print("uuid type:", type(session['uuid']))
    db.user.update_or_insert(
        db.user.user_id == session['uuid'],
        user_id=session['uuid'],
    )
    return dict(
        post_guess_url=URL('check_guess'),
        get_cards_url=URL('deal_cards'),
        get_init_game_state_url=URL('get_init_game_state')
    )

@action('leaderboard')
@action.uses('leaderboard.html', session, db)
def leaderboard():
    leaderboard = []
    rows = db(db.leaderboard).select(
        db.leaderboard.ALL,
        orderby=db.leaderboard.score|~db.leaderboard.time,
        limitby=(0, 10)
    )
    print(rows)
    for i in range(1, 11):
        leaderboard.append(
            {'place': i,
             'name': "Fernando",
             'score': "100",
             'time': "20"
             })
    return dict(leaderboard = leaderboard)

@action('deal_cards')
@action.uses(session, db)
def deal():
#    print("session type:", type(session))
#    print("session :", vars(session))
    rows = db(db.user.user_id == session['uuid']).select()
    print("deal_cards: rows:", rows)
    print("deal_cards: rows.first():", rows.first())
    current_score = rows.first().running_score
    if current_score is None:
      print("current score is none. Everything should break now!") 
    res = game_service(current_score)

    winners = res.get('winners')

    board = res.get('board')

    players = res.get('players')

    db.user.update_or_insert(
        db.user.user_id == session['uuid'],
        user_id=session['uuid'],
        winners=winners,
        is_solved=False,
    )
              
    return dict(
       board = board,
       players = players,
    )
  
@action('check_guess', method="POST")
@action.uses(session, db)
def check():
    rows = db(db.user.user_id == session['uuid']).select()
    print( "check_guess: rows:", rows)
    print( "check_guess: rows.first():", rows.first())
    if rows.first().is_solved:
      return
    right_answer = rows.first().winners
    lives = rows.first().lives
    ret_lives = lives
    score = rows.first().running_score
    ret_score = score
    guess = request.json.get('guess')
    is_end = False

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

    #if is end, save ret score in leaderboard

    db.user.update_or_insert(
        db.user.user_id == session['uuid'],
        user_id=session['uuid'],
        running_score=score,
        lives=lives,
        winners=[],
        is_solved=True,
    )

    return dict(
        right_answer = right_answer,
        lives = ret_lives,
        score = ret_score,
        is_end = is_end 
    )

@action('get_init_game_state')
@action.uses(session, db)
def get_init():
    rows = db(db.user.user_id == session['uuid']).select()
              
    return dict(
        lives = rows.first().lives,
        running_score = rows.first().running_score
    )

# players = [ all_players[i] for i in range(0, num_players) ]
# deck.deal_player_hands(players)
