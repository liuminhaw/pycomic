"""
Class definition for pycomic
"""

import os, sys
import configparser,  pathlib
from pycomic_pkg import logging_class as logcl
from pycomic_pkg import user_agent_class as agentcl


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


class Config():

    def __init__(self, candidates):
        """
        Input:
            candidates - ini config files list
        Error Code:
            1 - No config ini file found
            3 - CONFIG section not exist
            5 - DEFAULT section not exist

            11 - Some needed key not exist in ini files
        """
        HOME = str(pathlib.Path.home())

        self.DEFAULT_SEC = 'DEFAULT'
        self.CONFIG_SEC = 'CONFIG'
        self.DEFAULT_DIR = 'pycomic'
        self.DIRECTORY = 'Directory'
        self.MENU = 'Menu'
        self.LINKS = 'Links'
        self.IMAGES = 'Images'
        self.COMICS = 'Comics'
        self.USERAGENT = 'User Agent'
        self.MAIN_MENU = 'Main Menu'

        self._config = configparser.ConfigParser()
        self._config_found = self._config.read(candidates)

        # Make sure ini file exist
        if len(self._config_found) == 0:
            logger.warning('No config file found')
            sys.exit(1)

        # Set default directory
        try:
            self._config.set(self.DEFAULT_SEC, self.DIRECTORY, os.path.join(HOME,self.DEFAULT_DIR))
        except NoSectionError:
            logger.warning('Cannot find {} section in ini files.'.format(self.DEFAULT_SEC))
            sys.exit(5)

        # Write directory option setting to file
        self._write_file()

        # Set CONFIG section
        try:
            self._config_section = self._config[self.CONFIG_SEC]
        except KeyError:
            logger.warning('Cannot find {} section in ini files.'.format(self.CONFIG_SEC))
            sys.exit(3)

        # Read CONFIG section
        self._directory = self._read_key(self.DIRECTORY)
        self._menu = self._read_key(self.MENU)
        self._links = self._read_key(self.LINKS)
        self._images = self._read_key(self.IMAGES)
        self._comics = self._read_key(self.COMICS)
        self._user_agent = self._read_key(self.USERAGENT)
        self._main_menu = self._read_key(self.MAIN_MENU)



    def useragent(self):
        user_agent = agentcl.UserAgent().random_computer()

        if len(user_agent) != 0:
            self._config.set(self.CONFIG_SEC, self.USERAGENT, user_agent)
            self._write_file()
            return user_agent
        else:
            return self._user_agent

    def directory(self):
        return self._directory

    def menu(self):
        return os.path.join(self._directory, self._menu)

    def links(self):
        return os.path.join(self._directory, self._links)

    def images(self):
        return os.path.join(self._directory, self._images)

    def comics(self):
        return os.path.join(self._directory, self._comics)

    def main_menu(self):
        return os.path.join(self._directory, self._menu, self._main_menu)

    def set_directory(self, path):
        """
        Input:
            path : String - directory path
        """
        try:
            self._config.set(self.CONFIG_SEC, self.DIRECTORY, os.path.join(path, self.DEFAULT_DIR))
        except NoSectionError:
            logger.warning('Cannot find {} section in ini files.'.format(self.CONFIG_SEC))
            sys.exit(3)

        # Save ini file
        self._write_file()


    def _read_key(self, key):
        """
        Input:
            key : String - ini file option key
        Return:
            Value of the key
        """
        value = self._config_section.get(key)
        if value is None:
            logger.warning('No {} key exist in ini files.'.format(key))
            sys.exit(11)
        return value


    def _write_file(self):
        """
        Write config settings to file
        """
        for file in self._config_found:
            with open(file, 'w') as config_file:
                self._config.write(config_file)



if __name__ == '__main__':

    # Test Config class
    config = Config(['not_exist.ini', '.pycomic.ini'])

    print(config.useragent())
    print(config.directory())
    print(config.menu())
    print(config.links())
    print(config.images())
    print(config.comics())
    print(config.main_menu())

    config.set_directory('/tmp')
