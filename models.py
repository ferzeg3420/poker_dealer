"""
This file defines the database models
"""

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

db.define_table(
    'user',
    Field('user_id'),
    Field('running_score', "integer", default=0),
    Field('lives', "integer", default=3),
    Field('winners', 'list:integer'),
    Field('is_solved', 'boolean', redifine=True),
)

db.define_table(
    'leaderboard',
    Field('user_name', default="NO NAME"),
    Field('score', "integer", default=0),
    Field('lives', "integer", default=0),
    Field('time', "integer", default=0),
)

db.commit()
