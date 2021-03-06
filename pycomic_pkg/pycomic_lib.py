"""
Class definition for pycomic program

Author:
    haw

Error Code:
    103 - Menu data duplication error
"""

import os, sys
import random
import configparser,  pathlib
import csv, re, shutil
import datetime, time
import requests

from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pycomic_pkg import exceptions as pycomic_err
from pycomic_pkg import logging_class as logcl
from pycomic_pkg import user_agent_class as agentcl


logger = logcl.PersonalLog('pycomic_class')

class Comic():

    def __init__(self, english, chinese, number=''):
        self.english = english
        self.chinese = chinese
        self.number = number
        self.path = dict()

        self.chapter_title = ''
        # self.url = ''
        # self.total_pages = 0

    def __str__(self):
        return '{} - {}: {}'.format(self.english, self.chinese, self.number)

    # def def_url(self, url):
    #     self.url = url + self.number + '/'
    #     logger.debug('Comic URL: {}'.format(self.url))
    #
    # def def_menu(self, path):
    #     filename = self.english + '_menu.csv'
    #     self.menu_csv = os.path.join(path, filename)
    #
    # # pycomic/url
    # def def_chapter_dir(self, path):
    #     self.chapter_dir = os.path.join(path,self.english)
    #
    # def def_chapter(self, path, chapter):
    #     filename = self.english + '_' + chapter + '.csv'
    #     self.chapter_csv = os.path.join(path, self.english, filename)
    #
    # # pycomic/books
    # def def_book_dir(self, path):
    #     self.book_dir = os.path.join(path, self.english)
    #
    # def def_book(self, path, name):
    #     self.book = os.path.join(path, self.english, name)
    #
    # # pycomic/pdf
    # def def_pdf_dir(self, path):
    #     self.pdf_dir = os.path.join(path, self.english)
    #
    # def def_pdf(self, path, name):
    #     filename = name + '.pdf'
    #     self.pdf = os.path.join(path, self.english, filename)

    def file_path(self, path, key, name=None, extension=''):
        if name:
            name += extension
            self.path[key] = os.path.join(path, self.english, name)
        else:
            name = self.english + extension
            self.path[key] = os.path.join(path, name)

    def comic_site(self, url, key):
        self.path[key] = url + self.number + '/'



class Driver():

    class DriverError(Exception):
        """
        Raise when selenium problem occurs
        """
        pass

    def __init__(self, title, url):
        # self.driver = webdriver.Firefox()
        options = Options()
        options.set_headless(True)
        self.driver = webdriver.Chrome(options=options)

        self.chapter_title = title
        self.chapter_url = url
        self.total_pages = 0

    def get(self):
        """
        Open url page on driver
        """
        self.driver.get(self.chapter_url)

    def find_last_page(self, last_page_selector):
        """
        Find last page value

        Error:
            DriverError - Failed to get last page value
        """
        regex = re.compile(r'\d{1,3}')
        element = self.driver.find_element_by_css_selector(last_page_selector)

        try:
            self.total_pages = int(regex.search(element.text).group())
        except Exception as err:
            raise self.DriverError(err)

    def get_urls(self, image_id, next_page_selector, error_text='URL error occurs'):
        """
        All image urls
        """
        self.urls = []

        for counter in range(self.total_pages):
            for _ in range(5):
                try:
                    url = self._comic_image_url(image_id)
                    print('Page {} url {}'.format(counter, url))
                except self.DriverError:
                    self.driver.refresh()
                    continue
                else:
                    # next_page = self.driver.find_element_by_id(next_page_selector)
                    # next_page.click()
                    break
            else:
                url = error_text
                print('Page {} {}'.format(counter, url))

            self.urls.append(url)
            next_page = self.driver.find_element_by_id(next_page_selector)
            time.sleep(random.uniform(2, 3.5))
            next_page.click()

        self.driver.close()


    def page_source(self, js_execute=''):
        """
        Recent page html source code
        """
        if js_execute != '':
            self.driver.execute_script(js_execute)
        
        self.html = self.driver.page_source
        self.driver.close()


    def _comic_image_url(self, image_id):
        source, tag = 'src', 'img'

        try:
            element = self.driver.find_element_by_id(image_id)
            webpage = element.get_attribute(source)
            self.driver.execute_script("window.open('{page}');".format(page=webpage))
            time.sleep(1.2)
            self.driver.switch_to.window(self.driver.window_handles[1])
            image_tag = self.driver.find_element_by_tag_name(tag)
            image_url = image_tag.get_attribute(source)
        except Exception as err:
            raise self.DriverError(err)
        finally:
            for handle in self.driver.window_handles[1:]:
                self.driver.switch_to.window(handle)
                self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        return image_url



