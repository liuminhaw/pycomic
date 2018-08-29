# pycomic
#### Program to download and save comic to local disk
Fetching comic from **999comic** website

#### Additional Requirement
`geckodriver` need to be installed before program can be run

#### Setup
Run `setup.sh` script to setup program for use  
`DESTINATION` is where you want to put all the comics data

    ./setup.sh DESTINATION

#### Configuration
`.pycomic.ini` config file will be create in user's home directory  
Modify `.pycomic.ini` for custom configuration

### Version 1.2.0
- pycomic localize
- Update setup script

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
- verify

##### add
Store comic information to local.

    pycomic.py add ENGLISHNAME CHINESENAME NUMBER

##### download
Download comic
Use `pycomic list-url` command to get `FILETAG`

    pycomic.py download COMICNAME FILETAG

##### fetch-chapter
Store chapter link of comic to local

    pycomic.py fetch-chapter COMICNAME

##### fetch-url
Store each image link of comic to local  
Use `pycomic list-menu` to find `IDENTITYNUM`

    pycomic.py fetch-url COMICNAME IDENTITYNUM

##### help
Show available command options

    pycomic.py help

##### list
List stored comics  
Optional `PATTERN` search for matching

    pycomic.py list [PATTERN]

##### list-chapters
List chapters that are stored in local  
Show matching pattern if `PATTERN` is provided

    pycomic.py list-chapter COMICNAME [PATTERN]

##### list-menu
List comic's chapter menu  
Show matching pattern if `PATTERN` is provided

    pycomic.py list-menu COMICNAME [PATTERN]

##### list-pdf
List pdf files of comic that is stored  
Show matching pattern if `PATTERN` is provided

    pycomic.py list-pdf COMICNAME [PATTERN]

##### make-pdf
Use downloaded comic images to make pdf file  
Use `pycomic list-chapters` to find `DIRECTORYTAG`

    pycomic.py make-pdf COMICNAME DIRECTORYTAG

##### verify
Verify download images's integrity

    pycomic.py verify COMICNAME DIRECTORYTAG
