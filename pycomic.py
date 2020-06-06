#!/usr/bin/python3
"""
Program:
    Python comic downloader
Author:
    haw
"""

import sys, os, errno, shutil
import csv, re, time, datetime
import requests
import logging

from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image, ImageFile

from pycomic_pkg import pycomic_999 as comic999
from pycomic_pkg import pycomic_file as comic_file
from pycomic_pkg import pycomic_manhuagui as manhuagui

from pycomic_pkg import pycomic_lib as pylib
from pycomic_pkg import user_agent_class as agentcl
from pycomic_pkg import logging_class as logcl
from pycomic_pkg import exceptions as pycomic_err


# Pre-defined
HOME = str(Path.home())
LOG_DIR = os.path.join(os.getcwd(), 'log')
VERSION = 'v2.1.3'

SOURCE_999 = '999comics'
SOURCE_FILE = 'file'
SOURCE_MANHUAGUI = 'manhuagui'

# COMIC_999_URL_HOME = 'https://www.999comics.com'
# COMIC_999_URL = 'https://www.999comics.com/comic/'

logger = logcl.PersonalLog('pycomic', LOG_DIR)
# logging.disable(logging.DEBUG)

# pyconfig = pycl.Config(['.pycomic.ini', os.path.join(HOME, '.pycomic.ini')])
try:
    pyconfig = pylib.Config(['pycomic_config.ini'])
except pycomic_err.ConfigNotFoundError:
    sys.exit(101)


def main():

    # Source type
    try:
        source_type = pyconfig.source()
    except pycomic_err.NoSectionError:
        sys.exit(102)
    except pycomic_err.NoOptionError:
        sys.exit(103)

    # Source type methods
    if source_type.lower() == SOURCE_999:
        _comic999_action()
    elif source_type.lower() == SOURCE_FILE:
        _file_action()
    elif source_type.lower() == SOURCE_MANHUAGUI:
        _manhuagui_action()
    else:
        print('Source type {} not supported'.format(source_type))


def _comic999_action():
    """
    Action determination for source: 999comics
    """

    if len(sys.argv) == 1:
        comic999.help()
    elif sys.argv[1] == 'add':
        comic999.add(pyconfig)
    elif sys.argv[1] == 'convert-image':
        comic999.convert_image(pyconfig)
    elif sys.argv[1] == 'download':
        comic999.download(pyconfig)
    elif sys.argv[1] == 'error-url':
        comic999.error_url(pyconfig)
    elif sys.argv[1] == 'fetch-menu':
        comic999.fetch_menu(pyconfig)
    elif sys.argv[1] == 'fetch-url':
        comic999.fetch_url(pyconfig)
    elif sys.argv[1] == 'help':
        comic999.help()
    elif sys.argv[1] == 'list':
        comic999.list(pyconfig)
    elif sys.argv[1] == 'list-books':
        comic999.list_books(pyconfig)
    elif sys.argv[1] == 'list-menu':
        comic999.list_menu(pyconfig)
    elif sys.argv[1] == 'list-pdf':
        comic999.list_pdf(pyconfig)
    elif sys.argv[1] == 'list-url':
        comic999.list_url(pyconfig)
    elif sys.argv[1] == 'make-pdf':
        comic999.make_pdf(pyconfig)
    elif sys.argv[1] == 'source':
        comic999.source(pyconfig)
    elif sys.argv[1] == 'state-change':
        comic999.state_change(pyconfig)
    elif sys.argv[1] == 'verify-image':
        comic999.verify_image(pyconfig)
    elif sys.argv[1] == 'version':
        comic999.version(VERSION)
    else:
        comic999.help()


def _manhuagui_action():
    """
    Action determination for source: manhuagui
    """
    if len(sys.argv) == 1:
        manhuagui.help()
    elif sys.argv[1] == 'add':
        manhuagui.add(pyconfig)
    elif sys.argv[1] == 'convert-image':
        manhuagui.convert_image(pyconfig)
    elif sys.argv[1] == 'download':
        manhuagui.download(pyconfig)
    elif sys.argv[1] == 'error-url':
        manhuagui.error_url(pyconfig)
    elif sys.argv[1] == 'fetch-menu':
        manhuagui.fetch_menu(pyconfig)
    elif sys.argv[1] == 'fetch-url':
        manhuagui.fetch_url(pyconfig)
    elif sys.argv[1] == 'list':
        manhuagui.list(pyconfig)
    elif sys.argv[1] == 'list-books':
        manhuagui.list_books(pyconfig)
    elif sys.argv[1] == 'list-menu':
        manhuagui.list_menu(pyconfig)
    elif sys.argv[1] == 'list-pdf':
        manhuagui.list_pdf(pyconfig)
    elif sys.argv[1] == 'list-url':
        manhuagui.list_url(pyconfig)
    elif sys.argv[1] == 'make-pdf':
        manhuagui.make_pdf(pyconfig)
    elif sys.argv[1] == 'source':
        manhuagui.source(pyconfig)
    elif sys.argv[1] == 'state-change':
        manhuagui.state_change(pyconfig)
    elif sys.argv[1] == 'url-image':
        manhuagui.url_image(pyconfig)
    elif sys.argv[1] == 'verify-image':
        manhuagui.verify_image(pyconfig)
    elif sys.argv[1] == 'version':
        manhuagui.version(VERSION)
    else:
        manhuagui.help()