class Config():

    def __init__(self, candidates):
        """
        Input:
            candidates - ini config files list
        Error Code:
            1 - No config ini file found >> pycomic_err.ConfigNotFoundError
            3 - CONFIG section not exist >> configparser.NoSectionError
            5 - DEFAULT section not exist

            11 - Some needed key not exist in ini files
        """
        # self.HOME = str(pathlib.Path.home())

        self.DEFAULT_SEC = 'DEFAULT'
        self.CONFIG_SEC = 'CONFIG'
        self.TYPE_SEC = 'TYPE'

        self.SOURCE = 'source'

        self.DEFAULT_DIR = 'pycomic'
        self.HOME_URL = 'Home-url'
        self.SITE_URL = 'Site-url'
        self.ERROR_URL = 'error-url'
        self.DIRECTORY = 'Directory'
        self.MENU = 'Menu'
        self.LINKS = 'Links'
        self.IMAGES = 'Images'
        self.COMICS = 'Comics'
        self.USERAGENT = 'User-Agent'
        self.MAIN_MENU = 'Main-Menu'
        self.ORIGINAL = 'origin'
        self.FORMAT = 'format'

        # For source type - file
        self.RAW = 'raw'
        self.REFINE = 'refine'


        # Get config information
        self._config = configparser.ConfigParser()
        self._config_found = self._config.read(candidates)

        # Make sure ini file exist
        if len(self._config_found) == 0:
            logger.warning('No config file found')
            raise pycomic_err.ConfigNotFoundError()
            #sys.exit(1)


    def useragent(self, section):
        """
        Return config USERAGENT option in section 
        """
        user_agent = agentcl.UserAgent().random_computer()

        if len(user_agent) != 0:
            self._config.set(section, self.USERAGENT, user_agent)
            self._write_file()
            return user_agent
        else:
            return self._read_value(section, self.USERAGENT)

    def home_url(self, section):
        """
        Return config HOME_URL option in section 
        """
        return self._read_value(section, self.HOME_URL)

    def site_url(self, section):
        """
        Return config SITE_URL option in section 
        """
        return self._read_value(section, self.SITE_URL)

    def error_url(self, section):
        """
        Return config SITE_URL option in section 
        """
        return self._read_value(section, self.ERROR_URL)

    def directory(self, section):
        """
        Return config DIRECTORY option in section 
        """
        return self._read_value(section, self.DIRECTORY)

    def menu(self, section):
        """
        Return menu directory of configuration 
        """
        _directory = self._read_value(section, self.DIRECTORY)
        _menu = self._read_value(section, self.MENU)
        return os.path.join(_directory, _menu)

    def links(self, section):
        """
        Return url direcotry of configuration
        """
        _directory = self._read_value(section, self.DIRECTORY)
        _links = self._read_value(section, self.LINKS)
        return os.path.join(_directory, _links)

    def images(self, section):
        """
        Return books directory of configuration
        """
        _directory = self._read_value(section, self.DIRECTORY)
        _images = self._read_value(section, self.IMAGES)
        return os.path.join(_directory, _images)

    def comics(self, section):
        """
        Return pdf directory of configuration
        """
        _directory = self._read_value(section, self.DIRECTORY)
        _comics = self._read_value(section, self.COMICS)
        return os.path.join(_directory, _comics)

    def main_menu(self, section):
        """
        Return main menu.csv file path 
        """
        _directory = self._read_value(section, self.DIRECTORY)
        _menu = self._read_value(section, self.MENU)
        _main_menu = self._read_value(section, self.MAIN_MENU)
        return os.path.join(_directory, _menu, _main_menu)

    def origin(self, section):
        """
        Return origin books directory of configuration
        """
        _directory = self._read_value(section, self.DIRECTORY)
        _images = self._read_value(section, self.IMAGES)
        _original = self._read_value(section, self.ORIGINAL)
        return os.path.join(_directory, _images, _original)

    def formatted(self, section):
        """
        Return formatted books directory of configuration
        """
        _directory = self._read_value(section, self.DIRECTORY)
        _images = self._read_value(section, self.IMAGES)
        _format = self._read_value(section, self.FORMAT)
        return os.path.join(_directory, _images, _format)

    def raw(self, section):
        """
        Return raw url directory of configuration
        """
        _directory = self._read_value(section, self.DIRECTORY)
        _links = self._read_value(section, self.LINKS)
        _raw = self._read_value(section, self.RAW)
        return os.path.join(_directory, _links, _raw)

    def refine(self, section):
        """
        Return refine url directory of configuration
        """
        _directory = self._read_value(section, self.DIRECTORY)
        _links = self._read_value(section, self.LINKS)
        _refine = self._read_value(section, self.REFINE)
        return os.path.join(_directory, _links, _refine)

    def source(self, source=None):
        """
        source argument = None:
            Return current source of configuration
        source argument given:
            Set configuration source to source argument
        """

        if source:
            self._config.set(self.TYPE_SEC, self.SOURCE, source)
            self._write_file()
        else:
            return self._read_value(self.TYPE_SEC, self.SOURCE)

    def config_test(self, section, output=False):
        """
        Check config file to validate settings
        Error:
            pycomic_err.NoSectionError - Section not found
            pycomic_err.NoOptionError - Option not found
        """
        if output:
            print('Source: {}'.format(self.source()))
            print('Section: {}\n'.format(section))

            print('- user-agent: {}'.format(self.useragent(section)))
            print('- home-url: {}'.format(self.home_url(section)))
            print('- site-url: {}'.format(self.site_url(section)))
            print('- error-url: {}'.format(self.error_url(section)))
            print('- directory: {}'.format(self.directory(section)))
            print('- menu: {}'.format(self.menu(section)))
            print('- links: {}'.format(self.links(section)))
            print('- images: {}'.format(self.images(section)))
            print('- comics: {}'.format(self.comics(section)))
            print('- main-menu: {}'.format(self.main_menu(section)))
            print('- origin: {}'.format(self.origin(section)))
            print('- formatted: {}'.format(self.formatted(section)))
            print('- raw: {}'.format(self.raw(section)))
            print('- refine: {}\n'.format(self.refine(section)))
        else:
            self.source()
            self.useragent(section)
            self.home_url(section)
            self.site_url(section)
            self.error_url(section)
            self.directory(section)
            self.menu(section)
            self.links(section)
            self.images(section)
            self.comics(section)
            self.main_menu(section)
            self.origin(section)
            self.formatted(section)
            self.raw(section)
            self.refine(section)


    def _read_value(self, section, key):
        """
        Get the value of key inside section
        Input:
            section - config file section
            key - config file option
        Return:
            key value
        Error:
            pycomic_err.NoSectionError - Section not found
            pycomic_err.NoOptionError - Option not found
        """
        try:
            _config_value = self._config.get(section,key)
        except configparser.NoSectionError:
            logger.info('Section {} not found in config file'.format(section))
            raise pycomic_err.NoSectionError
        except configparser.NoOptionError:
            logger.info('Option {} not found in config file of section {}'.format(key, section))
            raise pycomic_err.NoOptionError
        else:
            return _config_value


    def _write_file(self):
        """
        Write config settings to file
        """
        for file in self._config_found:
            with open(file, 'w') as config_file:
                self._config.write(config_file)


