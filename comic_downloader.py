"""
Download comic from a list of sites

USAGE:
    comic_downloader.py URL_FILEPATH OUTPUT_DIR [PAGENUM]
PROGRAM:
    Given a file with image urls in it, download all images of those urls
"""

import sys, os, re
import datetime, time, logging
import requests
import downloader_class as dc

# logging.basicConfig(filename='comic_result.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.INFO)

USAGE = 'USAGE: comic_downloader.py URL_FILEPATH OUTPUT_DIR [PAGENUM]'
REGEXURL = r'http([s])?(.)*(\.jpg|\.jpeg|\.png)'
HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}


class Tracker():

    def __init__(self):
        self.current = 1
        self.target = 1
        self.new = True

    def __str__(self):
        return 'Current Page: {}, Target Page: {}'.format(self.current, self.target)


def url_gen(file):
    try:
        with open(file) as read_in:
            each_line = None
            while each_line != '':
                each_line = read_in.readline()
                yield each_line
    except:
        print('Cannot open file {}'.format(file))
        sys.exit(1)


def main():
    regex = re.compile(REGEXURL)

    # Input validation
    try:
        input_path = sys.argv[1]
        output_path = dc.Directory(sys.argv[2])
    except:
        print(USAGE)
        sys.exit(1)

    # output_path = os.path.abspath(sys.argv[2])
    # output_dir = os.path.dirname(output_path)
    # output_base = os.path.basename(output_path)
    download_mode = Tracker()
    try:
        download_mode.target = int(sys.argv[3])
        download_mode.new = False
    except:
        download_mode.target = 1


    if not os.path.isdir(output_path.dir):
        print('{} does not exist.'.format(output_path.dir))
        sys.exit(1)
    try:
        os.mkdir(output_path.abs_path)
    except FileExistsError:
        if download_mode.new:
            print('{} already exist in {}'.format(output_path.base, output_path.dir))
            sys.exit(1)


    # Download images
    for each_line in url_gen(input_path):
        img_url = regex.search(each_line)
        try_times = 0

        if download_mode.current != download_mode.target:
            download_mode.current += 1
            continue

        if not img_url:
            continue
        else:
            img_url = img_url.group()

        # Create file name
        img_name = output_path.base + '-' + \
                   datetime.datetime.now().strftime('%Y%m%dT%H%M%SMS%f') + \
                   '.' + img_url.split('.')[-1]
        img_path = os.path.join(output_path.abs_path, img_name)

        while True:
            if try_times >= 10:
                logging.warning('Exceed try time limit.')
                sys.exit(1)

            try:
                img_request = requests.get(img_url, headers=HEADER)
            except:
                logging.warning('{} request no response.'.format(img_url))
                try_times += 1
                time.sleep(1)

            try:
                img_request.raise_for_status()
            except:
                logging.warning('{} request failed.'.format(img_url))
                try_times += 1
                time.sleep(1)
            else:
                with open(img_path, 'wb') as write_file:
                    for chunk in img_request.iter_content(10000):
                        write_file.write(chunk)
                    print('Write {} image success.'.format(img_name))
                time.sleep(1)
                break



if __name__ == '__main__':
    main()
