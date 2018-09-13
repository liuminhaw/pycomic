"""
Class definition for pycomic
"""

import os, sys
import configparser,  pathlib
import csv
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
        # self.HOME = str(pathlib.Path.home())

        self.DEFAULT_SEC = 'DEFAULT'
        self.CONFIG_SEC = 'CONFIG'
        self.TYPE_SEC = 'TYPE'

        self.SOURCE = 'source'

        self.DEFAULT_DIR = 'pycomic'
        self.DIRECTORY = 'Directory'
        self.MENU = 'Menu'
        self.LINKS = 'Links'
        self.IMAGES = 'Images'
        self.COMICS = 'Comics'
        self.USERAGENT = 'User Agent'
        self.MAIN_MENU = 'Main Menu'

        # For source type - file
        self.RAW = 'raw'
        self.REFINE = 'refine'


        # Get config information
        self._config = configparser.ConfigParser()
        self._config_found = self._config.read(candidates)

        # Make sure ini file exist
        if len(self._config_found) == 0:
            logger.warning('No config file found')
            sys.exit(1)


    def useragent(self, section_title):
        config_section = self._read_section(section_title)
        user_agent = agentcl.UserAgent().random_computer()

        if len(user_agent) != 0:
            self._config.set(section_title, self.USERAGENT, user_agent)
            self._write_file()
            return user_agent
        else:
            return self._read_key(config_section, self.USERAGENT)

    def directory(self, section_title):
        config_section = self._read_section(section_title)
        self._read_config(config_section)
        return self._directory

    def menu(self, section_title):
        config_section = self._read_section(section_title)
        self._read_config(config_section)
        return os.path.join(self._directory, self._menu)

    def links(self, section_title):
        config_section = self._read_section(section_title)
        self._read_config(config_section)
        return os.path.join(self._directory, self._links)

    def images(self, section_title):
        config_section = self._read_section(section_title)
        self._read_config(config_section)
        return os.path.join(self._directory, self._images)

    def comics(self, section_title):
        config_section = self._read_section(section_title)
        self._read_config(config_section)
        return os.path.join(self._directory, self._comics)

    def main_menu(self, section_title):
        config_section = self._read_section(section_title)
        self._read_config(config_section)
        return os.path.join(self._directory, self._menu, self._main_menu)

    def raw(self, section_title):
        config_section = self._read_section(section_title)
        self._read_config(config_section)
        return os.path.join(self._directory, self._links, self._raw)

    def refine(self, section_title):
        config_section = self._read_section(section_title)
        self._read_config(config_section)
        return os.path.join(self._directory, self._links, self._refine)

    def source(self):
        type_section = self._read_section(self.TYPE_SEC)
        return self._read_key(type_section, self.SOURCE)




    def _read_config(self, section):
        self._directory = self._read_key(section, self.DIRECTORY)
        self._menu = self._read_key(section, self.MENU)
        self._links = self._read_key(section, self.LINKS)
        self._images = self._read_key(section, self.IMAGES)
        self._comics = self._read_key(section, self.COMICS)
        self._user_agent = self._read_key(section, self.USERAGENT)
        self._main_menu = self._read_key(section, self.MAIN_MENU)

        self._raw = self._read_key(section, self.RAW)
        self._refine = self._read_key(section, self.REFINE)



    def _read_section(self, name):
        """
        Read section in .ini files and return the read object
        Input:
            name - section name
        Return:
            Configuration section object
        """
        try:
            section = self._config[name]
        except:
            logger.warning('Cannot find {} section in .ini files.'.format(name))
            sys.exit(3)
        else:
            return section


    def _read_key(self, section, key):
        """
        Input:
            section - Config file section
            key : String - ini file option key
        Return:
            Value of the key - If key exist
            None - If key not exist
        """
        value = section.get(key)

        # if value is None:
            # raise NoOptionError('No {} exist in {} section'.format(key, section))

        return value
        # if value is None:
            # logger.warning('No {} key exist in ini files.'.format(key))
            # sys.exit(11)
        # else:
            # return value


    def _write_file(self):
        """
        Write config settings to file
        """
        for file in self._config_found:
            with open(file, 'w') as config_file:
                self._config.write(config_file)



def check_structure(config, sec_title):
    """
    Initial check for directory structure
    """
    # Check menu directory
    os.makedirs(config.menu(sec_title), exist_ok=True)
    # Check url directory
    os.makedirs(config.links(sec_title), exist_ok=True)
    # Check books directory
    os.makedirs(config.images(sec_title), exist_ok=True)
    # Check pdf directory
    os.makedirs(config.comics(sec_title), exist_ok=True)

    if not os.path.exists(config.main_menu(sec_title)):
        file = open(config.main_menu(sec_title), mode='wt', encoding='utf-8')
        file.close()


def check_menu_duplicate(config, sec_title, ch_name, eng_name, number=None):
    """
    Check data in menu file to avoid information duplication
    """
    with open(config.main_menu(sec_title), mode='rt', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        for index, data in enumerate(csv_reader):
            # English name duplication
            if eng_name in data:
                logger.info('Line {}: {} in {}'.format(index+1, eng_name, data))
                sys.exit(103)
            # Chinese name duplication
            if ch_name in data:
                logger.info('Line {}: {} in {}'.format(index+1, ch_name, data))
                sys.exit(103)
            # Number duplication
            if number in data:
                logger.info('Line {}: {} in {}'.format(index+1, number, data))
                sys.exit(103)


def write_menu_csv(config, sec_title, data):
    """
    Write new data to menu csv file

    Parameters:
        data - tuple
    """
    with open(config.main_menu(sec_title), mode='at', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data)



if __name__ == '__main__':

    # Test Config class
    config = Config(['not_exist.ini', '../pycomic_template.ini'])

    print(config.useragent())
    print(config.directory())
    print(config.menu())
    print(config.links())
    print(config.images())
    print(config.comics())
    print(config.main_menu())
    print(config.raw())
    print(config.refine())

    print(config.source())
