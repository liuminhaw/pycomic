"""
Extract urls from 999 comic site

USAGE:
    comic999_url.py SITEURL OUTPUT_FILEPATH [PAGENUM]
PROGRAM:
    Given an url of comic, scrape through each page and get each url of the image.
"""

import sys, os
import logging, requests, time
import re
import downloader_class as dc
from selenium import webdriver

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.INFO)

USAGE = 'USAGE: comic999_url.py SITEURL OUTPUT_FILEPATH [PAGENUM]'

LASTPAGE_SELECTOR = '#pageSelect option:nth-last-child(1)'
IMG_ID = 'manga'
IMG_ATTR = 'src'
IMG_TAG = 'img'
NEXTPAGE_ID = 'next'

GECKO_LOG = 'geckodriver.log'

REGEXPAGE = r'\d{1,3}'


class Comic():

    def __init__(self, page):
        self.current = 1
        self.last = page

    def __str__(self):
        string = 'Current Page: {}, Last Page: {}'.format(self.current, self.last)
        return string


def comic999_url():

    # Input validation
    try:
        url = sys.argv[1]
        output_file = dc.Directory(sys.argv[2])
    except:
        print(USAGE)
        sys.exit(1)
    output_file.logging()


    # Open web driver
    try:
        url_req = requests.get(url)
        url_req.raise_for_status()
        firefox = webdriver.Firefox()
        firefox.get(url)
    except:
        logging.warning('{} request failed.'.format(url))
        firefox.close()
        geckolog_clean()
        sys.exit(1)


    # Comic information gather
    last_page_elem = firefox.find_element_by_css_selector(LASTPAGE_SELECTOR)
    regex = re.compile(REGEXPAGE)

    try:
        last_page = int(regex.search(last_page_elem.text).group())
    except:
        logging.warning('Finding last page of comic failed.')
        firefox.close()
        geckolog_clean()
        sys.exit(1)

    book = Comic(last_page)
    logging.debug('Book: {}.'.format(str(book)))

    # Check for optional argument PAGENUM
    try:
        book.current = sys.argv[3]
        write_mode = 'a'
    except:
        book.current = 1
        write_mode = 'w'


    # Write in file
    try:
        write_file = open(output_file.abs_path, write_mode)
        while True:
            image_url = get_image_url(firefox)
            logging.debug('Image URL: {}'.format(image_url))
            write_file.write(image_url + '\n')
            print('Write {} success. Page {}'.format(image_url, book.current))
            if book.current == book.last:
                break
            comic_navigation(firefox, book)
    except:
        write_file.write('Write {} failed. Page {}\n'.format(image_url, book.current))
        logging.warning('Write url to {} failed.'.format(output_file.base))
        sys.exit(1)
    finally:
        write_file.close()
        firefox.close()
        geckolog_clean()


def comic_navigation(driver, book):
    next_page = driver.find_element_by_id(NEXTPAGE_ID)
    next_page.click()
    book.current += 1


def get_image_url(driver):
    # Find image information
    manga_id = driver.find_element_by_id(IMG_ID)
    logging.debug('Manga ID: {}'.format(manga_id))
    image_webpage = manga_id.get_attribute(IMG_ATTR)
    logging.debug('Image Webpage: {}'.format(image_webpage))
    # Open page in new tab
    driver.execute_script("window.open('{page}');".format(page=image_webpage))
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    # Get image url
    image_tag = driver.find_element_by_tag_name(IMG_TAG)
    logging.debug('Image Tag: {}'.format(image_tag))
    image_url = image_tag.get_attribute(IMG_ATTR)
    logging.debug('Image URL: {}'.format(image_url))
    # Close tab and return focus on first tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return image_url


def geckolog_clean():
    gecko_log = os.path.abspath(GECKO_LOG)
    if os.path.isfile(gecko_log):
        os.remove(gecko_log)


if __name__ == '__main__':
    comic999_url()
