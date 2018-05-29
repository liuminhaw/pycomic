"""
Class definition for pycomic
"""

import os

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.INFO)

class Comic():

    def __init__(self, eng, ch, num):
        self.english = eng
        self.chinese = ch
        self.number = num

    def __str__(self):
        return '{} - {}: {}'.format(self.english, self.chinese, self.number)

    def def_url(self, url):
        self.url = url + self.number + '/'
        logging.debug('Comic URL: {}'.format(self.url))

    def def_menu(self, path):
        filename = self.english + '_menu.csv'
        self.menu_csv = os.path.join(path, filename)

    def def_chapter_dir(self, path):
        self.chapter_dir = os.path.join(path,self.english)

    def def_chapter(self, path, number):
        filename = self.english + '_' + number + '.csv'
        self.chapter_csv = os.path.join(path, self.english, filename)
