# -*- coding: utf-8 -*-

import datetime
from basic_operations import *


class Librarian(object):
    def __init__(self, books_json, shelf_names_json):
        self.errors = set()  # from self.process_books
        self.allotment = self.process_books(load_json(books_json))
        self.shelf_names = load_json(shelf_names_json)
        print("Errors:")
        if self.errors:
            for error in self.errors:
                print(error)
        else:
            print(None)
        print()
        print()

    @staticmethod
    def convert_to_float(raw_num):
        """
        Convert a number from str to float, omitting commas; if n/a, to missing data marker
        :param raw_num: str
        :return: float or str
        """
        if raw_num in MISSING_DATUM:
            return MISSING_DATUM[0]
        num = ''
        for char in raw_num:
            if char != ',':
                num += char
        return float(num)

    @staticmethod
    def convert_rating(raw_rating):
        """
        Convert rating from str to float; if n/a, to missing data marker
        :param raw_rating: str
        :return: float or str
        """
        return RATINGS.get(raw_rating, MISSING_DATUM[0])

    @staticmethod
    def convert_date(raw_date):
        """
        Convert date from str to datetime format; if n/a, to missing data marker
        :param raw_date: unicode
        :return: datetime.date
        """
        if raw_date in MISSING_DATUM:
            return MISSING_DATUM[0]
        splitted_date = raw_date.split()
        length = len(splitted_date)
        if length == 3:
            return datetime.datetime.strptime(raw_date, '%b %d, %Y').date()
        elif length == 2:
            return datetime.datetime.strptime(' '.join((splitted_date[0], '01,', splitted_date[1])), '%b %d, %Y').date()
        else:
            return datetime.date(int(raw_date), 1, 1)

    def find_book(self, title):
        """
        Find and prettyprint book of the given title
        :param title: str
        :return: None
        """
        for book in self.allotment:
            if book[TITLE] == title:
                prettyprint_book(book)
                break
        else:
            print(title, "not found!")

    def process_val(self, func, val):
        """
        Process value val with the help of function func and catch & record errors
        """
        try:
            return func(val)
        except (ValueError, KeyError):
            self.errors.add(val)
            return val

    def collect_shelf(self, shelf_name, printer_on=False):
        """
        Return shelf of given name by browsing through all books and compiling list of those that are on that shelf
        :param shelf_name: str
        :param printer_on: Boolean
        :return: list (of dicts)
        """
        try:
            shelf = [book for book in self.allotment if shelf_name in book[SHELVES]]
        except KeyError as e:
            print('Book', '"' + book[TITLE] + '"', "doesn't have key", e)
            return
        if printer_on:
            prettyprint_allotment(shelf)
        return shelf

    def process_books(self, books):
        """
        Process all books: change datatypes where necessary
        :param books: list(of dicts)
        :return: list (of dicts)
        """
        for book in books:

            for rubric in (NUM_PAGES, NUM_RATINGS, AVG_RATING):
                book[rubric] = self.process_val(self.convert_to_float, book[rubric])

            for rubric in (DATE_PUB, DATE_ADDED, DATE_STARTED, DATE_READ):
                book[rubric] = self.process_val(self.convert_date, book[rubric])

            book[MY_RATING] = self.process_val(self.convert_rating, book[MY_RATING])

        return books

    def find_unshelved_books(self):
        """
        Print out books that are not placed at any shelf except READ, CURRENTLY_READING, or TO_READ
        :return: None
        """
        unshelved = [book for book in self.allotment if len(book[SHELVES]) == 1]
        if unshelved:
            prettyprint_allotment(unshelved)
        else:
            print("All books shelved")


if __name__ == '__main__':
    # title = u"The Wise King: A Christian Prince, Muslim Spain, and the Birth of the Renaissance"
    good_librarian = Librarian(MY_BOOKS_JSON, MY_SHELF_NAMES_JSON)
    # good_librarian.find_book(title)
    # print len(good_librarian.allotment)
    # print load_json(MY_BOOKS_JSON)[19]
    # good_librarian = Librarian(A_BOOKS_JSON, A_SHELF_NAMES_JSON)
    # print len(good_librarian.allotment)
    # print load_json(A_BOOKS_JSON)[19]
    good_librarian.find_unshelved_books()
