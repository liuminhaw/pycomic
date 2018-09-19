"""
Program:
    Python comic downloader - Fille type
Author:
    haw

Error Code:
    1 - Program usage error
    11 - ComicNotFoundError catch
"""

import sys, os
import csv

from pycomic_pkg import exceptions as pycomic_err
from pycomic_pkg import url_collections as url
from pycomic_pkg import logging_class as logcl
from pycomic_pkg import pycomic_lib as pylib


SECTION = 'FILE'
LOG_DIR = os.path.join(os.getcwd(), 'log')

logger = logcl.PersonalLog('pycomic_file', LOG_DIR)


def help():
    message = \
    """
    USAGE:
        pycomic.py add ENGLISHNAME CHINESENAME
        pycomic.py fetch-url COMICNAME
        pycomic.py help
        pycomic.py list [PATTERN]
        pycomic.py list-url [PATTERN]
    """

    print(message)


def add(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py add ENGLISHNAME CHINESENAME
    """

    try:
        english_name = sys.argv[2]
        chinese_name = sys.argv[3]
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Check to avoid duplicated comic information
    pylib.check_menu_duplicate(pyconfig, SECTION, chinese_name, english_name)

    # Get file content from user
    print('Enter file content. Ctrl-D to save.')
    contents = []

    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    # Write data to main menu
    data = (english_name, chinese_name)
    # pylib.write_menu_csv(pyconfig, SECTION, data)
    pylib.append_csv(pyconfig.main_menu(SECTION), data)

    logger.info('Write {} to menu csv file success'.format(data))

    # Write raw data file
    comic = pylib.Comic(english_name, chinese_name)
    pylib.write_txt(comic.file_path(pyconfig.raw(SECTION)), contents)

    # Success message
    logger.info('Write contents to {} success'.format(pyconfig.raw(SECTION)))


def fetch_url(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py fetch-url COMICNAME
    """
    try:
        comic_name = sys.argv[2]
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Find comic from menu csv file
    try:
       eng_name, ch_name = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Extract links from raw file
    comic = pylib.Comic(eng_name, ch_name)
    urls = url.extract_images(comic.file_path(pyconfig.raw(SECTION)))

    # Save links to extract file
    pylib.write_csv(comic.file_path(pyconfig.refine(SECTION)), urls)

    # Success message
    logger.info('Extract file {} success'.format(eng_name))



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
    _check(pyconfig, SECTION)

    # Show all matching data
    pylib.list_menu_csv(pyconfig, SECTION, pattern)


def list_url(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py list_url [PATTERN]
    """
    try:
        pattern = sys.argv[2]
    except IndexError:
        pattern = ''

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Show all matching data
    pylib.list_files(pyconfig.refine(SECTION), pattern)



def _check(config, sec_title):
    """
    Directory structure check for file type
    """
    # Check url/raw directory
    os.makedirs(config.raw(sec_title), exist_ok=True)
    # Check url/refind directory
    os.makedirs(config.refine(sec_title), exist_ok=True)
