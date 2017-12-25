# -*- coding: utf-8 -*-

from goodreads0_scrape_shelves import Scraping
from goodreads1_collect_books import GoodreadsBooks
from global_vars import *

if __name__ == '__main__':
    Scraping(URL, MY_ID, SHELF_INSERT, MY_SHELVES_JSON).dump_shelves()
    GoodreadsBooks(MY_SHELVES_JSON, MY_BOOKS_JSON, MY_SHELF_NAMES_JSON, printer_on=False).dump_books_and_shelf_names()
    # Scraping(URL, A_ID, SHELF_INSERT, A_SHELVES_JSON).dump_shelves()
    # GoodreadsBooks(A_SHELVES_JSON, A_BOOKS_JSON, A_SHELF_NAMES_JSON).dump_books_and_shelf_names()
