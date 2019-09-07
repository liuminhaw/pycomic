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
    21 - Directory exist error
    31 - HTTPError catch
    32 - DriverError catch
    33 - urlError catch
"""

import sys, os
import csv, shutil, datetime
import requests
import re

from selenium import webdriver
from bs4 import BeautifulSoup

from . import exceptions as pycomic_err
from . import url_collections as url
from . import logging_class as logcl
from . import pycomic_lib as pylib

from . import pycomic_tmp as pytmp


SECTION = 'MANHUAGUI'
LOG_DIR = os.path.join(os.getcwd(), 'log')

logger = logcl.PersonalLog('pycomic_manhuagui', LOG_DIR)


def help():
    message = \
    """
    USAGE:
        pycomic.py add ENGLISHNAME CHINESENAME NUMBER
        pycomic.py convert-image COMICNAME FILETAG
        pycomic.py download COMICNAME FILETAG 
        pycomic.py error-url COMICNAME IDENTITYNUM
        pycomic.py fetch-menu COMICNAME
        pycomic.py fetch-url COMICNAME IDENTITYNUM
        pycomic.py help
        pycomic.py list [PATTERN]
        pycomic.py list-books origin|format COMICNAME [PATTERN]
        pycomic.py list-menu [PATTERN]
        pycomic.py list-pdf COMICNAME [PATTERN]
        pycomic.py list-url COMICNAME [PATTERN]
        pycomic.py make-pdf COMICNAME FILETAG
        pycomic.py source [file|999comics|manhuagui]
        pycomic.py state-change COMICNAME
        pycomic.py url-image COMICNAME IDENTITYNUM
        pycomic.py verify-image COMICNAME FILETAG
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
        process_state = '--------'
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


def convert_image(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py convert-image COMICNAME FILETAG
    NOTE:
        Use 'pycomic.py list-books' command to get FILETAG value
    """
    try:
        comic_name = sys.argv[2]
        request_tag = int(sys.argv[3])
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)

    # Find comic from menu csv file
    try:
        eng_name, ch_name, number, _status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.links(SECTION), 'links-dir')
    # Get request tag's filename
    try:
        request_file = pylib.index_data(comic.path['links-dir'], request_tag, file=False)
    except pycomic_err.CSVError as err:
        logger.warning(err)
        logger.info('Failed to list directory {}'.format(comic.path['links-dir']))
        sys.exit(16)
    except pycomic_err.DataIndexError:
        logger.info('File Tag {} not found'.format(request_tag))
        sys.exit(18)

    comic.file_path(pyconfig.origin(SECTION), 'origin', name=request_file.split('.')[0])
    comic.file_path(pyconfig.formatted(SECTION), 'format', name=request_file.split('.')[0])

    # Convert images
    try:
        os.makedirs(comic.path['format'])
    except FileExistsError:
        logger.warning('Directory {} already exist'.format(comic.path['format']))
        sys.exit(21)

    try:
        pylib.convert_images_jpg(comic.path['origin'], comic.path['format'])
    except IOError:
        logger.warning('Failed to convert {} to jpeg files'.format(comic.path['origin']))
        shutil.rmtree(comic.path['format'])
        sys.exit(15)
    else:
        logger.info('Convert {} to jpeg files success'.format(comic.path['origin']))


def download(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py download COMICNAME FILETAG
    NOTE:
        use 'pycomic.py list-url' command to get FILETAG value
    """
    try:
        comic_name = sys.argv[2]
        request_tag = int(sys.argv[3])
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)

    # Find comic from menu csv file
    try:
        eng_name, ch_name, number, _status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.menu(SECTION), 'menu', extension='_menu.csv')
    comic.file_path(pyconfig.links(SECTION), 'links-dir')

    # Get request referer value
    try:
        comic_data = pylib.index_data(comic.path['menu'], request_tag)
    except pycomic_err.CSVError as err:
        logger.warning(err)
        logger.info('Failed to read file {}'.format(comic.path['menu']))
        sys.exit(16)
    except pycomic_err.DataIndexError:
        logger.info('File Tag {} not found'.format(request_tag))
        sys.exit(18)
    else:
        referer = comic_data[1]

    # Get request tag's filename
    try:
        request_file = pylib.index_data(comic.path['links-dir'], request_tag, file=False)
    except pycomic_err.CSVError as err:
        logger.warning(err)
        logger.info('Failed to list directory {}'.format(comic.path['links-dir']))
        sys.exit(16)
    except pycomic_err.DataIndexError:
        logger.info('File Tag {} not found'.format(request_tag))
        sys.exit(18)

    comic.file_path(pyconfig.origin(SECTION), 'book', name=request_file.split('.')[0])
    comic.file_path(pyconfig.links(SECTION), 'links', name=request_file)

    # Download images
    try:
        os.makedirs(comic.path['book'])
    except OSError:
        logger.warning('Directory {} already exist'.format(comic.path['book']))
        sys.exit(10)

    urls = url.extract_images(comic.path['links'], duplicates=True, extension=False)
    user_agent = pyconfig.useragent(SECTION)
    # Remove book directory if error occur when downloading images
    for index, each_url in enumerate(urls):
        header = {'User-Agent': user_agent, 'Referer': referer + '#p={}'.format(index + 1)}
        try:
            filename = datetime.datetime.now().strftime('%Y%m%dT%H%M%SMS%f')
            url.download_image(each_url, os.path.join(comic.path['book'], filename), header=header)
        except ReferenceError as err:
            logger.warning(err)
            shutil.rmtree(comic.path['book'])
            sys.exit(33)
        except Exception as err:
            logger.warning(err)
            shutil.rmtree(comic.path['book'])
            sys.exit(41)
        
    # Show download error messages
    # for error_message in errors:
        # logger.info(error_message)

    # Download success
    logger.info('Download {} {} complete'.format(comic.english, request_tag))

    
