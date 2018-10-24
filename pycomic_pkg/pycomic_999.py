"""
Program:
    Python comic downloader - 999comics type
Author:
    haw

Error Code:
    1 - Program usage error
    12 - UpdateError catch
"""

import sys, os
import csv, shutil

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
