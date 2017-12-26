# -*- coding: utf-8 -*-

import html
import requests
from bs4 import BeautifulSoup
from basic_operations import *


class Scraping(object):

    def __init__(self, url, user_id, shelf_insert, shelves_json):
        self.url = url
        self.user_id = user_id
        self.shelf_insert = shelf_insert
        self.shelves_json = shelves_json
        self.shelves = self.comprise_all_shelves()

    @staticmethod
    def find_vals(crazy_str):
        """
        Extract useful data, e.g. title "I Am a Strange Loop", from cell, thus emulating RE which I don't rememer
        """
        raw_vals = list()
        vals = list()
        length = len(crazy_str)

        for index in range(length):
            char = crazy_str[index]

            if char == '>':
                val = ''
                next_index = index + 1

                while next_index < length:
                    next_char = crazy_str[next_index]
                    next_index += 1
                    if next_char != '<':
                        val += next_char
                    else:
                        break

                raw_vals.append(val)

        for val in raw_vals:
            if len(val) > 0:
                for char in val:
                    if char != ' ':
                        vals.append(val)
                        break

        return vals

    def generate_shelf_url(self, shelf_name):
        return self.url + self.user_id + self.shelf_insert + shelf_name

    def comprise_all_shelves(self):
        """
        Compile dict with name of shelves as keys and lists of dicts (individual books on each given shelf) as values
        :return: dict (of lists of dicts)
        """
        shelves = dict()
        shelf_names = self.collect_shelf_names()
        num_shelves = len(shelf_names)
        index = 1
        for shelf_name in shelf_names:
            print("(% r of %r)" % (index, num_shelves), "Starting shelf", '"' + shelf_name + '":', end=' ')
            index += 1
            shelf_url = self.generate_shelf_url(shelf_name)
            shelves[shelf_name] = self.scrape_shelf(shelf_url)
        return shelves

    def collect_shelf_names(self):
        """
        Collect names of shelves
        :return: list (of strs)
        """
        shelf_names = [READ, CURRENTLY_READING, TO_READ]

        initial_url = self.url + self.user_id
        page_html = requests.get(initial_url).content
        soup = BeautifulSoup(page_html, 'lxml')

        raw_shelf_names = soup('div', id='paginatedShelfList')[0].find_all('div', class_="userShelf")

        shelf_names += [raw_shelf_name.find_all('a')[0].text.split()[0] for raw_shelf_name in raw_shelf_names[3:]]

        return shelf_names

    def scrape_shelf(self, first_page_url):
        """
        Scrape shelf, and present it as list of dicts (individual books) on this shelf
        To this end, iterate over all pages of shelf and put together resulting lists
        :param first_page_url: str
        :return: list (of dicts)
        """
        shelf = list()
        page_num = 1
        while True:
            page_url = first_page_url + '&page=' + str(page_num)
            page_of_shelf = self.scrape_page_of_shelf(page_url)
            if not page_of_shelf:
                # prettyprint_list_of_dicts(shelf)
                print(len(shelf), 'books')
                return shelf
            shelf.extend(page_of_shelf)
            page_num += 1

    def scrape_page_of_shelf(self, page_url):
        """
        Scrape page of shelf, and put it together as list of dictionaries (individual books) on this page
        Table is contained in 'tbody' tag; it contains all books' info on page.
        Rows contain individual books: one row - one book.
        Cells contain book properties (e.g. title, author, num pages): one cell - one property.
        :param page_url: str
        :return: list (of dicts)
        """
        page_of_shelf = list()
        page_html = requests.get(page_url).content
        soup = BeautifulSoup(page_html, 'lxml')

        # We are looking for the contents of the tag tbody with the unique id booksBody
        tbody = soup('tbody', id='booksBody')

        # We are looking for the rows in the table representing books
        rows = tbody[0].find_all('tr')

        # We are appending the page_of_shelf list with dict comprising individual book
        for row in rows:
            page_of_shelf.append(self.scrape_book(row))

        return page_of_shelf

    def scrape_book(self, row):
        """
        Scrape individual book and return it as dict with rubrics such as 'author' as keys
        :param row: bs4.element.Tag
        :return: dict
        """
        cells = row.find_all('td')
        book = dict()
        for cell in cells:
            class_entry = cell.get('class')[1]  # e.g. <td class="field title"> --> ['field', 'title'][1]
            if class_entry in RUBRICS[: -1]:  # except SHELVES
                if class_entry == DATE_STARTED or class_entry == DATE_READ:
                    val_index = 4
                elif class_entry == MY_RATING:
                    val_index = 2
                else:
                    val_index = 1
                val = self.find_vals(str(cell))[val_index].strip()
                if val == '':
                    val = MISSING_DATUM[0]
                try:
                    book[class_entry] = html.unescape(val)
                except TypeError:
                    book[class_entry] = val
        book[SHELVES] = list()
        return book

    def dump_shelves(self):
        print("Dumping shelves...")
        dump_json(self.shelves, self.shelves_json)


if __name__ == '__main__':
    # Scraping(URL, MY_ID, SHELF_INSERT, MY_SHELVES_JSON)
    # Scraping(URL, A_ID, SHELF_INSERT, A_SHELVES_JSON)
    Scraping(URL, MY_ID, SHELF_INSERT, MY_SHELVES_JSON).dump_shelves()
    # Scraping(URL, A_ID, SHELF_INSERT, A_SHELVES_JSON).dump_shelves()
