"""
Program:
    Python comic downloader - 999comics type
Author:
    haw

Error Code:
    1 - Program usage error
    3 - Webpage request error
    11 - ComicNotFoundError catch
    12 - UpdateError catch
    16 - CSVError catch
    18 - CSVContentError catch
    31 - HTTPError catch
    32 - DriverError catch
"""

import sys, os
import csv, shutil
import requests

from selenium import webdriver

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
        pycomic.py fetch-url COMICNAME IDENTITYNUM
        pycomic.py help
        pycomic.py list [PATTERN]
        pycomic.py list-menu [PATTERN]
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
    eng_name, ch_name, number, status = _check_comic_existence(pyconfig, comic_name)

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
    for chapter in chapter_list:
        chapter_url = pyconfig.home_url(SECTION) + chapter.get('href')
        chapter_title = chapter.find('span').text
        data.append((chapter_title, chapter_url, date, comic_state))

    # Write csv file
    try:
        pylib.write_csv(comic.path['menu'], data, index=False)
    except pycomic_err.CSVError as err:
        logger.warning('Error: {}'.format(err))
        logger.info('Failed to write to {}'.format(comic.path['menu']))
        sys.exit(16)
    else:
        logger.info('Write file {} success'.format(comic.path['menu']))


def fetch_url(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py fetch-url COMICNAME IDENTITYNUM
    NOTE:
        Use 'pycomic.py list-menu' command to get IDENTITYNUM
    """
    try:
        comic_name = sys.argv[2]
        request_identity = int(sys.argv[3])
    except:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)

    # Find comic from menu csv file
    eng_name, ch_name, number, status = _check_comic_existence(pyconfig, comic_name)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.menu(SECTION), 'menu', extension='_menu.csv')
    # Read comic URL from COMICNAME_menu.csv file
    try:
        comic_data = pylib.csv_datarow(comic.path['menu'], request_identity)
    except pycomic_err.CSVContentError:
        logger.info('Identity Number {} not found'.format(request_identity))
        sys.exit(18)

    driver = pylib.Driver(comic_data[0], comic_data[1])

    # comic.chapter_title, comic.url = comic_data[0], comic_data[1]
    comic.file_path(pyconfig.links(SECTION), 'links', name=comic.english, extension='_{}.csv'.format(driver.chapter_title))
    comic.file_path(pyconfig.links(SECTION), 'links-dir')

    os.makedirs(comic.path['links-dir'], exist_ok=True)

    # Start selenium driver
    try:
        driver.get()
    except:
        logger.info('Driver failed to request {}'.format(driver.chapter_url))
        sys.exit(3)

    # Information parsing
    try:
        driver.find_last_page('#pageSelect option:nth-last-child(1)')
    except pylib.Driver.DriverError as err:
        logger.warning('Error: {}'.format(err))
        logger.info('Failed to get last page value')
        sys.exit(32)

    # Fetch urls
    driver.get_urls('manga', 'next')

    # Write to csv file
    try:
        pylib.write_csv(comic.path['links'], driver.urls, index=True)
    except pycomic_err.CSVError as err:
        logger.warning('Error" {}'.format(err))
        logger.info('Failed to write to {}'.format(comic.path['links']))
        sys.exit(16)
    else:
        logger.info('Write file {} success'.format(comic.path['links']))


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


def list_menu(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py list-menu COMICNAME [PATTERN]
    """
    try:
        comic_name = sys.argv[2]
    except IndexError:
        print(message)
        sys.exit(1)

    try:
        pattern = sys.argv[3]
    except IndexError:
        pattern = ''

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)

    # Find comic from menu csv file
    eng_name, ch_name, number, status = _check_comic_existence(pyconfig, comic_name)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.menu(SECTION), 'menu', extension='_menu.csv')

    # Show menu content
    try:
        pylib.list_file_content(comic.path['menu'], pattern)
    except pycomic_err.CSVError:
        print('File {} not exist'.format(comic.path['menu']))
        print('Use fetch-menu function to create menu file')



def _check_comic_existence(config, comic_name):
    """
    Find comic from menu csv file
    Exit program if no matching comic found
    """
    try:
        return pylib.find_menu_comic(config, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)
