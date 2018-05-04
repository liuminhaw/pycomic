"""
Extract eyny urls to a neater file

USAGE:
    eyny_cleanurl.py URL_FILEPATH
PROGRAM:
    Given a file with a bunch of texts, extract urls in it.
    Then put these urls into a neater file.
"""

import sys, os, re
import logging
import collections, html, hashlib

# logging.basicConfig(filename='cleanurl_result.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.INFO)

USAGE = 'USAGE: eyny_cleanurl.py URL_FILEPATH'
# REGEXURL = r'img src="((http)(s)?(\S)*(\.jpg|\.jpeg|\.png))"'
REGEXURL = r'"((http)(s)?(\S)*(\.jpg|\.jpeg|\.png))"'


class Directory():

    def __init__(self, path):
        self.abs_path = os.path.abspath(path)
        self.dir = os.path.dirname(self.abs_path)
        self.base = os.path.basename(self.abs_path)

    def logging(self):
        logging.debug('abs path: {}'.format(self.abs_path))
        logging.debug('dir: {}'.format(self.dir))
        logging.debug('base: {}'.format(self.base))


def eyny_cleanurl():
    regex = re.compile(REGEXURL)

    # Input validation
    try:
        input_path = sys.argv[1]
    except:
        print(USAGE)
        sys.exit(1)

    source_dir = Directory(input_path)
    source_dir.logging()

    # Find every image urls in the file
    try:
        with open(source_dir.abs_path) as read_file:
            file_content = read_file.read()
            file_content = html.unescape(file_content)
            logging.debug('File content: {}'.format(file_content))
            urls_fetch = regex.findall(file_content)
    except:
        print('Read file {} failed.'.format(source_dir.abs_path))
        sys.exit(1)

    # URLs in ordered-dict
    url_dict = collections.OrderedDict()
    for url_group in urls_fetch:
        hash = hashlib.sha256(url_group[0].encode()).hexdigest()
        hash = hash[:10]
        url_dict[hash] = url_group[0]

    # Write urls to new file
    new_filename = os.path.join(source_dir.dir,
                   source_dir.base.split('.')[0] + '.txt')
    with open(new_filename, 'w') as write_file:
        for url in url_dict.values():
            write_file.write('{}\n'.format(url))
            print('Write {} to file {}.'.format(url, new_filename))

if __name__ == '__main__':
    eyny_cleanurl()
