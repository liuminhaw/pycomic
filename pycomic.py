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

from pycomic_pkg import pycomic_lib as pylib
from pycomic_pkg import user_agent_class as agentcl
from pycomic_pkg import logging_class as logcl


# Pre-defined
HOME = str(Path.home())
LOG_DIR = os.path.join(os.getcwd(), 'log')

COMIC_999_URL_HOME = 'https://www.999comics.com'
COMIC_999_URL = 'https://www.999comics.com/comic/'

logger = logcl.PersonalLog('pycomic', LOG_DIR)
# logging.disable(logging.DEBUG)

# pyconfig = pycl.Config(['.pycomic.ini', os.path.join(HOME, '.pycomic.ini')])
pyconfig = pylib.Config(['pycomic_config.ini'])


def main():

    # Source type
    source_type = pyconfig.source()

    # Apply different method according to source type
    if source_type.lower() == '999comics':
        _comic999_action()
    elif source_type.lower() == 'file':
        _file_action()
    else:
        pass

    # if len(sys.argv) == 1:
    #     pycomic_help()
    # elif sys.argv[1] == 'add':
    #     pycomic_add()
    # elif sys.argv[1] == 'download':
    #     pycomic_download()
    # elif sys.argv[1] == 'fetch-chapter':
    #     pycomic_fetch_chapter()
    # elif sys.argv[1] == 'fetch-url':
    #     pycomic_fetch_url()
    # elif sys.argv[1] == 'help':
    #     pycomic_help()
    # elif sys.argv[1] == 'list':
    #     pycomic_list()
    # elif sys.argv[1] == 'list-menu':
    #     pycomic_list_menu()
    # elif sys.argv[1] == 'list-pdf':
    #     pycomic_list_pdf()
    # elif sys.argv[1] == 'list-chapters':
    #     pycomic_list_chapters()
    # elif sys.argv[1] == 'list-url':
    #     pycomic_list_url()
    # elif sys.argv[1] == 'make-pdf':
    #     pycomic_make_pdf()
    # elif sys.argv[1] == 'verify':
    #     pycomic_verify()
    # else:
    #     pycomic_help()


