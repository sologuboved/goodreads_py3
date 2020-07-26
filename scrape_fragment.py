import requests
from bs4 import BeautifulSoup
from helpers import prettyprint_book
from global_vars import *


def find_vals(crazy_str):
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


def scrape_page_of_shelf(page_url):
    page_of_shelf = list()
    page_html = requests.get(page_url).content
    soup = BeautifulSoup(page_html, 'lxml')

    # We are looking for the contents of the tag tbody with the unique id booksBody
    tbody = soup('tbody', id='booksBody')

    # We are looking for the rows in the table representing books
    rows = tbody[0].find_all('tr')

    # We are appending the page_of_shelf list with dict comprising individual book
    for row in rows:
        page_of_shelf.append(scrape_book(row))

    return page_of_shelf


def scrape_book(row):
    cells = row.find_all('td')
    book = dict()
    for cell in cells:
        print(cell)
        print()
        print()
        class_entry = cell.get('class')[1]  # e.g. <td class="field title"> --> ['field', 'title'][1]
        if class_entry in RUBRICS[: -1]:  # except SHELVES
            if class_entry == DATE_STARTED or class_entry == DATE_READ:
                val_index = 4
            elif class_entry == MY_RATING:
                val_index = 2
            else:
                val_index = 1
            val = find_vals(str(cell))[val_index].strip()
            if val == '':
                val = MISSING_DATUM[0]
            book[class_entry] = val
    return book


if __name__ == '__main__':
    bs = scrape_page_of_shelf('https://www.goodreads.com/review/list/4457811-alyssa?shelf=euskal_herria')
    for b in bs:
        prettyprint_book(b, with_shelves=False)
