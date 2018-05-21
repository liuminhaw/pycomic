"""
Program:
    Python comic downloader
Author:
    haw
"""

import sys, os, errno
import csv, re
import requests
import pycomic_class as pycl
from pathlib import Path
from bs4 import BeautifulSoup

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.INFO)

# Pre-defined
HOME = str(Path.home())
PY_MENU = os.path.join(HOME, 'pycomic', 'menu')
PY_URL = os.path.join(HOME, 'pycomic', 'url')
PY_BOOKS = os.path.join(HOME, 'pycomic', 'books')
MENU_CSV = 'menu.csv'

COMIC_999_URL_HOME = 'https://www.999comics.com'
COMIC_999_URL = 'https://www.999comics.com/comic/'


def main():

    logging.debug('Menu: {}'.format(PY_MENU))
    logging.debug('URL: {}'.format(PY_URL))
    logging.debug('Books: {}'.format(PY_BOOKS))

    if len(sys.argv) == 1:
        pycomic_help()
    elif sys.argv[1] == 'add':
        pycomic_add()
    elif sys.argv[1] == 'list':
        pycomic_list()
    elif sys.argv[1] == 'download':
        pycomic_download()
    elif sys.argv[1] == 'help':
        pycomic_help()
    elif sys.argv[1] == 'fetch-chapter':
        pycomic_fetch_chapter()
    elif sys.argv[1] == 'fetch-url':
        pycomic_fetch_url()
    elif sys.argv[1] == 'search':
        pycomic_search()
    elif sys.argv[1] == 'make-pdf':
        pycomic_make_pdf()
    else:
        pycomic_help()


def pycomic_help():
    message = \
    """
    USAGE:
        pycomic add ENGLISHNAME CHINESENAME NUMBER
        pycomic download COMICNAME CHAPTER
        pycomic fetch-chapter COMICNAME
        pycomic fetch-url COMICNAME CHAPTER
        pycomic help
        pycomic list [PATTERN]
        pycomic make-pdf COMICNAME CHAPTER
        pycomic search COMICNAME
    """
    print(message)
    sys.exit(1)


def pycomic_add():
    message = \
    """
    USAGE:
        pycomic add ENGLISHNAME CHINESENAME NUMBER
    """
    try:
        english_name = sys.argv[2]
        chinese_name = sys.argv[3]
        number = sys.argv[4]
        data = (english_name, chinese_name, number)
    except IndexError:
        print(message)
        sys.exit(1)

    _check()

    line_number = 0
    menu_csv = os.path.join(PY_MENU, MENU_CSV)
    # Check duplicate comic information
    with open(menu_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for comic_data in csv_reader:
            line_number += 1
            if english_name in comic_data:
                logging.warning('{} in {}. Line: {}'.format(english_name, comic_data, line_number))
                sys.exit(1)
            if chinese_name in comic_data:
                logging.warning('{} in {}. Line: {}'.format(chinese_name, comic_data, line_number))
                sys.exit(1)
            if number in comic_data:
                logging.warning('{} in {}. Line: {}'.format(number, comic_data, line_number))
                sys.exit(1)

    # Write data to file
    with open(menu_csv, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)
    print('Write {} to {} success.'.format(data, menu_csv))


def pycomic_list():
    message = \
    """
    USAGE:
        pycomic list [PATTERN]
    """
    try:
        pattern = sys.argv[2]
    except IndexError:
        pattern = ''

    _check()

    print('----- START -----')
    menu_csv = os.path.join(PY_MENU, MENU_CSV)
    re_pattern = re.compile(r'.*{}.*'.format(pattern))
    with open(menu_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for comic_data in csv_reader:
            if re_pattern.search(comic_data[0]) != None or re_pattern.search(comic_data[1]) != None:
                print('{} / {}: {}'.format(comic_data[0], comic_data[1], comic_data[2]))
    print('------ END ------')


def pycomic_download():
    pass


def pycomic_fetch_chapter():
    message = \
    """
    USAGE:
        pycomic fetch-chapter COMICNAME
    """
    try:
        comic_name = sys.argv[2]
    except IndexError:
        print(message)
        sys.exit(1)

    _check()

    # Find comic in menu.csv file
    search_result = _search(comic_name)
    if search_result == None:
        logging.warning('No match to {} found.'.format(comic_name))
        sys.exit(1)
    comic = pycl.Comic(search_result[0], search_result[1], search_result[2])
    comic.def_url(COMIC_999_URL)
    logging.debug(comic)

    # Make requests
    page_req = requests.get(comic.url)
    try:
        page_req.raise_for_status()
    except:
        logging.warning('Request to {} failed.').format(comic.url)
        sys.exit(1)
    page_req.encoding = 'utf-8'

    # Parse information
    css_selector = 'div.chapter-list ul li a'
    page_parse = BeautifulSoup(page_req.text, 'html.parser')
    chapter_list = page_parse.select(css_selector)

    # Write file
    comic.def_menu(PY_MENU)
    try:
        with open(comic.menu_csv, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            for data in chapter_list:
                chapter_url = COMIC_999_URL_HOME + data.get('href')
                chapter_title = data.find('span').text
                csv_writer.writerow((chapter_title, chapter_url))
    except:
        logging.warning('Failed to write file {}.'.format(comic.menu_csv))
        sys.exit(1)
    else:
        print('Write file {} success.'.format(comic.menu_csv))


def pycomic_fetch_url():
    pass


def pycomic_search():
    pass


def pycomic_make_pdf():
    pass



def _check():
    menu_csv = os.path.join(PY_MENU, MENU_CSV)

    _check_dir_existence(PY_MENU)
    _check_dir_existence(PY_URL)
    _check_dir_existence(PY_BOOKS)

    if not os.path.exists(menu_csv):
        create_file = open(menu_csv, 'w')
        create_file.close()
    logging.debug('Check file {} success.'.format(menu_csv))


def _check_dir_existence(dir):
    try:
        os.makedirs(dir)
        logging.debug('Check dir {} success.'.format(dir))
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise


def _search(name):
    menu_csv = os.path.join(PY_MENU, MENU_CSV)

    with open(menu_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for comic_data in csv_reader:
            if comic_data[0].lower() == name.lower() or comic_data[1].lower() == name.lower():
                return comic_data
    return None



if __name__ == '__main__':
    main()
