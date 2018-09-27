"""
Program:
    Python comic downloader - Fille type
Author:
    haw

Error Code:
    1 - Program usage error
    11 - ComicNotFoundError catch
    21 - Directory exist error
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
        pycomic.py download COMICNAME
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
        process_state = '------'
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
    data = (english_name, chinese_name, process_state)
    # pylib.write_menu_csv(pyconfig, SECTION, data)
    pylib.append_csv(pyconfig.main_menu(SECTION), data)

    logger.info('Write {} to menu csv file success'.format(data))

    # Write raw data file
    comic = pylib.Comic(english_name, chinese_name)
    comic.file_path(pyconfig.raw(SECTION), 'raw')
    pylib.write_txt(comic.path['raw'], contents)

    # Success message
    logger.info('Write contents to {} success'.format(comic.path['raw']))


def download(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py download COMICNAME
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
        eng_name, ch_name, status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name)
    comic.file_path(pyconfig.images(SECTION), 'book')
    comic.file_path(pyconfig.refine(SECTION), 'refine')

    # Download images
    try:
        os.mkdir(comic.path['book'])
    except FileExistsError:
        logger.warning('Directory {} already exist'.format(comic.path['book']))
        sys.exit(21)
    urls = url.extract_images(comic.path['refine'])
    errors = url.download_images(urls, comic.path['book'], header=pyconfig.useragent(SECTION))

    # Show download error messages
    for error_message in errors:
        logger.info(error_message)



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
       eng_name, ch_name, status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name)
    comic.file_path(pyconfig.raw(SECTION), 'raw')
    comic.file_path(pyconfig.refine(SECTION), 'refine')

    # Extract links
    urls = url.extract_images(comic.path['raw'])

    # Save links to extract file
    pylib.write_csv(comic.path['refine'], urls)

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
