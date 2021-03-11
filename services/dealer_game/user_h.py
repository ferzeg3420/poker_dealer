from .util import *

class User:
    def __init__(self, score, lives):
        self.score = score
        self.lives = lives
        self.name = "User"

    def __repr__(self):
        score = self.score
        hearts = lives_2_hearts(self.lives)
        lives = self.lives
        name = self.name
        if self.lives == 0:
            user_string = name               \
                          + "\t"             \
                          + hearts           \
                          + " Tilted"        \
                          + "\tCash: $"      \
                          + str(score)       \
                          + "\n\n"
        else:
            user_string = name               \
                          + "\t"             \
                          + hearts           \
                          + "\t\tCash: $"    \
                          + str(score)       \
                          + "\n\n"         
        return user_string