def _file_action():
    """
    Action determination for source: file
    """

    if len(sys.argv) == 1:
        comic_file.help()
    elif sys.argv[1] == 'add':
        comic_file.add(pyconfig)
    elif sys.argv[1] == 'convert':
        comic_file.convert(pyconfig)
    elif sys.argv[1] == 'download':
        comic_file.download(pyconfig)
    elif sys.argv[1] == 'list':
        comic_file.list(pyconfig)
    elif sys.argv[1] == 'list-books':
        comic_file.list_books(pyconfig)
    elif sys.argv[1] == 'list-pdf':
        comic_file.list_pdf(pyconfig)
    elif sys.argv[1] == 'list-url':
        comic_file.list_url(pyconfig)
    elif sys.argv[1] == 'make-pdf':
        comic_file.make_pdf(pyconfig)
    elif sys.argv[1] == 'source':
        comic_file.source(pyconfig)
    elif sys.argv[1] == 'state-change':
        comic_file.state_change(pyconfig)
    elif sys.argv[1] == 'fetch-url':
        comic_file.fetch_url(pyconfig)
    elif sys.argv[1] == 'verify':
        comic_file.verify(pyconfig)
    elif sys.argv[1] == 'eyny-download':
        comic_file.eyny_download(pyconfig)
    elif sys.argv[1] == 'version':
        comic_file.version(VERSION)
    else:
        comic_file.help()


def _get_source(source):
    """
    Show current source
    """
    if source == SOURCE_999 or source == SOURCE_FILE:
        print('{}'.format(source))
    else:
        print('Source type {} not supported'.format(source))


def _check(config):
    """
    Initial check for pycomic file structure
    Input:
        config : Config Object
    """
    # pyconfig = pycl.Config(['/etc/.pycomic.ini', '.pycomic.ini'])

    _check_dir_existence(config.menu())
    _check_dir_existence(config.links())
    _check_dir_existence(config.images())
    _check_dir_existence(config.comics())

    if not os.path.exists(config.main_menu()):
        create_file = open(config.main_menu(), 'w')
        create_file.close()
    logger.debug('Check file {} success.'.format(config.main_menu()))


def _check_dir_existence(dir):
    os.makedirs(dir, exist_ok=True)



def _get_image_url(driver):
    img_id = 'manga'
    img_attr = 'src'
    img_tag = 'img'

    # Find image information
    image_url = 'Failed'
    try:
        manga_id = driver.find_element_by_id(img_id)
        logger.debug('Manga ID: {}'.format(manga_id))
        image_webpage = manga_id.get_attribute(img_attr)
        logger.debug('Image Webpage: {}'.format(image_webpage))
        # Open page in new tab
        driver.execute_script("window.open('{page}');".format(page=image_webpage))
        time.sleep(1.2)
        driver.switch_to.window(driver.window_handles[1])
        # Get image url
        image_tag = driver.find_element_by_tag_name(img_tag)
        logger.debug('Image Tag: {}'.format(image_tag))
        image_url = image_tag.get_attribute(img_attr)
        logger.debug('Image URL: {}'.format(image_url))
    except:
        logger.warning('Some Error occurs in _get_image_url')
    finally:
        # Close tab and return focus on first tab
        logger.debug('Handles: {}'.format(driver.window_handles))
        for handle in driver.window_handles[1:]:
            logger.debug('Handle: {}'.format(handle))
            driver.switch_to.window(handle)
            logger.debug('Switch handle')
            driver.close()
        logger.debug('Closing tags success.')
        driver.switch_to.window(driver.window_handles[0])
        logger.debug('_get_image_url Success.')

    return image_url


def _geckolog_clean(geckolog):
    gecko_log = os.path.abspath(geckolog)
    if os.path.isfile(gecko_log):
        os.remove(gecko_log)



if __name__ == '__main__':
    main()
