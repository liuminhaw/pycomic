"""
Class definition for pycomic
"""

import os
import logging_class as logcl


logger = logcl.PersonalLog('pycomic_class')

class Comic():

    def __init__(self, eng, ch, num):
        self.english = eng
        self.chinese = ch
        self.number = num

    def __str__(self):
        return '{} - {}: {}'.format(self.english, self.chinese, self.number)

    def def_url(self, url):
        self.url = url + self.number + '/'
        logger.debug('Comic URL: {}'.format(self.url))

    def def_menu(self, path):
        filename = self.english + '_menu.csv'
        self.menu_csv = os.path.join(path, filename)

    # pycomic/url
    def def_chapter_dir(self, path):
        self.chapter_dir = os.path.join(path,self.english)

    def def_chapter(self, path, chapter):
        filename = self.english + '_' + chapter + '.csv'
        self.chapter_csv = os.path.join(path, self.english, filename)

    # pycomic/books
    def def_book_dir(self, path):
        self.book_dir = os.path.join(path, self.english)

    def def_book(self, path, name):
        self.book = os.path.join(path, self.english, name)

    # pycomic/pdf
    def def_pdf_dir(self, path):
        self.pdf_dir = os.path.join(path, self.english)

    def def_pdf(self, path, name):
        filename = name + '.pdf'
        self.pdf = os.path.join(path, self.english, filename)
