"""
Program:
    Python comic downloader - Fille type
Author:
    haw

Error Code:
    11 - add function error
"""

import sys, os
import csv

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
        pycomic.py help
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
        sys.exit(11)

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
    pylib.write_menu_csv(pyconfig, SECTION, data)

    logger.info('Write {} to menu csv file success'.format(data))

    # Write raw data file
    with open(os.path.join(pyconfig.raw(SECTION), english_name), mode='wt', encoding='utf-8') as file:
        file.writelines('{}\n'.format(content) for content in contents)

    logger.info('Write contents to {} success'.format(pyconfig.raw(SECTION)))



def _check(config, sec_title):
    """
    Directory structure check for file type
    """
    # Check url/raw directory
    os.makedirs(config.raw(sec_title), exist_ok=True)
    # Check url/refind directory
    os.makedirs(config.refine(sec_title), exist_ok=True)

# Move to pycomic class
# def _check(config, sec_title):
#     """
#     Initial check for directory structure
#     """
#     # Check menu directory
#     os.makedirs(config.menu(sec_title), exist_ok=True)
#     # Check url directory
#     os.makedirs(config.links(sec_title), exist_ok=True)
#     # Check books directory
#     os.makedirs(config.images(sec_title), exist_ok=True)
#     # Check pdf directory
#     os.makedirs(config.comics(sec_title), exist_ok=True)
#
#     if not os.path.exists(config.main_menu(sec_title)):
#         file = open(config.main_menu(sec_title), mode='wt', encoding='utf-8')
#         file.close()


# Move to pycomic class
# def _check_menu_duplicate(config, sec_title, ch_name, eng_name, number=None):
#     """
#     Check data in menu file to avoid information duplication
#     """
#     with open(config.main_menu(sec_title), mode='rt', encoding='utf-8') as file:
#         csv_reader = csv.reader(file)
#
#         for index, data in enumerate(csv_reader):
#             # English name duplication
#             if eng_name in data:
#                 logger.info('Line {}: {} in {}'.format(index+1, eng_name, data))
#                 sys.exit(103)
#             # Chinese name duplication
#             if ch_name in data:
#                 logger.info('Line {}: {} in {}'.format(index+1, ch_name, data))
#                 sys.exit(103)
#             # Number duplication
#             if number in data:
#                 logger.info('Line {}: {} in {}'.format(index+1, number, data))
#                 sys.exit(103)


# Move to pycomic class
# def _write_menu_csv(config, sec_title, data):
#     """
#     Write new data to menu csv file
#
#     Parameters:
#         data - tuple
#     """
#     with open(config.main_menu(sec_title), mode='at', encoding='utf-8') as file:
#         csv_writer = csv.writer(file)
#         csv_writer.writerow(data)
