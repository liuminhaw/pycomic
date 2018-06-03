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


### In Development
New **pycomic.py** program to replace the older programs

##### Methods
- add
- download
- fetch-chapter
- fetch-url
- help
- list
- list-chapters
- list-menu

##### add
Store comic information to local.

    pycomic add ENGLISHNAME CHINESENAME NUMBER

##### download
Download comic
Use `pycomic list-url` command to get `FILETAG`

    pycomic download COMICNAME FILETAG

##### fetch-chapter
Store chapter link of comic to local

    pycomic fetch-chapter COMICNAME

##### fetch-url
Store each image link of comic to local  
Use `pycomic list-menu` to find `IDENTITYNUM`

    pycomic fetch-url COMICNAME IDENTITYNUM

##### help
Show available command options

    pycomic help

##### list
List stored comics  
Optional `PATTERN` search for matching

    pycomic list [PATTERN]

##### list-chapters
List chapters that are stored in local  
Show matching pattern if `PATTERN` is provided

    pycomic list-chapter COMICNAME [PATTERN]


##### list-menu
List comic's chapter menu (Find `IDENTITYNUM` using `fetch-url`)  
Show matching pattern if `PATTERN` is provided

    pycomic list-menu COMICNAME [PATTERN]
