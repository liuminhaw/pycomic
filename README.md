# pycomic
#### Program to download and save comic to local disk
Fetching comic from **999comic** website

### Version 0.9
New **pycomic.py** program to replace the older programs

##### Methods
- add
- download
- fetch-chapter
- fetch-url
- help
- list
- list-chapters
- list-pdf
- list-menu
- make-pdf

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
List comic's chapter menu  
Show matching pattern if `PATTERN` is provided

    pycomic list-menu COMICNAME [PATTERN]

##### list-pdf
List pdf files of comic that is stored
Show matching pattern if `PATTERN` is provided

    pycomic list-pdf COMICNAME [PATTERN]

##### make-pdf
Use downloaded comic images to make pdf file
Use `pycomic list-chapters` to find `DIRECTORYTAG`

    pycomic make-pdf COMICNAME DIRECTORYTAG