def error_url(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py error_url COMICNAME FILETAG
    NOTE:
        Use 'pycomic.py list-url' command to get FILETAG
    """
    try:
        comic_name = sys.argv[2]
        request_tag = int(sys.argv[3])
    except (IndexError, ValueError):
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)

    # Find comic from menu csv file
    eng_name, ch_name, number, _status = _check_comic_existence(pyconfig, comic_name)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.links(SECTION), 'links-dir')
    # print(pylib.index_data(comic.path['links-dir'], request_tag, file=False))
    try:
        comic.file_path(pyconfig.links(SECTION), 'links', name=pylib.index_data(comic.path['links-dir'], request_tag, file=False))
    except pycomic_err.DataIndexError:
        logger.info('File Tag {} not found'.format(request_tag))
        sys.exit(18)

    # Show errors
    errors = pylib.list_file_content(comic.path['links'], 'error')
    print('File {}'.format(comic.path['links']))
    for index, error in errors:
        print('Page {} error - {}'.format(index, error[1]))


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

    # Find comic form menu csv file - eng_name, ch_name, number, status
    eng_name, ch_name, number, _status = _check_comic_existence(pyconfig, comic_name)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.menu(SECTION), 'menu', extension='_menu.csv')
    comic.comic_site(pyconfig.site_url(SECTION), 'site-url')

    # Page request
    js_code = 'var elements = document.querySelectorAll("#chapter-list-1 ul"); \
        elements.forEach(function(elem) {elem.style.display = "block";});'

    driver = pylib.Driver(eng_name, comic.path['site-url'])
    driver.get()
    driver.page_source(js_execute=js_code)

    # Information parsing
    page_parse = BeautifulSoup(driver.html, 'html.parser')
    css_selector_0 = 'div#chapter-list-0 ul li a'
    css_selector_1 = 'div#chapter-list-1 ul li a'
    date_selector = 'ul.detail-list li.status span'

    if '已完結' in page_parse.text:
        comic_state = '已完結'
    else:
        comic_state = '連載中'

    date = page_parse.select(date_selector)[-1].text
    chapter_list = page_parse.select(css_selector_0)
    if len(chapter_list) == 0:
        chapter_list = page_parse.select(css_selector_1)

    # Construct data
    data = []
    for chapter in chapter_list:
        chapter_url = pyconfig.home_url(SECTION) + chapter.get('href')
        chapter_type = chapter.find_parent('div').find_previous_sibling('h4').text
        chapter_title = '{}-{}'.format(chapter_type, chapter.get('title'))
        data.append((chapter_title, chapter_url, date, comic_state))

    # Write csv file

    # data.sort(key=_menu_sort_function)
    data.sort()
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
    eng_name, ch_name, number, _status = _check_comic_existence(pyconfig, comic_name)
     
    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.menu(SECTION), 'menu', extension='_menu.csv')
    # Read comic URL from COMICNAME_menu.csv file
    try:
        comic_data = pylib.index_data(comic.path['menu'], request_identity)
    except pycomic_err.CSVError as err:
        logger.warning(err)
        logger.info('Failed to read file {}'.format(comic.path['menu']))
        sys.exit(16)
    except pycomic_err.DataIndexError:
        logger.info('Identity Number {} not found'.format(request_identity))
        sys.exit(18)

    driver = pylib.Driver(comic_data[0], comic_data[1])

    # comic.chapter_title, comic.url = comic_data[0], comic_data[1]
    comic.file_path(pyconfig.links(SECTION), 'links', name=comic.english, extension='_{}.csv'.format(driver.chapter_title))
    comic.file_path(pyconfig.links(SECTION), 'links-dir')

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
    driver.get_urls('mangaFile', 'next', error_text=pyconfig.error_url(SECTION))

    # Write to csv file
    os.makedirs(comic.path['links-dir'], exist_ok=True)
    try:
        pylib.write_csv(comic.path['links'], driver.urls, index=True)
    except pycomic_err.CSVError as err:
        logger.warning('Error" {}'.format(err))
        logger.info('Failed to write to {}'.format(comic.path['links']))

        os.remove(comic.path['links'])
        sys.exit(16)
    else:
        logger.info('Write file {} success'.format(comic.path['links']))


def list(pyconfig):
    _message = \
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


def list_books(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py list-books origin|format COMICNAME [PATTERN]
    """
    _ORIGIN = 'origin'
    _FORMAT = 'format'
    source_type = ''

    try:
        source_type = sys.argv[2]
        comic_name = sys.argv[3]
    except IndexError:
        print(message)
        sys.exit(1)

    try:
        pattern = sys.argv[4]
    except IndexError:
        pattern = ''

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)

    # Find comic from menu csv
    eng_name, ch_name, number, _status = _check_comic_existence(pyconfig, comic_name)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.origin(SECTION), 'origin')
    comic.file_path(pyconfig.formatted(SECTION), 'format')

    # Show matching data list
    if source_type == _ORIGIN:
        _print_files(pylib.list_files(comic.path['origin'], pattern))
    elif source_type == _FORMAT:
        _print_files(pylib.list_files(comic.path['format'], pattern))
    else:
        print(message)
        sys.exit(1)


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
    eng_name, ch_name, number, _status = _check_comic_existence(pyconfig, comic_name)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.menu(SECTION), 'menu', extension='_menu.csv')

    # Show menu content
    try:
        _print_contents(pylib.list_file_content(comic.path['menu'], pattern, target_index=0))
    except pycomic_err.CSVError:
        print('File {} not exist'.format(comic.path['menu']))
        print('Use fetch-menu function to create menu file')


