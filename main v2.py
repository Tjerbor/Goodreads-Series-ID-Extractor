"""
Usage:
    remix.audio_dl.py
    remix.audio_dl.py <URL>
    remix.audio_dl.py -h | --help
    remix.audio_dl.py --version
Options:
    No argument                     Will use the clipboard string as URL.

    -h --help                       Show this screen.
    --version                       Show version.
"""
import logging
import sys
from urllib.request import urlopen

import pyperclip
from bs4 import BeautifulSoup
from docopt import docopt

__version__ = '0.0.1'
ARGUMENTS: dict


def main():
    global ARGUMENTS
    global __version__
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='INFO: %(message)s')
    ARGUMENTS = docopt(__doc__, version=__version__)
    if ARGUMENTS['<URL>'] is not None:
        url = ARGUMENTS['<URL>']
    else:
        url = pyperclip.paste()

    book_ids = get_book_ids(url)
    formatted_ids = list(map(lambda book_id: f'goodreads:{book_id}', book_ids))

    clipboard_string = '\n'.join(formatted_ids)
    pyperclip.copy(clipboard_string)
    print(clipboard_string)


def get_book_ids(url: str) -> list:
    try:
        source = urlopen(url)
        soup = BeautifulSoup(source, 'html.parser')
        books = soup.find_all('div', {'class': 'listWithDividers__item'})
        book_ids = list(
            map(lambda item: item.find('a', {'data-reactid': True})['href'].removeprefix('/book/show/'), books))
        logging.info(f'Book IDs: [{', '.join(book_ids)}]')
    except Exception as e:
        print(f'Invalid URL: {url}')
        sys.exit(1)

    return book_ids


if __name__ == '__main__':
    main()
