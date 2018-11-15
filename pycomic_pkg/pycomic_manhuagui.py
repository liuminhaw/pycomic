"""
Program:
    Python comic downloader - manhuagui type
Author:
    haw

Error Code:
    1 - Program usage error
    3 - Webpage request error
    11 - ComicNotFoundError catch
    12 - UpdateError catch
    13 - FileNotFoundError catch
    16 - CSVError catch
    18 - DataIndexEror catch
    31 - HTTPError catch
    32 - DriverError catch
"""

import sys, os
import csv, shutil
import requests

from selenium import webdriver

from . import exceptions as pycomic_err
from . import url_collections as url
from . import logging_class as logcl
from . import pycomic_lib as pylib


SECTION = 'MANHUAGUI'
LOG_DIR = os.path.join(os.getcwd(), 'log')

logger = logcl.PersonalLog('pycomic_manhuagui', LOG_DIR)


def help():
    message = \
    """
    USAGE:
        pycomic.py add ENGLISHNAME CHINESENAME NUMBER
        pycomic.py help
        pycomic.py list [PATTERN]
        pycomic.py source [file|999comics|manhuagui]
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


def source(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py source [file|999comics|manhuagui]
    """
    if len(sys.argv) == 2:
        pylib.get_source(pyconfig)
    elif sys.argv[2] == 'file' or sys.argv[2] == '999comics' or sys.argv[2] == 'manhuagui':
        pylib.set_source(pyconfig, sys.argv[2])
    else:
        print(message)
        sys.exit(1)
