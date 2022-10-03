
# URL for login into booking room
uoBookRoomUrl = 'https://bibliorooms.uottawa.ca/'

boundBoxPixelOffset = 40

'''
    text indicator which is actually the status of
    the current timeSlot it is used by setTextAdd()
    to set the correct text when visualising the result on the calendar image
    
    It is also a great way to tell the status of the timeslot on the console
'''

FIRST_HALF_INDICATOR = 'FIRST-HALF-FREE'
SECOND_HALF_INDICATOR = 'SECOND-HALF-FREE'
FULLY_RESERVABLE_INDICATOR = 'FREE'
FULLY_BOOK_INDICATOR = 'FULL'
CLOSED_INDICATOR = 'CLOSE'

FIRST_HALF_FULL_SECOND_HALF_CLOSE_INDICATOR = 'FIRST_HALF_FULL_SECOND_HALF_CLOSE'
FIRST_HALF_FREE_SECOND_HALF_CLOSE_INDICATOR = 'FIRST_HALF_FREE_SECOND_HALF_CLOSE'

FIRST_HALF_CLOSE_SECOND_HALF_FULL_INDICATOR = 'FIRST_HALF_FREE_SECOND_HALF_FULL'
FIRST_HALF_CLOSE_SECOND_HALF_FREE_INDICATOR = 'FIRST_HALF_CLOSE_SECOND_HALF_FREE'

'''
    Text indicator used in when adding text 
    to the availability img
'''

TEXT_FREE = 'FREE'
TEXT_FULL = 'FULL'
TEXT_FIRST_HALF = 'Ffree'
TEXT_SECOND_HALF = 'Sfree'
TEXT_CLOSE = 'CLOS'
TEXT_FIRST_HALF_FREE_SECOND_HALF_CLOSE = 'Ff SC'
TEXT_FIRST_HALF_FULL_SECOND_HALF_CLOSE = 'FF SC'
TEXT_FIRST_HALF_CLOSE_SECOND_HALF_FREE = 'FC Sf'
TEXT_FIRST_HALF_CLOSE_SECOND_HALF_FULL = 'FC SF'
TEXT_UNDEFINED = 'UND'

'''
    Portion divisor used when portioning the image 
    when searching by area
'''


PORTION_HEIGHT_DIVISOR = 2
PORTION_WIDTH_DIVISOR = 2

'''
    Corrector used when initial portioning did not find the date
    It will get added to the initial potion divisor
    
    For ex:
     PORTION_HEIGHT_DIVISOR += PORTION_HEIGHT_CORRECTOR = 2
'''

PORTION_HEIGHT_CORRECTOR = 2
PORTION_WIDTH_CORRECTOR = 2

'''
    Number of maximum narrow search loop iterations to find the
    date in the calendar image
    
    In combination to the portion divisor and the portion corrector
    it will reduce the size of the area searched by the algorithm
'''

NARROW_SEARCH_MAX_ITERATION = 3

'''
    constants rgb values representing the color 
    of the portion of the image representing by closed indicator
    
    It is a range because the actual value is not always the same since
    the image portioning is random 
'''

CLOSE_IMAGE_RED_MAX_VALUE = 220
CLOSE_IMAGE_RED_MIN_VALUE = 120

CLOSE_IMAGE_GREEN_MAX_VALUE = 200
CLOSE_IMAGE_GREEN_MIN_VALUE = 110

CLOSE_IMAGE_BLUE_MAX_VALUE = 200
CLOSE_IMAGE_BLUE_MIN_VALUE = 110