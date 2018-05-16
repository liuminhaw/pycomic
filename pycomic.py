"""
Program:
    Python comic downloader
Author:
    haw
"""

import sys, os



def main():

    if len(sys.argv) == 1:
        pycomic_help()
    elif sys.argv[1] == 'add':
        pycomic_add()
    elif sys.argv[1] == 'list':
        pycomic_list()
    elif sys.argv[1] == 'download':
        pycomic_download()
    elif sys.argv[1] == 'help':
        pycomic_help()
    elif sys.argv[1] == 'fetch-chapter':
        pycomic_fetch_chapter()
    elif sys.argv[1] == 'fetch-url':
        pycomic_fetch_url()
    else:
        pycomic_help()


def pycomic_help():
    message = \
    """
    USAGE:
        pycomic add COMIC-NAME NUMBER DIGITS
        pycomic download COMIC-NAME CHAPTER
        pycomic fetch-chapter COMIC-NAME CHAPTER
        pycomic fetch-url COMIC-NAME CHAPTER
        pycomic help
        pycomic list
    """
    print(message)
    sys.exit(1)


def pycomic_add():
    pass


def pycomic_list():
    pass


def pycomic_download():
    pass


def pycomic_fetch_chapter():
    pass


def pycomic_fetch_url():
    pass


if __name__ == '__main__':
    main()
