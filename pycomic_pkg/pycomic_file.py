"""
Program:
    Python comic downloader - Fille type
Author:
    haw

Error Code:
    1 - Program usage error
    11 - ComicNotFoundError catch
    12 - UpdateError catch
    13 - FileNotFoundError catch
    14 - FileExistError catch
    15 - IOError catch
    16 - CSVError catch
    17 - TXTError catch
    21 - Directory exist error
    22 - Make pdf error
"""

import sys, os
import csv, shutil

from pycomic_pkg import exceptions as pycomic_err
from pycomic_pkg import url_collections as url
from pycomic_pkg import logging_class as logcl
from pycomic_pkg import pycomic_lib as pylib


SECTION = 'FILE'
LOG_DIR = os.path.join(os.getcwd(), 'log')

logger = logcl.PersonalLog('pycomic_file', LOG_DIR)


def help():
    message = \
    """
    USAGE:
        pycomic.py add ENGLISHNAME CHINESENAME
        pycomic.py convert COMICNAME
        pycomic.py download COMICNAME
        pycomic.py fetch-url COMICNAME
        pycomic.py help
        pycomic.py list [PATTERN]
        pycomic.py list-books origin|format [PATTERN]
        pycomic.py list-pdf [PATTERN]
        pycomic.py list-url [PATTERN]
        pycomic.py make-pdf COMICNAME
        pycomic.py source [file|999comics|manhuagui]
        pycomic.py state-change COMICNAME
        pycomic.py verify COMICNAME
    """

    print(message)


def add(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py add ENGLISHNAME CHINESENAME
    """

    try:
        english_name = sys.argv[2]
        chinese_name = sys.argv[3]
        book_number = '------'
        process_state = '--------'
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Check to avoid duplicated comic information
    pylib.check_menu_duplicate(pyconfig, SECTION, chinese_name, english_name)

    # Get file content from user
    print('Enter file content. Ctrl-D to save.')
    contents = []

    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    # Define Comic object
    comic = pylib.Comic(english_name, chinese_name)
    comic.file_path(pyconfig.raw(SECTION), 'raw')

    # Add data to main menu
    data = [english_name, chinese_name, book_number, process_state]
    try:
        pylib.update_menu(pyconfig.main_menu(SECTION), data)
    except pycomic_err.UpdateError:
        logger.warning('Update {} failed'.format(pyconfig.main_menu(SECTION)))
        sys.exit(12)

    logger.info('Write {} to menu csv file success'.format(data))

    # Write raw data file
    try:
        pylib.write_txt(comic.path['raw'], contents)
    except pycomic_err.TXTError as err:
        logger.warning('Error: {}'.format(err))
        logger.info('Failed to write to {}'.format(comic.path['raw']))
        sys.exit(17)
    else:
        logger.info('Write contents to {} success'.format(comic.path['raw']))


def convert(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py convert COMICNAME
    """
    try:
        comic_name = sys.argv[2]
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Find comic from menu csv file
    try:
        eng_name, ch_name, number, status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name)
    comic.file_path(pyconfig.origin(SECTION), 'origin')
    comic.file_path(pyconfig.formatted(SECTION), 'format')

    # Convert images
    try:
        os.mkdir(comic.path['format'])
    except FileExistsError:
        logger.warning('Directory {} already exist'.format(comic.path['format']))
        sys.exit(21)

    try:
        pylib.convert_images_jpg(comic.path['origin'], comic.path['format'])
    except IOError:
        logger.warning('Failed to convert {} to jpeg files'.format(comic.path['origin']))
        shutil.rmtree(comic.path['format'])
        sys.exit(15)
    else:
        logger.info('Convert {} to jpeg files success'.format(comic.path['origin']))



def download(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py download COMICNAME
    """
    try:
        comic_name = sys.argv[2]
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Find comic from menu csv file
    try:
        eng_name, ch_name, _number, _status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name)
    comic.file_path(pyconfig.origin(SECTION), 'book')
    comic.file_path(pyconfig.refine(SECTION), 'refine')

    # Download images
    try:
        os.mkdir(comic.path['book'])
    except FileExistsError:
        logger.warning('Directory {} already exist'.format(comic.path['book']))
        sys.exit(21)
    urls = url.extract_images(comic.path['refine'])
    errors = url.download_images(urls, comic.path['book'], header=pyconfig.useragent(SECTION))
    # errors = url.download_images(urls, comic.path['book'], header='Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0')

    # Show download error messages
    for error_message in errors:
        logger.info(error_message)



def fetch_url(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py fetch-url COMICNAME
    """
    try:
        comic_name = sys.argv[2]
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Find comic from menu csv file
    try:
       eng_name, ch_name, number, status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name)
    comic.file_path(pyconfig.raw(SECTION), 'raw')
    comic.file_path(pyconfig.refine(SECTION), 'refine')

    # Extract links
    urls = url.extract_images(comic.path['raw'])

    # Save links to extract file
    try:
        pylib.write_csv(comic.path['refine'], urls)
    except pycomic_err.CSVError as err:
        logger.warning('Error: {}'.format(err))
        logger.info('Failed to write to {}'.format(comic.path['refine']))
        sys.exit(16)
    else:
        logger.info('Extract file {} success'.format(eng_name))



