#!/usr/bin/python
"""
Program:
    Python comic downloader
Author:
    haw
"""

import sys, os, errno, shutil
import csv, re, time, datetime
import requests
import pycomic_class as pycl
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.INFO)

# Pre-defined
HOME = str(Path.home())
PY_MENU = os.path.join(HOME, 'pycomic', 'menu')
PY_URL = os.path.join(HOME, 'pycomic', 'url')
PY_BOOKS = os.path.join(HOME, 'pycomic', 'books')
PY_PDF = os.path.join(HOME, 'pycomic', 'pdf')
MENU_CSV = 'menu.csv'

COMIC_999_URL_HOME = 'https://www.999comics.com'
COMIC_999_URL = 'https://www.999comics.com/comic/'


def main():

    logging.debug('Menu: {}'.format(PY_MENU))
    logging.debug('URL: {}'.format(PY_URL))
    logging.debug('Books: {}'.format(PY_BOOKS))
    logging.debug('PDF: {}'.format(PY_PDF))

    if len(sys.argv) == 1:
        pycomic_help()
    elif sys.argv[1] == 'add':
        pycomic_add()
    elif sys.argv[1] == 'download':
        pycomic_download()
    elif sys.argv[1] == 'fetch-chapter':
        pycomic_fetch_chapter()
    elif sys.argv[1] == 'fetch-url':
        pycomic_fetch_url()
    elif sys.argv[1] == 'help':
        pycomic_help()
    elif sys.argv[1] == 'list':
        pycomic_list()
    elif sys.argv[1] == 'list-menu':
        pycomic_list_menu()
    elif sys.argv[1] == 'list-chapters':
        pycomic_list_chapters()
    elif sys.argv[1] == 'list-url':
        pycomic_list_url()
    elif sys.argv[1] == 'make-pdf':
        pycomic_make_pdf()
    else:
        pycomic_help()


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
        pycomic list-menu COMICNAME [PATTERN]
        pycomic list-chapters
        pycomic list-url COMICNAME [PATTERN]
        pycomic make-pdf COMICNAME DIRECTORYTAG
        pycomic search COMICNAME
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

    _check()

    line_number = 0
    menu_csv = os.path.join(PY_MENU, MENU_CSV)
    # Check duplicate comic information
    with open(menu_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for comic_data in csv_reader:
            line_number += 1
            if english_name in comic_data:
                logging.warning('{} in {}. Line: {}'.format(english_name, comic_data, line_number))
                sys.exit(1)
            if chinese_name in comic_data:
                logging.warning('{} in {}. Line: {}'.format(chinese_name, comic_data, line_number))
                sys.exit(1)
            if number in comic_data:
                logging.warning('{} in {}. Line: {}'.format(number, comic_data, line_number))
                sys.exit(1)

    # Write data to file
    with open(menu_csv, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)
    print('Write {} to {} success.'.format(data, menu_csv))


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

    _check()

    print('----- START -----')
    menu_csv = os.path.join(PY_MENU, MENU_CSV)
    re_pattern = re.compile(r'.*{}.*'.format(pattern))
    with open(menu_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for comic_data in csv_reader:
            if re_pattern.search(comic_data[0]) != None or re_pattern.search(comic_data[1]) != None:
                print('{} / {}: {}'.format(comic_data[0], comic_data[1], comic_data[2]))
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

    _check()

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)

    # Search content in file
    menu_csv = comic.menu_csv
    re_pattern = re.compile(r'.*{}.*'.format(pattern))
    identify_num = 0
    remind_message = None

    try:
        with open(menu_csv, 'r') as csv_file:
            last_update = None
            print('----- START -----')
            csv_reader = csv.reader(csv_file)
            for comic_data in csv_reader:
                if re_pattern.search(comic_data[0]) != None:
                    # Make sure menu include last update in the newer version
                    try:
                        last_update = comic_data[2]
                    except IndexError:
                        remind_message = '{} is an old version.\nPlease update with fetch-chapter command.'.format(menu_csv)
                    print('Identity Number {} : {}'.format(identify_num, comic_data[0]))
                identify_num += 1
            if last_update is not None:
                print('Last Update: {}'.format(last_update))
            print('------ END ------')
    except FileNotFoundError:
        logging.warning('File {} not exist.'.format(menu_csv))
        sys.exit(1)

    # Remind for update
    if remind_message is not None:
        print(remind_message)


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

    _check()

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)
    comic.def_book_dir(PY_BOOKS)

    # Show exist chapter file
    re_pattern = re.compile(r'.*{}.*'.format(pattern), re.IGNORECASE)
    _check_dir_existence(comic.book_dir)
    dir_list = os.listdir(comic.book_dir)
    dir_list.sort()
    print('----- START -----')
    for dir_tag, dir in enumerate(dir_list):
        if re_pattern.search(dir) != None:
            print('Directory Tag {}: {}'.format(dir_tag, dir))
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

    _check()

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)
    comic.def_chapter_dir(PY_URL)

    # Search existing url file
    re_pattern = re.compile(r'.*{}.*'.format(pattern), re.IGNORECASE)
    file_tag = 0
    _check_dir_existence(comic.chapter_dir)
    file_list = os.listdir(comic.chapter_dir)
    file_list.sort()
    print('----- START -----')
    for file in file_list:
        if re_pattern.search(file) != None:
            print('FILE TAG {} : {}'.format(file_tag, file))
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

    _check()

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)
    comic.def_chapter_dir(PY_URL)
    comic.def_book_dir(PY_BOOKS)
    _check_dir_existence(comic.chapter_dir)
    _check_dir_existence(comic.book_dir)

    # Find correct comic url csv file
    file_list = os.listdir(comic.chapter_dir)
    file_list.sort()
    for file_tag, file in enumerate(file_list):
        if file_tag == request_tag:
            # filename = os.path.splitext(file)[0]
            filename = file
            logging.debug('Filename: {}'.format(filename))

    try:
        comic.def_book(PY_BOOKS, os.path.splitext(filename)[0])
        logging.debug('{}'.format(comic.book))
    except NameError:
        logging.warning('File Tag {} not exist.'.format(request_tag))
        sys.exit(1)

    # Make sure not to write same chapter repeatly
    try:
        os.mkdir(comic.book)
    except FileExistsError:
        logging.warning('Directory {} already exist.'.format(comic.book))
        sys.exit(1)

    # Write images
    # user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}

    with open(os.path.join(comic.chapter_dir, filename), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for page, url in csv_reader:
            try_times = 0
            img_name = os.path.splitext(filename)[0] + '-' + datetime.datetime.now().strftime('%Y%m%dT%H%M%SMS%f') + '.' + url.split('.')[-1]
            img_path = os.path.join(comic.book, img_name)

            while try_times <= 10:
                img_request = requests.get(url, headers=user_agent)
                try:
                    img_request.raise_for_status()
                except:
                    logging.warning('Page {} - {} request failed.'.format(page, url))
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
                logging.warning('Exceed try time limit.')
                shutil.rmtree(comic.book)
                logging.warning('Remove directory {}.'.format(comic.book))
                sys.exit(1)

    print('Write {} complete.'.format(comic.book))


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

    _check()

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)

    # Make requests
    page_req = requests.get(comic.url)
    try:
        page_req.raise_for_status()
    except:
        logging.warning('Request to {} failed.').format(comic.url)
        sys.exit(1)
    page_req.encoding = 'utf-8'

    # Parse information
    css_selector = 'div.chapter-list ul li a'
    date_selector = 'ul.detail-list li.status span'
    page_parse = BeautifulSoup(page_req.text, 'html.parser')
    chapter_list = page_parse.select(css_selector)
    date = page_parse.select(date_selector)

    # Write file
    try:
        with open(comic.menu_csv, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            for data in chapter_list:
                chapter_url = COMIC_999_URL_HOME + data.get('href')
                chapter_title = data.find('span').text
                csv_writer.writerow((chapter_title, chapter_url, date[-1].text))
    except:
        logging.warning('Failed to write file {}.'.format(comic.menu_csv))
        sys.exit(1)
    else:
        print('Write file {} success.'.format(comic.menu_csv))


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

    _check()

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
        logging.warning('Identity Number {} not exist.'.format(request_identity))
        sys.exit(1)
    except:
        logging.warning('Failed to read file {}.'.format(comic.menu_csv))
        sys.exit(1)
    finally:
        logging.debug('Chapter url: {}'.format(chapter_url))

    # Open Firefox web driver
    geckolog = 'geckodriver.log'
    try:
        firefox = webdriver.Firefox()
        firefox.get(chapter_url)
    except:
        logging.warning('{} request failed.'.format(chapter_url))
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
        logging.warning('Failed to find last page of comic.')
        firefox.close()
        _geckolog_clean(geckolog)
        sys.exit(1)

    # Write urls to file
    comic.def_chapter(PY_URL, chapter_num)
    comic.def_chapter_dir(PY_URL)
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
        logging.warning('Try getting url at page {} exceed limit times'.format(current_page))
    except:
        logging.warning('Failed to write url to {} at page {}.'.format(comic.chapter_csv, current_page))
        sys.exit(1)
    finally:
        csv_file.close()
        firefox.close()
        _geckolog_clean(geckolog)
    print('{} fetch urls success.'.format(comic_name))


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
    except:
        print(message)
        sys.exit(1)

    _check()

    # Find comic in menu.csv file
    comic = _comic_in_menu(comic_name)
    comic.def_book_dir(PY_BOOKS)
    book_name = None

    # Get directory to for making pdf
    dir_list = os.listdir(comic.book_dir)
    dir_list.sort()
    try:
        for tag_num, dir in enumerate(dir_list):
            if dir_tag == tag_num:
                book_name = dir
        if book_name == None:
            raise Warning
    except Warning:
        logging.warning('Directory Tag {} not exist.'.format(dir_tag))
        sys.exit(1)
    except:
        logging.warning('Failed to get target directory.')
        sys.exit(1)
    else:
        logging.debug('Book Name: {}'.format(book_name))
        comic.def_book(PY_BOOKS, book_name)

    # Preparation for making pdf
    comic.def_pdf_dir(PY_PDF)
    comic.def_pdf(PY_PDF, book_name)
    logging.debug('PDF directory: {}'.format(comic.pdf_dir))
    logging.debug('PDF File: {}'.format(comic.pdf))

    _check_dir_existence(comic.pdf_dir)

    if os.path.isfile(comic.pdf):
        logging.warning('File {} already exist.'.format(comic.pdf))
        sys.exit(1)

    # Making pdf file
    pages = os.listdir(comic.book)
    pages.sort()
    for index, page in enumerate(pages):
        image = Image.open(os.path.join(comic.book, page))
        try:
            image.save(comic.pdf, 'PDF', resolution=100, save_all=True, append=True)
        except IOError:
            image.save(comic.pdf, 'PDF', resolution=100, save_all=True)
        except:
            os.remove(comic.pdf)
            logging.warning('Failed to make PDF, some problem occurs.')
            sys.exit(1)
        print('Write page {:3} Success.'.format(index+1))

    print('Make PDF {} success.'.format(book_name))



def _check():
    menu_csv = os.path.join(PY_MENU, MENU_CSV)

    _check_dir_existence(PY_MENU)
    _check_dir_existence(PY_URL)
    _check_dir_existence(PY_BOOKS)
    _check_dir_existence(PY_PDF)

    if not os.path.exists(menu_csv):
        create_file = open(menu_csv, 'w')
        create_file.close()
    logging.debug('Check file {} success.'.format(menu_csv))


def _check_dir_existence(dir):
    try:
        os.makedirs(dir)
        logging.debug('Check dir {} success.'.format(dir))
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise


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
        logging.warning('No match to {} found.'.format(comic_name))
        sys.exit(1)
    comic = pycl.Comic(search_result[0], search_result[1], search_result[2])
    comic.def_url(COMIC_999_URL)
    comic.def_menu(PY_MENU)
    logging.debug(comic)
    return comic


def _search(name):
    menu_csv = os.path.join(PY_MENU, MENU_CSV)

    with open(menu_csv, 'r') as csv_file:
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
        logging.debug('Manga ID: {}'.format(manga_id))
        image_webpage = manga_id.get_attribute(img_attr)
        logging.debug('Image Webpage: {}'.format(image_webpage))
        # Open page in new tab
        driver.execute_script("window.open('{page}');".format(page=image_webpage))
        time.sleep(1.2)
        driver.switch_to.window(driver.window_handles[1])
        # Get image url
        image_tag = driver.find_element_by_tag_name(img_tag)
        logging.debug('Image Tag: {}'.format(image_tag))
        image_url = image_tag.get_attribute(img_attr)
        logging.debug('Image URL: {}'.format(image_url))
    except:
        logging.debug('Some Error occurs in _get_image_url')
    finally:
        # Close tab and return focus on first tab
        logging.debug('Handles: {}'.format(driver.window_handles))
        for handle in driver.window_handles[1:]:
            logging.debug('Handle: {}'.format(handle))
            driver.switch_to.window(handle)
            logging.debug('Switch handle')
            driver.close()
        logging.debug('Closing tags success.')
        driver.switch_to.window(driver.window_handles[0])
        logging.debug('_get_image_url Success.')

    return image_url


def _geckolog_clean(geckolog):
    gecko_log = os.path.abspath(geckolog)
    if os.path.isfile(gecko_log):
        os.remove(gecko_log)



if __name__ == '__main__':
    main()
