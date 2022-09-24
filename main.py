
from BookBot import *
from LoginBot import *
from TextBot import *

if __name__ == '__main__':

    filepath = 'screencapture/testBooking2.png'

    bot = LoginBot()

    bookBot = BookBot()

    textBot = TextBot()

    textBot.analyze(filepath)

    # bookBot.login()