def pycomic_help():
    message = \
    """
    USAGE:
        pycomic add ENGLISHNAME CHINESENAME NUMBER
        pycomic download COMICNAME FILETAG
        pycomic fetch-chapter COMICNAME
        pycomic fetch-url COMICNAME IDENTITYNUM
        pycomic help
        pycomic list [PATTERN]
        pycomic list-chapters
        pycomic list-menu COMICNAME [PATTERN]
        pycomic list-pdf COMICNAME [PATTERN]
        pycomic list-url COMICNAME [PATTERN]
        pycomic make-pdf COMICNAME DIRECTORYTAG
        pycomic verify COMICNAME DIRECTORYTAG
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

    _check(pyconfig)

    line_number = 0
    # menu_csv = os.path.join(PY_MENU, MENU_CSV)
    menu_csv = pyconfig.main_menu()

    # Check duplicate comic information
    with open(menu_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for comic_data in csv_reader:
            line_number += 1
            # Check for ENGLISHNAME duplicate
            if english_name in comic_data:
                logger.info('{} in {}. Line: {}'.format(english_name, comic_data, line_number))
                sys.exit(1)
            # Check for CHINESENAME duplicate
            if chinese_name in comic_data:
                logger.info('{} in {}. Line: {}'.format(chinese_name, comic_data, line_number))
                sys.exit(1)
            # Check for NUMBER duplicate
            if number in comic_data:
                logger.info('{} in {}. Line: {}'.format(number, comic_data, line_number))
                sys.exit(1)

    # Write data to file
    with open(menu_csv, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)
    logger.info('Write {} to {} success.'.format(data, menu_csv))


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

    _check(pyconfig)

    print('----- START -----')
    re_pattern = re.compile(r'.*{}.*'.format(pattern), re.IGNORECASE)
    with open(pyconfig.main_menu(), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for comic_data in csv_reader:
            if re_pattern.search(comic_data[0]) != None or re_pattern.search(comic_data[1]) != None:
                print('{:6} : {:20} {:10}'.format(comic_data[2], comic_data[0], comic_data[1]))
    print('------ END ------')


def pycomic_list_menu():
    message = \
    """
    USAGE:
        pycomic list-menu COMICNAME [PATTERN]
    """
    try:
        comic_name = sys.argv[2]
    except IndexError:
        print(message)
        sys.exit(1)

    try:
        pattern = sys.argv[3]
    except:
        pattern = ''

    _check(pyconfig)

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)

    # Search content in file
    # menu_csv = comic.menu_csv
    re_pattern = re.compile(r'.*{}.*'.format(pattern))
    identify_num = 0
    remind_message = None

    try:
        with open(comic.menu_csv, 'r') as csv_file:
            last_update, comic_state = None, None
            print('----- START -----')
            csv_reader = csv.reader(csv_file)
            for comic_data in csv_reader:
                if re_pattern.search(comic_data[0]) != None:
                    # Make sure menu include last update in the newer version
                    try:
                        last_update = comic_data[2]
                        comic_state = comic_data[3]
                    except IndexError:
                        remind_message = '{} is an old version.\nPlease update with fetch-chapter command.'.format(comic.menu_csv)
                    print('Identity Number {:4d} : {}'.format(identify_num, comic_data[0]))
                identify_num += 1

            print('------ INFO ------')
            if last_update is not None:
                print('Last  Update: {}'.format(last_update))
            if comic_state is not None:
                print('Comic Status: {}'.format(comic_state))

            if remind_message is not None:
                print('')
                print(remind_message)
            print('------- END ------')
    except FileNotFoundError:
        logger.warning('File {} not exist.'.format(comic.menu_csv))
        sys.exit(1)


def pycomic_list_chapters():
    message = \
    """
    USAGE:
        pycomic list-chapter COMICNAME [PATTERN]
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

    _check(pyconfig)

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)
    comic.def_book_dir(pyconfig.images())

    # Show exist chapter file
    re_pattern = re.compile(r'.*{}.*'.format(pattern), re.IGNORECASE)
    _check_dir_existence(comic.book_dir)
    dir_list = os.listdir(comic.book_dir)
    dir_list.sort()
    print('----- START -----')
    for dir_tag, dir in enumerate(dir_list):
        if re_pattern.search(dir) != None:
            print('Directory Tag {:4d} : {}'.format(dir_tag, dir))
    print('------ END ------')


def pycomic_list_pdf():
    message = \
    """
    USAGE:
        pycomic list-pdf COMICNAME [PATTERN]
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

    _check(pyconfig)

    # See if comic exist
    comic = _comic_in_menu(comic_name)
    comic.def_pdf_dir(pyconfig.comics())

    # Search and show existing pdf files
    re_pattern = re.compile(r'.*{}.*'.format(pattern), re.IGNORECASE)
    _check_dir_existence(comic.pdf_dir)
    file_list = os.listdir(comic.pdf_dir)
    file_list.sort()
    print('----- START -----')
    for file in file_list:
        if re_pattern.search(file) != None:
            print('Comic Book : {:>20}'.format(file))
    print('------ END ------')


def pycomic_list_url():
    message = \
    """
    USAGE:
        pycomic list-url COMICNAME [PATTERN]
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

    _check(pyconfig)

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)
    comic.def_chapter_dir(pyconfig.links())

    # Search existing url file
    re_pattern = re.compile(r'.*{}.*'.format(pattern), re.IGNORECASE)
    file_tag = 0
    _check_dir_existence(comic.chapter_dir)
    file_list = os.listdir(comic.chapter_dir)
    file_list.sort()
    print('----- START -----')
    for file in file_list:
        if re_pattern.search(file) != None:
            print('FILE TAG {:4d} : {:>20}'.format(file_tag, file))
        file_tag += 1
    print('------ END ------')


