"""
Class definition for pycomic
"""

import os, sys
import configparser,  pathlib
import logging_class as logcl
import user_agent_class as agentcl


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
            3 - CONFIG section not exist
            5 - DEFAULT section not exist

            11 - Some needed key not exist in ini files
        """
        HOME = str(pathlib.Path.home())

        config = configparser.ConfigParser()
        config_found = config.read(candidates)

        # Set default directory
        try:
            config.set('DEFAULT', 'directory', os.path.join(HOME,'pycomic'))
        except NoSectionError:
            logger.warning('Cannot find DEFAULT section in ini files.')
            sys.exit(5)

        # Write directory option setting to file
        for file in config_found:
            with open(file, 'w') as config_file:
                config.write(config_file)

        config = configparser.ConfigParser()
        config_found = config.read(candidates)

        # Set CONFIG section
        try:
            self._config = config['CONFIG']
        except KeyError:
            logger.warning('Cannot find CONFIG section in ini files.')
            sys.exit(3)

        # Read CONFIG section
        self._directory = self._read_key('directory')
        self._menu = self._read_key('menu')
        self._links = self._read_key('links')
        self._images = self._read_key('images')
        self._comics = self._read_key('comics')
        self._user_agent = self._read_key('useragent')



    def useragent(self):
        user_agent = agentcl.UserAgent().random_computer()

        if len(user_agent) != 0:
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

    def _read_key(self, key):
        """
        Input:
            key : String - ini file option key
        Return:
            Value of the key
        """
        value = self._config.get(key)
        if value is None:
            logger.warning('No {} key exist in ini files.'.format(key))
            sys.exit(11)
        return value



if __name__ == '__main__':

    # Test Config class
    config = Config(['.pycomic.ini'])

    print(config.useragent())
    print(config.directory())
    print(config.menu())
    print(config.links())
    print(config.images())
    print(config.comics())