class UserConfig():
    """
    Error Code:
        1 - No config file in candidates found
        3 - CONFIG section not found
        11 - EYNY section username not set
        13 - EYNY section password not set
    """

    def __init__(self, candidates):
        """
        Input:
            candidates - ini config files list
        """

        # Get config information
        self._config = configparser.ConfigParser()
        self._config_found = self._config.read(candidates)

        # Make sure candidates file existed
        if len(self._config_found) == 0:
            logger.warning('No user config file found')
            # TODO: Better if throw exception
            sys.exit(1)

    def eyny_info(self):
        """
        Usage:
            Read EYNY section and return user information
        Return:
            Tuple: (username, password)
        """
        # Get section
        try: 
            section = self._config['EYNY']
        except:
            logger.warning('Cannot find EYNY section in config files')
            # TODO: Better if throw exception
            sys.exit(3)
        
        # Fetch information
        username = section.get('username')
        password = section.get('password')

        # Test username and password value
        if len(username) == 0:
            logger.info('EYNY username not set')
            # TODO: Better if throw exception
            sys.exit(11)

        if len(password) == 0:
            logger.info('EYNY password not set')
            # TODO: Better if throw exception
            sys.exit(13)

        return (username, password)



##### Functions #####


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

    # Check origin directory in books directory
    os.makedirs(config.origin(sec_title), exist_ok=True)
    # Check jpeg directory in books directory
    os.makedirs(config.formatted(sec_title), exist_ok=True)

    if not os.path.exists(config.main_menu(sec_title)):
        file = open(config.main_menu(sec_title), mode='wt', encoding='utf-8')
        file.close()


