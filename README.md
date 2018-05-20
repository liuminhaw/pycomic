# pycomic
#### Program to download and save comic to local disk
Fetching comic from **999comic** website

### Version 0.2
Give the number that represent the comic and fetch URL of each chapter

    comic999_chapter_url.py OUTPUTFILEPATH COMICNUMBER

Give an url of comic, scrape through and get URLs of each page image.
Add optional PAGENUM to specify the starting page.

    comic999_url.py SITEURL OUTPUTFILEPATH [PAGENUM]

Given a file with URLs in it, download all images of those URLs
Add optional PAGENUM to specify the starting page.

    comic_downloader.py URLFILEPATH OUTPUTDIR [PAGENUM]