def list(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py list [PATTERN]
    """
    try:
        pattern = sys.argv[2]
    except IndexError:
        pattern = ''

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Show all matching data
    pylib.list_menu_csv(pyconfig, SECTION, pattern)


def list_books(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py list-books origin|format [PATTERN]
    """
    _ORIGIN = 'origin'
    _FORMAT = 'format'
    source_type = ''

    try:
        source_type = sys.argv[2]
        pattern = sys.argv[3]
    except IndexError:
        pattern = ''

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Show all matching csv_data
    # pylib.list_files(pyconfig.images(SECTION), pattern)
    if source_type == _ORIGIN:
        _print_files(pylib.list_files(pyconfig.origin(SECTION), pattern))
        # pylib.list_files(pyconfig.origin(SECTION), pattern)
    elif source_type == _FORMAT:
        _print_files(pylib.list_files(pyconfig.formatted(SECTION), pattern))
        # pylib.list_files(pyconfig.format(SECTION), pattern)
    else:
        print(message)
        sys.exit(1)



def list_pdf(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py list-pdf [PATTERN]
    """
    try:
        pattern = sys.argv[2]
    except IndexError:
        pattern = ''

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Show all matching data
    _print_files(pylib.list_files(pyconfig.comics(SECTION), pattern))
    # pylib.list_files(pyconfig.comics(SECTION), pattern)


def list_url(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py list-url [PATTERN]
    """
    try:
        pattern = sys.argv[2]
    except IndexError:
        pattern = ''

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Show all matching data
    _print_files(pylib.list_files(pyconfig.refine(SECTION), pattern))
    # pylib.list_files(pyconfig.refine(SECTION), pattern)


def make_pdf(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py make-pdf COMICNAME
    """
    try:
        comic_name = sys.argv[2]
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Find comic from menu csv file
    try:
        eng_name, ch_name, number, status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name)
    comic.file_path(pyconfig.formatted(SECTION), 'books')
    comic.file_path(pyconfig.comics(SECTION), 'pdf')

    # Make pdf
    try:
        pylib.make_pdf(comic.path['books'], comic.path['pdf'])
    except FileNotFoundError:
        logger.warning('Directory {} not exist'.format(comic.path['books']))
        sys.exit(13)
    except pycomic_err.FileExistError:
        logger.info('PDF file {} already exist'.format(comic.path['pdf']))
        sys.exit(14)
    except:
        logger.warning('Failed to make pdf file from {}'.format(comic.path['books']))
        os.remove(comic.path['pdf'])
        sys.exit(22)
    else:
        logger.info('Make PDF {} success'.format(comic.path['pdf']))


def source(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py source [file|999comics|manhuagui]
    """
    if len(sys.argv) == 2:
        pylib.get_source(pyconfig)
    elif sys.argv[2] == 'file' or sys.argv[2] == '999comics' or sys.argv[2] == 'manhuagui':
        pylib.set_source(pyconfig, sys.argv[2])
    else:
        print(message)
        sys.exit(1)


def state_change(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py state-change COMICNAME
    """
    try:
        comic_name = sys.argv[2]
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Find comic from menu csv file
    try:
        eng_name, ch_name, number, status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Change comic state
    COMPLETE = 'complete'
    IN_PROGRESS = '--------'
    if status == IN_PROGRESS:
        status = COMPLETE
    else:
        status = IN_PROGRESS

    try:
        pylib.modify_menu(pyconfig.main_menu(SECTION), comic_name, status=status)
    except pycomic_err.UpdateError:
        logger.warning('Modify {} failed'.format(pyconfig.main_menu(SECTION)))
        sys.exit(12)

    # Success message
    if status == IN_PROGRESS:
        logger.info('{} marked as in progress'.format(comic_name))
    else:
        logger.info('{} marked as process complete'.format(comic_name))


def verify(pyconfig):
    message = \
    """
    USAGE:
        pycomic.py verify COMICNAME
    """
    try:
        comic_name = sys.argv[2]
    except IndexError:
        print(message)
        sys.exit(1)

    # Check directory structure
    pylib.check_structure(pyconfig, SECTION)
    _check(pyconfig, SECTION)

    # Find comic from menu csv file
    try:
        eng_name, ch_name, number, status = pylib.find_menu_comic(pyconfig, SECTION, comic_name)
    except pycomic_err.ComicNotFoundError:
        logger.info('No match to {} found'.format(comic_name))
        sys.exit(11)

    # Define comic object
    comic = pylib.Comic(eng_name, ch_name)
    comic.file_path(pyconfig.origin(SECTION), 'books')

    # Verification
    try:
        truncated = pylib.verify_images(comic.path['books'])
    except FileNotFoundError:
        logger.warning('Directory {} not exist'.format(comic.path['books']))
        sys.exit(13)

    for image in truncated:
        logger.info('Image file {} is truncated'.format(image))
    logger.info('{} verification completed'.format(comic_name))



def _check(config, sec_title):
    """
    Directory structure check for file type
    """
    # Check url/raw directory
    os.makedirs(config.raw(sec_title), exist_ok=True)
    # Check url/refind directory
    os.makedirs(config.refine(sec_title), exist_ok=True)


def _print_files(files):
    """
    Output files information to terminal
    """
    print('------ START ------')
    for index, file in files:
        print('FILE TAG {:4d} : {:>20}'.format(index, file))
    print('------- END -------')
