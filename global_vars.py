# -*- coding: utf-8 -*-

URL = 'https://www.goodreads.com/review/list/'
MY_ID = '4457811'
# A_ID = '8755368'
A_ID = '35473855'
SHELF_INSERT = '?shelf='

MY_SHELF_NAMES_JSON = 'shelf_names.json'
MY_SHELVES_JSON = 'shelves.json'
MY_BOOKS_JSON = 'books.json'

A_SHELF_NAMES_JSON = 'a_shelf_names.json'
A_SHELVES_JSON = 'a_shelves.json'
A_BOOKS_JSON = 'a_books.json'


TITLE = 'title'
AUTHOR = 'author'
NUM_PAGES = 'num_pages'
AVG_RATING = 'avg_rating'
NUM_RATINGS = 'num_ratings'
DATE_PUB = 'date_pub'
MY_RATING = 'rating'
DATE_STARTED = 'date_started'
DATE_READ = 'date_read'
DATE_ADDED = 'date_added'

SHELVES = 'shelves'

RUBRICS = [TITLE,
           AUTHOR,
           NUM_PAGES,
           AVG_RATING,
           NUM_RATINGS,
           DATE_PUB,
           MY_RATING,
           DATE_STARTED,
           DATE_READ,
           DATE_ADDED,
           SHELVES]

MISSING_DATUM = (None, 'not set', 'unknown')

TIME_DELTA = 'time_delta'
TIME_GAP = 'time_gap'
SPEED = 'speed'

READ = 'read'
CURRENTLY_READING = 'currently-reading'
TO_READ = 'to-read'

RATINGS = {"it was amazing": 5.0,
           "really liked it": 4.0,
           "liked it": 3.0,
           "it was ok": 2.0,
           "did not like it": 1.0}
