# -*- coding: utf-8 -*-

from basic_operations import *


class GoodreadsBooks(object):
    def __init__(self, shelves_json, books_json, shelf_names_json, printer_on=True):
        self.shelves_json = shelves_json
        self.books_json = books_json
        self.shelf_names_json = shelf_names_json
        self.printer_on = printer_on
        self.shelves = load_json(self.shelves_json)
        self.shelf_names = sorted(self.shelves.keys())
        self.books = self.collect_books()

    def collect_books(self):
        """
        Produce all-encompassing list of books
        Initialize a dict of books; each key if to be a combination of author and title
        Through iteration over shelves (lists) and books on each shelf (dicts), either create new entry in this dict or
        append rubric 'shelves' (if the entry already exists)
        Turn this dict into a list
        :return: list (of dicts)
        """
        print("Collecting books...")
        books = dict()
        for shelf in self.shelves:
            if self.printer_on:
                print()
                print('*-*-*-*-*-*-*-*-*-*')
                print('Loading', shelf)
                print()
            for raw_book in self.shelves[shelf]:
                book = {rubric: raw_book[rubric] for rubric in raw_book}
                rating = book[MY_RATING]
                book[MY_RATING] = RATINGS.get(rating, MISSING_DATUM[0])
                book_key = book[AUTHOR] + ' -- ' + book[TITLE]
                if self.printer_on:
                    print(book_key, end=' ')
                readymade_entry = books.get(book_key)
                if readymade_entry:
                    readymade_entry[SHELVES].append(shelf)
                    if self.printer_on:
                        print("is in the library")
                        print(books[book_key][SHELVES])
                else:
                    book[SHELVES] = [shelf]
                    books[book_key] = book
                    if self.printer_on:
                        print('added')
                if self.printer_on:
                    print()
                    print()
                # prettyprint_book(book, with_shelves=False)
                # print()
        books = list(books.values())
        return books

    def dump_books_and_shelf_names(self):
        dump_json(self.books, self.books_json)
        dump_json(self.shelf_names, self.shelf_names_json)


if __name__ == '__main__':
    pass
    # GoodreadsBooks(MY_SHELVES_JSON, MY_BOOKS_JSON, MY_SHELF_NAMES_JSON, printer_on=True)
    # books = GoodreadsBooks(MY_SHELVES_JSON, MY_BOOKS_JSON, MY_SHELF_NAMES_JSON, printer_on=False).books
    GoodreadsBooks(MY_SHELVES_JSON, MY_BOOKS_JSON, MY_SHELF_NAMES_JSON, printer_on=False).dump_books_and_shelf_names()
    # GoodreadsBooks(A_SHELVES_JSON, A_BOOKS_JSON, A_SHELF_NAMES_JSON).dump_books_and_shelf_names()
