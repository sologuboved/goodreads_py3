from basic_operations import load_json
from global_vars import TITLE, SHELVES
from basic_operations import prettyprint_allotment


def compare(old_json, new_json):
    old = load_json(old_json)
    new = load_json(new_json)
    common_titles = list()
    pairs = list()
    for old_book in old:
        for new_book in new:
            title = old_book[TITLE]
            if new_book[TITLE] == title:
                common_titles.append(title)
                pairs.append((old_book, new_book))

    odd_old = find_odd_books(old, common_titles)
    odd_new = find_odd_books(new, common_titles)

    return pairs, odd_old, odd_new


def find_odd_books(books, common_titles):
    return [book for book in books if book[TITLE] not in common_titles]


def process_pairs(pairs):
    ind = 0
    for pair in pairs:
        old_book, new_book = pair
        if old_book == new_book:
            continue
        for rubric in old_book:
            old_rub = old_book[rubric]
            new_rub = new_book[rubric]
            if rubric == SHELVES:
                if not (set(old_rub) ^ set(new_rub)):
                    continue
            else:
                if old_rub == new_rub:
                    continue
            print()
            print(ind)
            print(old_book[TITLE])
            print(rubric + ':')
            print('old:', old_rub)
            print('new:', new_rub)
        ind += 1
        ind += 1
        print()


if __name__ == '__main__':
    pass
    # pairs_res, odd_old_res, odd_new_res = compare('old_books.json', 'books.json')
    # print(process_pairs(pairs_res))
    # prettyprint_allotment(odd_old_res)
    # prettyprint_allotment(odd_new_res)

