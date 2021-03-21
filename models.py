"""
This file defines the database models
"""
import datetime

from .common import db, Field
from pydal.validators import *

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#

def get_time():
    return datetime.datetime.utcnow()

db.define_table(
    'user',
    Field('user_id'),
    Field('running_score', "integer", default=0),
    Field('lives', "integer", default=3),
    Field('winners', 'list:integer'),
    Field('score_to_save', "integer", default=0, redifine=True),
    Field('is_solved', 'boolean', redifine=True),
    Field('is_end', 'boolean', default=False, redifine=True),
    Field('is_saved', 'boolean', default=False, redifine=True),
    Field('start_time', 'datetime', default=get_time, redifine=True),
    Field('best_hand_name', default="Pair", redefine=True),
    Field('end_time', 'datetime', default=get_time, redifine=True),
)

db.define_table(
    'leaderboard',
    Field('user_id'),
    Field('user_name', default="NO NAME"),
    Field('score', "integer", default=0),
    Field('lives', "integer", default=0),
    Field('start_time', 'datetime', default=get_time, redefine=True),
    Field('end_time', 'datetime', default=get_time, redefine=True)
)

db.commit()
