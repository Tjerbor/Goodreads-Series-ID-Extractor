"""
Usage:
    remix.audio_dl.py
    remix.audio_dl.py <URL>
    remix.audio_dl.py -h | --help
    remix.audio_dl.py --version
Options:
    No argument                     Will use the clipboard string as URL

    -h --help                       Show this screen.
    --version                       Show version.
"""
import json
import logging
import sys
from typing import Any
from urllib.request import urlopen

import pyperclip
import requests
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

    ISBNs = list(map(lambda book_id: get_book_ISBN(f'https://www.goodreads.com/book/show/{book_id}'), book_ids))
    print('\n'.join(ISBNs))


def get_book_ids(url: str) -> map:
    source = urlopen(url)
    soup = BeautifulSoup(source, 'html.parser')
    books = soup.find_all('div', {'class': 'listWithDividers__item'})
    book_ids = list(map(lambda item: item.find('a', {'data-reactid': True})['href'].removeprefix('/book/show/'), books))
    logging.info(f'Book IDs: {', '.join(book_ids)}')
    return book_ids


def get_book_ISBN(url: str) -> str:
    source = urlopen(url)
    soup = BeautifulSoup(source, 'html.parser')
    metadata = soup.find('script', {'type': 'application/ld+json'})
    json_metadata = json.loads(metadata.text)
    ISBN = json_metadata['isbn']
    logging.info(f'Found ISBN {ISBN} for {url}')
    return ISBN


if __name__ == '__main__':
    main()
