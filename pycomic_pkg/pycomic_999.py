"""
Program:
    Python comic downloader - 999comics type
Author:
    haw

Error Code:
    1 - Program usage error
    11 - ComicNotFoundError catch
    12 - UpdateError catch
    16 - CSVError catch
    31 - HTTPError catch

"""

import sys, os
import csv, shutil
import requests

from pycomic_pkg import exceptions as pycomic_err
from pycomic_pkg import url_collections as url
from pycomic_pkg import logging_class as logcl
from pycomic_pkg import pycomic_lib as pylib


SECTION = '999COMIC'
LOG_DIR = os.path.join(os.getcwd(), 'log')

logger = logcl.PersonalLog('pycomic_999comic', LOG_DIR)


def help():
    message = \
    """
    USAGE:
        pycomic.py add ENGLISHNAME CHINESENAME NUMBER
        pycomic.py fetch-menu COMICNAME
        pycomic.py help
        pycomic.py list [PATTERN]
    """

    print(message)


def add(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py add ENGLISHNAME CHINESENAME NUMBER
    """

    try:
        english_name = sys.argv[2]
        chinese_name = sys.argv[3]
        book_number = sys.argv[4]
        process_state = '-------'
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)

    # Check to avoid duplicated comic information
    pylib.check_menu_duplicate(pyconfig, SECTION, chinese_name, english_name, book_number)

    # Add data to main menu
    data = [english_name, chinese_name, book_number, process_state]
    try:
        pylib.update_menu(pyconfig.main_menu(SECTION), data)
    except pycomic_err.UpdateError:
        logger.warning('Update {} failed'.format(pyconfig.main_menu(SECTION)))
        sys.exit(12)
    else:
        logger.info('Write {} to menu csv file success'.format(data))


def fetch_menu(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py fetch-menu COMICNAME
    """
    try:
        comic_name = sys.argv[2]
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)

    # Find comic from menu csv file
    try:
        eng_name, ch_name, number, status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.menu(SECTION), 'menu', extension='_menu.csv')
    comic.comic_site(pyconfig.site_url(SECTION), 'site-url')

    # Page request
    try:
        page_parse = pylib.request_page(comic.path['site-url'])
    except requests.exceptions.HTTPError:
        logger.warning('Request to {} fail'.format(comic.path['site-url']))
        sys.exit(31)

    # Information parsing
    css_selector = 'div.chapter-list ul li a'
    date_selector = 'ul.detail-list li.status span'

    chapter_list = page_parse.select(css_selector)
    date = page_parse.select(date_selector)[-1].text

    if '已完結' in page_parse.text:
        comic_state = '已完結'
    else:
        comic_state = '連載中'

    # Construct data
    data = []
    for index, chapter in enumerate(chapter_list):
        chapter_url = pyconfig.home_url(SECTION) + chapter.get('href')
        chapter_title = chapter.find('span').text
        data.append((index, chapter_title, chapter_url, date, comic_state))

    # Write csv file
    try:
        pylib.write_csv(comic.path['menu'], data, index=False)
    except pycomic_err.CSVError as err:
        logger.warning('Error: {}'.format(err))
        logger.info('Failed to write to {}'.format(comic.path['menu']))
        sys.exit(16)
    else:
        logger.info('Write file {} success'.format(comic.path['menu']))


def list(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py list [PATTERN]
    """
    try:
        pattern = sys.argv[2]
    except IndexError:
        pattern = ''

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)

    # Show matching data
    pylib.list_menu_csv(pyconfig, SECTION, pattern)