def pycomic_download():
    message = \
    """
    USAGE:
        pycomic download COMICNAME FILETAG
    NOTE:
        use 'pycomic list-url' command to get FILETAG
    """
    try:
        comic_name = sys.argv[2]
        request_tag = int(sys.argv[3])
    except IndexError:
        print(message)
        sys.exit(1)
    except ValueError:
        logger.info("Please enter numeric value for FILETAG")
        sys.exit(1)

    _check(pyconfig)

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)
    comic.def_chapter_dir(pyconfig.links())
    comic.def_book_dir(pyconfig.images())
    _check_dir_existence(comic.chapter_dir)
    _check_dir_existence(comic.book_dir)

    # Find correct comic url csv file
    file_list = os.listdir(comic.chapter_dir)
    file_list.sort()
    for file_tag, file in enumerate(file_list):
        if file_tag == request_tag:
            # filename = os.path.splitext(file)[0]
            filename = file
            logger.debug('Filename: {}'.format(filename))

    try:
        comic.def_book(pyconfig.images(), os.path.splitext(filename)[0])
        logger.debug('{}'.format(comic.book))
    except NameError:
        logger.warning('File Tag {} not exist.'.format(request_tag))
        sys.exit(1)

    # Make sure not to write same chapter repeatly
    try:
        os.mkdir(comic.book)
    except FileExistsError:
        logger.warning('Directory {} already exist.'.format(comic.book))
        sys.exit(1)

    # Write images
    # random_user_agent = agentcl.UserAgent().load_random()
    # print('User Agent: {}'.format(random_user_agent))
    # user_agent = {'User-Agent': random_user_agent}
    user_agent = {'User-Agent': pyconfig.useragent()}


    with open(os.path.join(comic.chapter_dir, filename), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for page, url in csv_reader:
            try_times = 0
            img_name = os.path.splitext(filename)[0] + '-' + datetime.datetime.now().strftime('%Y%m%dT%H%M%SMS%f') + '.' + url.split('.')[-1]
            img_path = os.path.join(comic.book, img_name)

            while try_times <= 10:
                try:
                    img_request = requests.get(url, headers=user_agent)
                    img_request.raise_for_status()
                except:
                    logger.warning('Page {} - {} request failed.'.format(page, url))
                    try_times += 1
                    time.sleep(1)
                else:
                    with open(img_path, 'wb') as write_file:
                        for chunk in img_request.iter_content(10000):
                            write_file.write(chunk)
                        print('Write page {} - {} image success.'.format(page, img_name))
                    time.sleep(1)
                    break
            else:
                logger.warning('Exceed try time limit.')
                shutil.rmtree(comic.book)
                logger.info('Remove directory {}.'.format(comic.book))
                sys.exit(1)

    logger.info('Write {} {} complete.'.format(comic.book, request_tag))


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

    _check(pyconfig)

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)

    # Make requests
    try:
        page_req = requests.get(comic.url)
        page_req.raise_for_status()
    except:
        logger.warning('Request to {} failed.').format(comic.url)
        sys.exit(1)
    page_req.encoding = 'utf-8'

    # Parse information
    css_selector = 'div.chapter-list ul li a'
    date_selector = 'ul.detail-list li.status span'
    status_selector = 'ul.detail-list li.status span span.dgreen'
    page_parse = BeautifulSoup(page_req.text, 'html.parser')

    chapter_list = page_parse.select(css_selector)
    date = page_parse.select(date_selector)
    status = page_parse.select(status_selector)

    # Determine comic status (In progress or Complete)
    try:
        comic_state = status[0].text
    except:
        comic_state = date[-2].text

    # Write file
    try:
        with open(comic.menu_csv, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            for data in chapter_list:
                chapter_url = COMIC_999_URL_HOME + data.get('href')
                chapter_title = data.find('span').text
                csv_writer.writerow((chapter_title, chapter_url, date[-1].text, comic_state))
    except:
        logger.warning('Failed to write file {}.'.format(comic.menu_csv))
        sys.exit(1)
    else:
        logger.info('Write file {} success.'.format(comic.menu_csv))


def pycomic_fetch_url():
    message = \
    """
    USAGE:
        pycomic fetch-url COMICNAME IDENTITYNUM
    NOTE:
        use 'pycomic list-menu' command to get IDENTITYNUM
    """
    try:
        comic_name = sys.argv[2]
        request_identity = int(sys.argv[3])
    except IndexError:
        print(message)
        sys.exit(1)
    except ValueError:
        logger.info("Please enter numeric value for IDENTITYNUM")
        sys.exit(1)


    _check(pyconfig)

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)
    chapter_url, chapter_num = None, None

    # URL to comic chapter
    try:
        with open(comic.menu_csv, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for identity_num, comic_data in enumerate(csv_reader):
                if request_identity == identity_num:
                    chapter_num, chapter_url = comic_data[0], comic_data[1]
            if chapter_num == None or chapter_url ==None:
                raise Warning
    except Warning:
        logger.warning('Identity Number {} not exist.'.format(request_identity))
        sys.exit(1)
    except:
        logger.warning('Failed to read file {}.'.format(comic.menu_csv))
        sys.exit(1)
    finally:
        logger.debug('Chapter url: {}'.format(chapter_url))

    # Open Firefox web driver
    geckolog = 'geckodriver.log'
    try:
        firefox = webdriver.Firefox()
        firefox.get(chapter_url)
    except:
        logger.warning('{} request failed.'.format(chapter_url))
        firefox.close()
        _geckolog_clean(geckolog)
        sys.exit(1)

    # Preparation for gather urls
    last_page_selector = '#pageSelect option:nth-last-child(1)'
    last_page_elem = firefox.find_element_by_css_selector(last_page_selector)
    num_regex = re.compile(r'\d{1,3}')

    try:
        last_page = int(num_regex.search(last_page_elem.text).group())
    except:
        logger.warning('Failed to find last page of comic.')
        firefox.close()
        _geckolog_clean(geckolog)
        sys.exit(1)

    # Write urls to file
    comic.def_chapter(pyconfig.links(), chapter_num)
    comic.def_chapter_dir(pyconfig.links())
    _check_dir_existence(comic.chapter_dir)
    current_page = 1
    try_times = 0
    try:
        csv_file = open(comic.chapter_csv, 'w')
        csv_writer = csv.writer(csv_file)
        while True:
            # Try _get_image_url for multiple times if failed
            if try_times > 4:
                raise Warning
            image_url = _get_image_url(firefox)
            if image_url == 'Failed':
                try_times += 1
                continue
            # Get image url successful
            csv_writer.writerow((current_page, image_url))
            print('Write page {} success - {}'.format(current_page, image_url))
            if current_page == last_page:
                break
            next_page = firefox.find_element_by_id('next')
            next_page.click()
            current_page += 1
    except Warning:
        logger.warning('Try getting url at page {} exceed limit times'.format(current_page))
        sys.exit(1)
    except:
        logger.warning('Failed to write url to {} at page {}.'.format(comic.chapter_csv, current_page))
        sys.exit(1)
    finally:
        csv_file.close()
        firefox.close()
        _geckolog_clean(geckolog)
    logger.info('{} {} fetch urls success.'.format(comic_name, request_identity))


def pycomic_make_pdf():
    message = \
    """
    USAGE:
        pycomic make-pdf COMICNAME DIRECTORYTAG
    NOTE:
        Get DIRECTORYTAG value from list-chapters command
    """
    try:
        comic_name = sys.argv[2]
        dir_tag = int(sys.argv[3])
    except IndexError:
        print(message)
        sys.exit(1)
    except ValueError:
        logger.info("Please enter numeric value for DIRECTORYTAG")
        sys.exit(1)

    _check(pyconfig)

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)
    comic.def_book_dir(pyconfig.images())
    book_name = None

    # Get directory for making pdf
    dir_list = os.listdir(comic.book_dir)
    dir_list.sort()
    try:
        for tag_num, dir in enumerate(dir_list):
            if dir_tag == tag_num:
                book_name = dir
        if book_name == None:
            raise Warning
    except Warning:
        logger.warning('Directory Tag {} not exist.'.format(dir_tag))
        sys.exit(1)
    except:
        logger.warning('Failed to get target directory.')
        sys.exit(1)
    else:
        logger.debug('Book Name: {}'.format(book_name))
        comic.def_book(pyconfig.images(), book_name)

    # Preparation for making pdf
    comic.def_pdf_dir(pyconfig.comics())
    comic.def_pdf(pyconfig.comics(), book_name)
    logger.debug('PDF directory: {}'.format(comic.pdf_dir))
    logger.debug('PDF File: {}'.format(comic.pdf))

    # Check directory and file existence
    _check_dir_existence(comic.pdf_dir)

    if os.path.isfile(comic.pdf):
        logger.warning('File {} already exist.'.format(comic.pdf))
        sys.exit(1)

    # Making pdf file
    # ImageFile.LOAD_TRUNCATED_IMAGES = True
    pages = os.listdir(comic.book)
    pages.sort()

    images = []
    for page in pages:
        images.append(Image.open(os.path.join(comic.book, page)))
    images[0].save(comic.pdf, 'PDF', resolution=100, save_all=True, append_images=images[1:])

    logger.info('Make PDF {} success.'.format(book_name))


