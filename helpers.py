# -*- coding: utf-8 -*-

import json
from math import floor, sqrt
from global_vars import *


def load_utf_json(json_file):
    with open(json_file, encoding='utf8') as data:
        return json.load(data)


def dump_utf_json(entries, json_file):
    with open(json_file, 'w', encoding='utf-8') as handler:
        json.dump(entries, handler, ensure_ascii=False, sort_keys=True, indent=2)


def print_scraped_rubrics(cells):
    print(cells)


def prettyprint_allotment(allotment, num_books=None, only_meaningful=False):
    if type(allotment) is dict:
        prettyprint_grouped_allotment(allotment, num_books, only_meaningful)
    elif type(allotment) is list:
        prettyprint_ungrouped_allotment(allotment, num_books, only_meaningful)
    else:
        "Wrong type of allotment, prettyprinter is broken"


def prettyprint_grouped_allotment(grouped_allotment, num_books=None, only_meaningful=False):
    for key in grouped_allotment:
        print(" ---------", key, '---------')
        print()
        prettyprint_ungrouped_allotment(grouped_allotment[key], num_books, only_meaningful)
        print()


def prettyprint_ungrouped_allotment(allotment, num_books=None, only_meaningful=False):
    if not num_books:
        num_books = len(allotment)

    if only_meaningful:
        index = 1
        for book in allotment:
            if type(book[only_meaningful]) == float and index <= num_books:
                print(index)
                index += 1
                prettyprint_book(book)
                print()
    else:
        index = 1
        for entry in allotment[: num_books]:
            print(index)
            index += 1
            prettyprint_book(entry)
            print()


def prettyprint_book(book, with_shelves=True):
    for rubric in RUBRICS[: -1]:
        print(rubric + ':', book[rubric])

    try:

        time_delta = book[TIME_DELTA]
        if time_delta not in MISSING_DATUM:
            time_delta = str(int(time_delta)) + " day(s)"
        print(TIME_DELTA + ':', time_delta)

        time_gap = book[TIME_GAP]
        if time_gap not in MISSING_DATUM:
            time_gap = str(int(time_gap)) + " day(s)"
        print(TIME_GAP + ':', time_gap)

        speed = book[SPEED]
        if speed not in MISSING_DATUM:
            speed = str(speed) + " pages per day"
        print(SPEED + ':', speed)

    except KeyError:
        pass

    if with_shelves:
        print('shelves:')
        for shelf_name in book[SHELVES]:
            print("         ", shelf_name)
        print()


def deep_copy(multi):
    if type(multi) == dict:
        dict_copy = dict()
        for key in multi:
            dict_copy[key] = deep_copy(multi[key])
        return dict_copy

    elif type(multi) == list:
        list_copy = list()
        for item in multi:
            list_copy.append(deep_copy(item))
        return list_copy

    else:
        return multi


def update_book_shelves(json_file, title, upd_shelves):
    # Change the contents of shelves rubric in the json file
    assert type(upd_shelves) is list, "upd_shelves must be of type list"
    library = load_utf_json(json_file)
    print("Loaded allotment")
    for book in library:
        if book[TITLE] == title:
            book[SHELVES] = upd_shelves[:]
            dump_utf_json(library, json_file)
            print("Dumped updated allotment")
            return
    print(title, 'not found!')


def find_time(book):
    started, read, added = book[DATE_STARTED], book[DATE_READ], book[DATE_ADDED]
    delta, gap = None, None
    if started:
        if read:
            delta = float((read - started).days)
            if not delta:
                delta = 1.0
        if added:
            gap = float((started - added).days)
            if not gap:
                gap = 1.0
    return delta, gap


def find_book_speed(book, rounded=False):
    # pages per day
    try:
        if rounded:
            return float(floor(book[NUM_PAGES] / book[TIME_DELTA]))
        return book[NUM_PAGES] / book[TIME_DELTA]
    except TypeError:
        return


def find_suitable_vals(allotment, rubric):
    for book in allotment:
        val = book[rubric]
        if type(val) is float:
            yield val


def find_mean(allotment, rubric):
    suitable_vals = list(find_suitable_vals(allotment, rubric))
    if suitable_vals:
        return sum(suitable_vals) / len(suitable_vals)


def sort_books(allotment, rubric, large_to_small):
    allotment.sort(key=lambda book: book[rubric], reverse=large_to_small)


def print_sorted_res(results, alpha=False, large_to_small=True):
    nones = list()
    clean = list()
    for shelf_name in results:
        value = results[shelf_name]
        result = (shelf_name, value)
        if value is None:
            nones.append(result)
        else:
            clean.append(result)
    if alpha:
        ind = 0
    else:
        ind = 1
    sorted_results = sorted(clean, key=lambda b: b[ind], reverse=large_to_small)
    sorted_results += sorted(nones, key=lambda s: s[0], reverse=large_to_small)
    for result in sorted_results:
        print(result[0], end=' ')
        print(':', result[1])


def find_variance(allotment, rubric):
    suitable_vals = list(find_suitable_vals(allotment, rubric))
    if suitable_vals:
        mean = sum(suitable_vals) / len(suitable_vals)
        return sum([(suitable_val - mean) ** 2 for suitable_val in suitable_vals]) / len(suitable_vals)


def find_sd(allotment, rubric):
    try:
        return sqrt(find_variance(allotment, rubric))
    except TypeError:
        return
