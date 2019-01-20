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
`pycomic_config.ini` config file will be create in user's home directory  
Modify `pycomic_config.ini` for custom configuration

### Version 1.3.3

##### v1.3.3 Update
- Update urllib3 version due to security reason

##### v1.3.2 Update
- Update requirements requests version due to security reason

##### v1.3.1 Update
- Remove file after fetch-url function failed

##### v1.3.0 Update
- Implement check function
- Implement uncheck function
- Showing book name when verify

##### Methods
- add
- check
- download
- fetch-chapter
- fetch-url
- help
- list
- list-chapters
- list-pdf
- list-menu
- make-pdf
- uncheck
- verify
- version

##### add
Store comic information to local.

    pycomic.py add ENGLISHNAME CHINESENAME NUMBER

##### check
Mark `COMICNAME` progression in menu file as complete

    pycomic.py check COMICNAME

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

##### uncheck
Remove the completion mark of `COMICNAME` in menu file

    pycomic.py uncheck COMICNAME

##### verify
Verify download images's integrity

    pycomic.py verify COMICNAME DIRECTORYTAG

##### version
Show current using version of the program

    pycomic.py version
