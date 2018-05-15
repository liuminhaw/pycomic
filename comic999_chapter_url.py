"""
Get each chapter's url of a comic

USAGE:
    comic999_chapter_url.py OUTPUT_FILEPATH COMIC_NUM
PROGRAM:
    Give the number that represent the comic and fetch urls of each chapter.
"""

import sys, os
import logging, requests
import downloader_class as dc
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.INFO)

USAGE = 'USAGE: comic999_chapter_url.py OUPUT_FILEPATH COMIC_NUM'

GENERAL_URL = 'https://www.999comics.com'
ENCODE = 'utf-8'

CSS_SELECTOR = 'div.chapter-list ul li a'

class Anchor():

    def __init__(self, url, title):
        self.url = url
        self.title = title

    def __str__(self):
        return 'Title: {}, URL: {}'.format(self.url, self.title)


def chapter_url():

    # Input validation
    try:
        file_class = dc.Directory(sys.argv[1])
        comic_num = sys.argv[2]
    except:
        print(USAGE)
        sys.exit(1)

    # full url --> point to homepage of the comic
    full_url = GENERAL_URL + '/comic/' + comic_num + '/'
    logging.debug(full_url)

    # Make request
    page_req = requests.get(full_url)
    try:
        page_req.raise_for_status()
    except:
        print('Request to {} failed.'.format(full_url))
        sys.exit(1)

    page_req.encoding = ENCODE
    page_soup = BeautifulSoup(page_req.text, 'html.parser')
    chapter_list = page_soup.select(CSS_SELECTOR)

    # Write file
    if os.path.isfile(file_class.abs_path):
        print('{} file already exist.'.format(file_class.abs_path))
        sys.exit(1)

    try:
        with open(file_class.abs_path, 'w') as write_file:
            for each_url, each_title in gen_url(chapter_list):
                data = Anchor(each_url, each_title)
                write_file.write('{},{}\n'.format(data.title, data.url))
    except:
        print('Failed to write data in file.')
        sys.exit(1)
    else:
        print('Write file success.')


def gen_url(li):
    """
    Generate url and title
    """
    for elem in li:
        url = GENERAL_URL + elem.get('href')
        title = elem.find('span').text
        yield (url, title)


if __name__ == '__main__':
    chapter_url()