def pycomic_verify():
    message = \
    """
    USAGE:
        pycomic.py verify COMICNAME DIRECTORYTAG
    NOTE:
        Get DIRECTORYTAG value from list-chapters command
    """
    try:
        comic_name = sys.argv[2]
        dir_tag = int(sys.argv[3])
    except IndexError:
        print(message)
        sys.exit(1)
    except ValueError:
        logger.info("Please enter numeric value for DIRECTORYTAG")
        sys.exit(1)

    _check(pyconfig)

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)
    comic.def_book_dir(pyconfig.images())
    book_name = None

    # Get directory of images to verify
    dir_list = os.listdir(comic.book_dir)
    dir_list.sort()
    try:
        for tag_num, dir in enumerate(dir_list):
            if dir_tag == tag_num:
                book_name = dir
        if book_name == None:
            raise Warning
    except Warning:
        logger.warning('Directory Tag {} not exist.'.format(dir_tag))
        sys.exit(1)
    except:
        logger.warning('Failed to get target directory.')
        sys.exit(1)
    else:
        logger.debug('Book Name: {}'.format(book_name))
        comic.def_book(pyconfig.images(), book_name)

    # Verify images
    images = os.listdir(comic.book)
    images.sort()

    for image in images:
        img = Image.open(os.path.join(comic.book, image))
        # print('Verify {}'.format(image))
        try:
            img.load()
        except IOError:
            logger.info("Image file {} is truncated.".format(os.path.join(comic.book, image)))
        finally:
            img.close()

    print('Verification completed.')


