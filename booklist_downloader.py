import requests
from bs4 import BeautifulSoup
from helpers import dump_utf_json, load_utf_json


def download_raw_booklist(url, num_pages, target_json):
    books = list()
    for page_num in range(1, num_pages + 1):
        for a in BeautifulSoup(requests.get(url.format(page_num)).content, 'lxml').find_all('td'):
            try:
                author_name = a.find('a', {'class': 'authorName'}).text.strip()
            except AttributeError:
                continue
            raw_title = a.find('a', {'class': 'bookTitle'})
            books.append([author_name, raw_title.text.strip(), raw_title.get('href').strip()])
    books.sort(key=lambda b: b[0].split()[-1])
    print("Dumping {} books...".format(len(books)))
    dump_utf_json(books, target_json)


def process_booklist(src_json, target_txt):
    with open(target_txt, 'wt') as handler:
        handler.write('<ol>')
        for author_name, title, title_url in load_utf_json(src_json):
            handler.write('<li><a href="{}">{} - {}</a></li>\n'.format('https://www.goodreads.com' + title_url,
                                                                       author_name, title))
        handler.write('</ol>')


if __name__ == '__main__':
    json_fname = 'raw_booklist.json'
    download_raw_booklist('https://www.goodreads.com/list/show/148119.Conspirologic?page={}', 2, json_fname)
    # process_booklist(json_fname, 'booklist.txt')
