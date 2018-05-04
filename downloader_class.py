"""
Classes use in Comic Download program
"""

import os
import logging


class Directory():

    def __init__(self, path):
        self.abs_path = os.path.abspath(path)
        self.dir = os.path.dirname(self.abs_path)
        self.base = os.path.basename(self.abs_path)

    def logging(self):
        logging.debug('abs path: {}'.format(self.abs_path))
        logging.debug('dir: {}'.format(self.dir))
        logging.debug('base: {}'.format(self.base))
