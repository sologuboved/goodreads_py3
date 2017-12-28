# -*- coding: utf-8 -*-

import datetime
from goodreads2_librarian import Librarian
from basic_operations import *


class Stats(Librarian):

    def __init__(self, books_json, shelf_names_json):
        super(Stats, self).__init__(books_json, shelf_names_json)
        self.time_books()
        self.grouped = dict()
        self.filter_by_shelves()

    def time_books(self):
        for book in self.allotment:
            book[TIME_DELTA], book[TIME_GAP] = find_time(book)
            book[SPEED] = find_book_speed(book, rounded=True)

    def filter_by_range(self, *args):
        if not args:
            return
        for arg in args:
            rubric, start, finish = arg
            self.allotment = filter(lambda book: type(book[rubric]) is float, self.allotment)
            self.allotment = list(filter(lambda book: start <= book[rubric] <= finish, self.allotment))

    def filter_by_date(self, *args):
        if not args:
            return
        for arg in args:
            rubric, start, finish = arg
            self.allotment = filter(lambda book: type(book[rubric]) is datetime.date, self.allotment)
            self.allotment = list(filter(lambda book: start <= book[rubric].year <= finish, self.allotment))

    def filter_by_shelves(self, incl_and=(), incl_or=(), excl=(), by_shelf=False):
        assert type(incl_and) is tuple and type(incl_or) is tuple and type(excl) is tuple, "wrong type of argument"

        if by_shelf:

            if incl_and:
                self.grouped = {shelf: list() for shelf in incl_and}
                for book in self.allotment:
                    if set(incl_and).issubset(book[SHELVES]):
                        for shelf_name in incl_and:
                            self.grouped[shelf_name].append(book)
                return

            if incl_or:
                self.grouped = {shelf_name: list() for shelf_name in incl_or}
                for book in self.allotment:
                    for shelf_name in book[SHELVES]:
                        if shelf_name in incl_or:
                            self.grouped[shelf_name].append(book)
                return

            if excl:
                for book in self.allotment:
                    if not set(excl).intersection(set(book[SHELVES])):
                        for shelf_name in book[SHELVES]:
                            val = self.grouped.get(shelf_name, list())
                            val.append(book)
                            self.grouped[shelf_name] = val
                return

            self.grouped = {shelf_name: list() for shelf_name in self.shelf_names}
            for book in self.allotment:
                for shelf_name in book[SHELVES]:
                    self.grouped[shelf_name].append(book)
            return

        if incl_and:
            self.allotment = list(filter(lambda b: set(incl_and).issubset(b[SHELVES]), self.allotment))
        elif incl_or:
            self.allotment = list(filter(lambda b: set(incl_or).intersection(b[SHELVES]), self.allotment))
        elif excl:
            self.allotment = list(filter(lambda b: not set(excl).intersection(b[SHELVES]), self.allotment))

    def find_total_mean(self, rubric):
        total_mean = find_mean(self.allotment, rubric)
        print('\nMean:\n', total_mean)
        return total_mean

    def find_mean_per_shelf(self, rubric, alpha=False, large_to_small=True):
        assert self.grouped, "Shelved allotment is empty"
        means = {shelf_name: find_mean(self.grouped[shelf_name], rubric) for shelf_name in self.grouped}
        print('\nMean per shelf:\n')
        print_sorted_res(means, alpha, large_to_small)
        print()
        return means

    def find_est_books(self, rubric, large_to_small=True, num_books=5, by_shelf=False):
        print("\nBooks by %s:\n" % rubric)
        if by_shelf:
            assert self.grouped, "Shelved allotment is empty"
            for shelf_name in self.grouped:
                self.grouped[shelf_name] = list(filter(lambda book: type(book[rubric]) is float,
                                                       self.grouped[shelf_name]))
                sort_books(self.grouped[shelf_name], rubric, large_to_small)
            prettyprint_allotment(self.grouped, num_books, rubric)
        else:
            self.allotment = list(filter(lambda book: type(book[rubric]) is float, self.allotment))
            sort_books(self.allotment, rubric, large_to_small)
            prettyprint_allotment(self.allotment, num_books, rubric)

    def find_total_variance(self, rubric):
        total_variance = find_variance(self.allotment, rubric)
        print('\nVariance:\n', total_variance)
        return total_variance

    def find_variance_per_shelf(self, rubric, alpha=False, large_to_small=True):
        assert self.grouped, "Shelved allotment is empty"
        variances = {shelf_name: find_variance(self.grouped[shelf_name], rubric) for shelf_name in self.grouped}
        print('\nVariance per shelf:\n')
        print_sorted_res(variances, alpha, large_to_small)
        print()
        return variances

    def find_total_sd(self, rubric):
        total_sd = find_sd(self.allotment, rubric)
        print('\nStandard Deviation:\n', total_sd)
        return total_sd

    def find_sd_per_shelf(self, rubric, alpha=False, large_to_small=True):
        assert self.grouped, "Shelved allotment is empty"
        sds = {shelf_name: find_sd(self.grouped[shelf_name], rubric) for shelf_name in self.grouped}
        print("\nStandard Deviation per shelf:\n")
        print_sorted_res(sds, alpha, large_to_small)
        print()
        return sds


if __name__ == '__main__':
    pass
