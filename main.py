
from BookBot import *
from LoginBot import *
from TextBot import *

if __name__ == '__main__':

    bot = LoginBot()

    bookBot = BookBot()

    textBot = TextBot()

    textBot.analyze()