def _comic999_action():
    """
    Action determination for source: 999comics
    """

    if len(sys.argv) == 1:
        comic999.help()
    elif sys.argv[1] == 'add':
        comic999.add(pyconfig)
    elif sys.argv[1] == 'download':
        comic999.download()
    elif sys.argv[1] == 'fetch-chapter':
        comic999.fetch_chapter()
    elif sys.argv[1] == 'fetch-url':
        comic999.fetch_url()
    elif sys.argv[1] == 'help':
        comic999.help()
    elif sys.argv[1] == 'list':
        comic999.list(pyconfig)
    elif sys.argv[1] == 'list-menu':
        comic999.list_menu()
    elif sys.argv[1] == 'list-pdf':
        comic999.list_pdf()
    elif sys.argv[1] == 'list-chapters':
        comic999.list_chapters()
    elif sys.argv[1] == 'list-url':
        comic999.list_url()
    elif sys.argv[1] == 'make-pdf':
        comic999.make_pdf()
    elif sys.argv[1] == 'verify':
        comic999.verify()
    else:
        comic999.help()


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
    elif sys.argv[1] == 'state-change':
        comic_file.state_change(pyconfig)
    elif sys.argv[1] == 'fetch-url':
        comic_file.fetch_url(pyconfig)
    elif sys.argv[1] == 'verify':
        comic_file.verify(pyconfig)
    else:
        comic_file.help()



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


def _comic_in_menu(comic_name):
    """
    Find if comic_name is in menu.csv file
    If Exist:
        return Comic class object
    If not Exist:
        Inform user and quit program
    """
    search_result = _search(comic_name)
    if search_result == None:
        logger.warning('No match to {} found.'.format(comic_name))
        sys.exit(1)
    comic = pycl.Comic(search_result[0], search_result[1], search_result[2])
    comic.def_url(COMIC_999_URL)
    comic.def_menu(pyconfig.menu())
    logger.debug(comic)
    return comic


def _search(name):
    # menu_csv = os.path.join(PY_MENU, MENU_CSV)

    with open(pyconfig.main_menu(), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for comic_data in csv_reader:
            if comic_data[0].lower() == name.lower() or comic_data[1].lower() == name.lower():
                return comic_data
    return None



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