def list_pdf(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py list-pdf COMICNAME [PATTERN]
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

    # Find comic from menu csv
    eng_name, ch_name, number, _status = _check_comic_existence(pyconfig, comic_name)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.comics(SECTION), 'pdf-dir')

    # Show matching data
    _print_files(pylib.list_files(comic.path['pdf-dir'], pattern))


def list_url(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py list-url COMICNAME [PATTERN]
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

    # Find comic from menu csv
    eng_name, ch_name, number, _status = _check_comic_existence(pyconfig, comic_name)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.links(SECTION), 'links-dir')

    # Show matching data
    _print_files(pylib.list_files(comic.path['links-dir'], pattern))
    # pylib.list_files(comic.path['links-dir'], pattern)


def make_pdf(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py make-pdf COMICNAME FILETAG
    NOTE:
        Use 'pycomic.py list-books' command to get FILETAG value
    """
    try:
        comic_name = sys.argv[2]
        request_tag = int(sys.argv[3])
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)

    # Find comic from menu csv file 
    # To make sure that comic is already added to data structure
    try:
        eng_name, ch_name, number, _status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.formatted(SECTION), 'books-dir')
    # Get request tag's directory name
    try:
        request_file = pylib.index_data(comic.path['books-dir'], request_tag, file=False)
    except pycomic_err.DataIndexError:
        logger.info('File Tag {} not found'.format(request_tag))
        sys.exit(18)
    
    comic.file_path(pyconfig.comics(SECTION), 'pdf-dir')
    comic.file_path(pyconfig.formatted(SECTION), 'book', name=request_file.split('.')[0])
    comic.file_path(pyconfig.comics(SECTION), 'pdf', name=request_file.split('.')[0])

    # Make pdf
    os.makedirs(comic.path['pdf-dir'], exist_ok=True)

    try:
        pylib.make_pdf(comic.path['book'], comic.path['pdf'])
    except FileNotFoundError:
        logger.warning('Directory {} not exist'.format(comic.path['book']))
        sys.exit(13)
    except pycomic_err.FileExistError:
        logger.info('PDF file {} already exist'.format(comic.path['pdf']))
        sys.exit(14)
    except Exception as err:
        logger.warning('Error: {}'.format(err))
        logger.warning('Failed to make pdf file from {}'.format(comic.path['book']))
        shutil.rmtree(comic.path['pdf'])
        sys.exit(22)
    else:
        logger.info('Make PDF {} success'.format(comic.path['pdf']))


def state_change(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py state-change COMICNAME
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
        _eng_name, _ch_name, _number, status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Change comic state
    COMPLETE = 'complete'
    IN_PROGRESS = '--------'
    if status == IN_PROGRESS:
        status = COMPLETE
    else:
        status = IN_PROGRESS

    try:
        pylib.modify_menu(pyconfig.main_menu(SECTION), comic_name, status=status)
    except pycomic_err.UpdateError:
        logger.warning('Modify {} failed'.format(pyconfig.main_menu(SECTION)))
        sys.exit(12)

    # Success message
    if status == IN_PROGRESS:
        logger.info('{} marked as in progress'.format(comic_name))
    else:
        logger.info('{} marked as process complete'.format(comic_name))

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


def url_image(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py url-image COMICNAME IDENTITYNUM
    NOTE:
        Temporary function to substitutew download, which is not working at the moment
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
    eng_name, ch_name, number, _status = _check_comic_existence(pyconfig, comic_name)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.menu(SECTION), 'menu', extension='_menu.csv')
    # Read comic URL from COMICNAME_menu.csv file
    try:
        comic_data = pylib.index_data(comic.path['menu'], request_identity)
    except pycomic_err.CSVError as err:
        logger.warning(err)
        logger.info('Failed to read file {}'.format(comic.path['menu']))
        sys.exit(16)
    except pycomic_err.DataIndexError:
        logger.info('Identity Number {} not found'.format(request_identity))
        sys.exit(18)

    driver = pytmp.Driver(comic_data[0], comic_data[1])

    # comic.chapter_title, comic.url = comic_data[0], comic_data[1]
    comic.file_path(pyconfig.links(SECTION), 'links', name=comic.english, extension='_{}.csv'.format(driver.chapter_title))
    comic.file_path(pyconfig.links(SECTION), 'links-dir')
    comic.file_path(pyconfig.origin(SECTION), 'book', name=comic.english, extension='_{}'.format(driver.chapter_title))

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

    # Fetch urls and download images
    driver.get_urls_and_images('mangaFile', 'next')

    # Write to csv file
    os.makedirs(comic.path['links-dir'], exist_ok=True)
    try:
        pylib.write_csv(comic.path['links'], driver.urls, index=True)
    except pycomic_err.CSVError as err:
        logger.warning('Error" {}'.format(err))
        logger.info('Failed to write to {}'.format(comic.path['links']))

        os.remove(comic.path['links'])
        sys.exit(16)
    else:
        logger.info('Write file {} success'.format(comic.path['links']))

    # Copy temp images to book location
    try:
        shutil.copytree(driver.dir_path, comic.path['book'])
    except shutil.Error as err:
        # Directory are the same
        logger.warning('Error: {}'.format(err))
        # print('Error: {}'.format(err))
    except OSError as err:
        logger.warning('Error: {}'.format(err))
        # print('Error: {}'.format(err))
    else:
        logger.info('Save images to {} success'.format(comic.path['book']))
        # print('Save images to {} success'.format(comic.path['book']))


def verify_image(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py verify-image COMCINAME FILETAG
    NOTE:
        Use 'pycomic.py list-books' command to get FILETAG value
    """
    try:
        comic_name = sys.argv[2]
        request_tag = int(sys.argv[3])
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)

    # Find comic from menu csv file
    try:
        eng_name, ch_name, number, _status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name, number)
    comic.file_path(pyconfig.origin(SECTION), 'books-dir')
    # Get request tag's filename
    try:
        request_file = pylib.index_data(comic.path['books-dir'], request_tag, file=False)
    except pycomic_err.CSVError as err:
        logger.warning(err)
        logger.info('Failed to list directory {}'.format(comic.path['books-dir']))
        sys.exit(16)
    except pycomic_err.DataIndexError:
        logger.info('File Tag {} not found'.format(request_tag))
        sys.exit(18)

    comic.file_path(pyconfig.origin(SECTION), 'book', name=request_file.split('.')[0])

    # Verification
    try:
        truncated = pylib.verify_images(comic.path['book'])
    except FileNotFoundError:
        logger.warning('Directory {} not exist'.format(comic.path['books']))
        sys.exit(13)

    for image in truncated:
        logger.info('Image file {} in {} {} is truncated'.format(image, comic_name, request_tag))
    logger.info('{} {} verification completed'.format(comic_name, request_tag))


def _check_comic_existence(config, comic_name):
    """
    Find comic from menu csv file
    Exit program if no matching comic found
    """
    try:
        # return eng_name, ch_name, number, status
        return pylib.find_menu_comic(config, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)


def _menu_sort_function(item):
    """
    The value of the key parameter should be a function that 
    takes a single argument and returns a key to use for sorting purposes.
    """
    regex = re.compile(r'\d+')
    match = regex.search(item[0])
    if match is None:
        return -1
    else:
        return int(match.group())


def _print_files(files):
    """
    Output files information to terminal
    """
    print('------ START ------')
    for index, file in files:
        print('FILE TAG {:4d} : {:>20}'.format(index, file))
    print('------- END -------')


def _print_contents(contents):
    """
    Output contents to terminal
    """
    last_update, comic_state = '', ''

    print('------ START ------')
    for index, content in contents:
        last_update, comic_state = content[2], content[3]
        print('Identity Number {:4d} : {}'.format(index, content[0]))

    print('------ INFO -------')
    print('Last Update: {}'.format(last_update))
    print('Comic State: {}'.format(comic_state))
    print('------- END -------')