def check_menu_duplicate(config, sec_title, ch_name, eng_name, number=None):
    """
    Check data in menu file to avoid information duplication

    Error Code:
        103 - Information duplication in menu csv file
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


def write_csv(path, data, index=True):
    """
    Write data to csv file

    Parameters:
        data - Iterable
    Error:
        CSVError - Failed to write csv
    """
    try:
        with open(path, mode='wt', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            if index:
                [csv_writer.writerow((index, item)) for index, item in enumerate(data)]
            else:
                [csv_writer.writerow(item) for item in data]
    except Exception as err:
        raise pycomic_err.CSVError(err)


def append_csv(path, data):
    """
    Append data to csv file

    Parameters:
        data - Iterable
    Error:
    CSVError - Failed to append csv
    """
    try:
        with open(path, mode='at', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data)
    except Exception as err:
        raise pycomic_err.CSVError(err)


def read_csv(path):
    """
    Read data from path of csv file

    Return:
        List of read data
    Error:
        CSVError - Failed to read csv
    """
    contents = []

    try:
        with open(path, mode='rt', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for data in csv_reader:
                contents.append(data)
    except Exception as err:
        raise pycomic_err.CSVError(err)

    return contents


def write_txt(path, data):
    """
    Write data to text file

    Parameters:
        data - Iterable
    Error:
        TXTError - Failed to write txt file
    """
    try:
        with open(path, mode='wt', encoding='utf-8') as file:
            file.writelines('{}\n'.format(content) for content in data)
    except Exception as err:
        raise pycomic_err.TXTError(err)


def append_txt(path, data):
    """
    Append data to text file

    Parameter:
        data - iterable
    Error:
        TXTError - Failed to append to txt file
    """
    try:
        with open(path, mode='at', encoding='utf-8') as file:
            file.writelines('{}\n'.format(content) for content in data)
    except Exception as err:
        raise pycomic_err.TXTError(err)


def index_data(path, target_index, file=True):
    """
    file is True:
        Return the index-th row of a csv file
    file is False:
        Return the index-th file in a directory

    Return:
        String of the matching index
    Error:
        CSVError - read_csv function failed
        DataIndexError - Failed to find matching index
    """
    if file:
        contents = read_csv(path)
        for index, data in enumerate(contents):
            if target_index == index:
                return data
    else:
        contents = list_files(path, '')
        for index, data in contents:
            if target_index == index:
                return data

    raise pycomic_err.DataIndexError


def list_menu_csv(config, sec_title, pattern):
    """
    List contents in menu csv file which match the pattern
    """
    print('------ START ------')
    re_pattern = re.compile(r'.*{}.*'.format(pattern), re.IGNORECASE)

    with open(config.main_menu(sec_title), mode='rt', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for data in csv_reader:
            # Assign value from read data
            eng_name = data[0]
            ch_name = data[1]
            number = data[2]
            status = data[3]

            # Search for matching pattern
            if re_pattern.search(eng_name) or re_pattern.search(ch_name):
                print('{:6} : {:20} {:10} {:10}'.format(number, eng_name, status, ch_name))

    print('------- END -------')


def list_files(directory, pattern):
    """
    Obtain files in directory that matches the pattern

    Return:
        Sorted list of files in directory
    """
    # Get files in directory
    re_pattern = re.compile(r'.*{}.*'.format(pattern), re.IGNORECASE)
    matched_files = []

    os.makedirs(directory, exist_ok=True)
    files = os.listdir(directory)
    files.sort()

    # Find and return matching files
    for index, file in enumerate(files):
        if re_pattern.search(file):
            matched_files.append((index, file))

    return matched_files

    # Search for matching result
    # print('------ START ------')
    # for index, file in enumerate(files):
    #     if re_pattern.search(file):
    #         print('FILE TAG {:4d} : {:>20}'.format(index, file))
    # print('------- END -------')


def list_file_content(path, pattern, target_index=1):
    """
    List each line of file's content that match the pattern

    Parameter:
        path - File to be read
    Return:
        List of matching data
    Error:
        CSVError - read_csv function failed
    """
    re_pattern = re.compile(r'.*{}.*'.format(pattern))
    matched_contents = []
    # last_update, comic_state = '', ''

    # Read file
    file_contents = read_csv(path)

    # Find and return matching contents
    for index, content in enumerate(file_contents):
        if re_pattern.search(content[target_index]) != None:
            matched_contents.append((index, content))

    return matched_contents

    # Search for matching result
    # print('------ START ------')
    # for index, content in enumerate(file_contents):
    #     if re_pattern.search(content[1]) != None:
    #         last_update, comic_state = content[2], content[3]
    #         print('Identity Number {:4d} : {}'.format(index, content[0]))
    #
    # print('------ INFO -------')
    # print('Last Update: {}'.format(last_update))
    # print('Comic State: {}'.format(comic_state))
    # print('------- END -------')



def find_menu_comic(config, sec_title, comic_name):
    """
    Finding comic in menu csv file

    Exist: Return tuple of found data
    Not Exist: Raise ComicNotFoundError
    """
    # Search for comic name in menu csv file
    with open(config.main_menu(sec_title), mode='rt', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for data in csv_reader:
            if comic_name.lower() in map(str.lower, data):
                return data

    # No match found, raise ComicNotFoundError
    raise pycomic_err.ComicNotFoundError


def update_menu(path, data):
    """
    Update menu csv file when with data

    Error:
        Raise UpdateError if writing new file failed
    """
    # Make backup before update
    bkp_path = path + '.bkp'
    shutil.copyfile(path, bkp_path)

    try:
        csv_data = read_csv(path)
        csv_data.insert(0, data)
        write_csv(path, csv_data, index=False)
    except:
        shutil.copyfile(bkp_path, path)
        raise pycomic_err.UpdateError
    else:
        os.remove(bkp_path)


def modify_menu(path, target, eng_name=None, ch_name=None, number=None, status=None):
    """
    Modify menu csv data with given value

    Error:
        Raise UpdateError if writing new file failed
    """
    # Make backup before update
    bkp_path = path + '.bkp'
    shutil.copyfile(path, bkp_path)

    csv_data_new = []
    csv_data = read_csv(path)
    for data in csv_data:
        if target.lower() in map(str.lower, data):
            if eng_name:
                data[0] = eng_name
            if ch_name:
                data[1] = ch_name
            if number:
                data[2] = number
            if status:
                data[3] = status
        csv_data_new.append(data)

    try:
        write_csv(path, csv_data_new, index=False)
    except:
        shutil.copyfile(bkp_path, path)
        raise pycomic_err.UpdateError
    else:
        os.remove(bkp_path)


def verify_images(path):
    """
    Images validation within path directory

    Return:
        List of truncated images
    Error:
        Raise FileNotFoundError if path does not exist
    """
    truncated_images = []
    images = os.listdir(path)
    images.sort()

    for image in images:
        try:
            img = Image.open(os.path.join(path, image))
        except OSError:
            truncated_images.append(os.path.join(path, image))
            continue

        try:
            img.load()
        except IOError:
            truncated_images.append(os.path.join(path, image))
        finally:
            img.close()

    return truncated_images


def make_pdf(input_dir, output_path):
    """
    Produce pdf file output_path using images in input_dir

    pycomic_err.FileExistError:
        Raise if file already exist
    FileNotFoundError:
        Raise if path does not exist
    """
    if os.path.isfile(output_path):
        raise pycomic_err.FileExistError

    pages = []
    images = os.listdir(input_dir)
    images.sort()

    for image in images:
        pages.append(Image.open(os.path.join(input_dir, image)))
    pages[0].save(output_path, 'PDF', resolution=100, save_all=True, append_images=pages[1:])


def convert_images_jpg(input_dir, output_dir):
    """
    Convert images in input_dir to jpeg file format and save to output_dir

    Error:
        Raise IOError with truncated images
    """
    images = os.listdir(input_dir)
    images.sort()

    for image in images:
        img = Image.open(os.path.join(input_dir, image))
        file = os.path.join(output_dir, datetime.datetime.now().strftime('%Y%m%dT%H%M%SMS%f'))
        img.convert('RGB').save(file, 'JPEG')


def request_page(page_url):
    """
    Request and parse page_url

    Return:
        BeautifulSoup parsed object
    Error:
        requests.exceptions.HTTPError - Request failed
    """
    page_req = requests.get(page_url)
    page_req.raise_for_status()
    page_req.encoding = 'utf-8'

    return BeautifulSoup(page_req.text, 'html.parser')


def get_source(config):
    """
    Get config file source value
    """
    print(config.source())


def set_source(config, source_type):
    """
    Change config file source
    """
    config.source(source_type)


# if __name__ == '__main__':

    # Test Config class
    # config = Config(['not_exist.ini', '../pycomic_template.ini'])

    # print(config.useragent())
    # print(config.directory())
    # print(config.menu())
    # print(config.links())
    # print(config.images())
    # print(config.comics())
    # print(config.main_menu())
    # print(config.raw())
    # print(config.refine())

    # print(config.source())