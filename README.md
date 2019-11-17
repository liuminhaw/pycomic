# pycomic
#### Program to download and save comic to local disk
Fetching comic from multiple sources

#### Additional Requirement
selenium `chromedriver` need to be installed before program can be run  
(Use automated chrome to run the program)

#### Setup
Run `setup.sh` script to setup program for use  
`DESTINATION` is where you want to put all the comics data

    ./setup.sh DESTINATION

#### Configuration
`pycomic_config.ini` config file will be created in destination directory  
Modify `pycomic_config.ini` for custom configuration

`user_config.ini` config file will be created in destination directory  
Set username and password in `user_config.ini` for auto-login 

### Version 2.1.2
- Automatically show page source tab
- Prevent setup script from overiding user config file 

**Version 2.1.1**
- Eyny site log out after function complete
- Fix file type `change-state` problem

**Version 2.1.0**
- File new function: eyny-download
- Add user config file for sites auto-login

**Version 2.0.0**
- New program structure
- Multiple sources type
  - file
  - 999comics
  - manhuagui

---

#### Type File
- add
- convert
- download
- fetch-url
- help
- list
- list-books
- list-pdf
- list-url
- make-pdf
- state-change
- verify  
- version  
==================
- eyny-download

##### add
Store comic title information to local.

    pycomic.py add ENGLISHNAME CHINESENAME

##### convert
Convert image files into `jpeg` format

    pycomic.py convert COMICNAME

##### download
Download comic

    pycomic.py download COMICNAME

##### fetch-url
Store each image link of comic to local  

    pycomic.py fetch-url COMICNAME

##### help
Show available command options

    pycomic.py help

##### list
List stored comic title information
Optional `PATTERN` search for matching

    pycomic.py list [PATTERN]

##### list-books
List books that are stored in local  
Show matching pattern if `PATTERN` is provided  
`origin` option for unconverted images  
`format` option for converted images

    pycomic.py list-books origin|format [PATTERN]

##### list-pdf
List pdf files of comic that is stored  
Show matching pattern if `PATTERN` is provided

    pycomic.py list-pdf [PATTERN]

##### list-url
List extracted url files
Show matching pattern if `PATTERN` is provided

    pycomic.py list-url [PATTERN]

##### make-pdf
Use downloaded comic images to make pdf file  

    pycomic.py make-pdf COMICNAME

##### source
Change or reference source type information  
Reference mode if no `SOURCE_TYPE` given

    pycomic.py source [SOURCE_TYPE]

##### state-change
Change comic progress state

    pycomic.py state-change COMICNAME

##### verify
Verify download images integrity

    pycomic.py verify COMICNAME

##### version
Show current version of the program

    pycomic.py version

##### eyny-download
Download images process for Eyny site

    pycomic.py eyny-download URL

---

#### Type 999comics
- add
- convert-image
- download
- error-url
- fetch-menu
- fetch-url
- help
- list
- list-books
- list-menu
- list-pdf
- list-url
- make-pdf
- source
- state-change
- verify-image
- version

##### add
Store comic information to menu csv file

    pycomic.py add ENGLISHNAME CHINESENAME NUMBER

##### convert-image
Convert images to jpeg file type

    pycomic.py convert-image COMICNAME FILETAG

##### download
Save comic images to local 

    pycomic.py download COMICNAME FILETAG

##### error-url
Show errors that occurs during url fetching process

    pycomic.py error-url COMICNAME IDENTITYNUM

##### fetch-menu
Store chapter's information of each comic

    pycomic.py fetch-menu COMICNAME

##### fetch-url
Store each image link of comic's chapter

    pycomic.py fetch-url COMICNAME IDENTITYNUM

##### help
Show available command options

    pycomic.py help

##### list
List stored comic information  
Optional `PATTERN` search for matching

    pycomic.py list [PATTERN]

##### list-books
List stored comic chapters  
`origin` option to show raw image data  
`format` option to show jpeg image data

    pycomic.py list-books origin|format COMICNAME [PATTERN]

##### list-menu
List chapter's information of comic  
Optional `PATTERN` search for matching 

    pycomic.py list-menu [PATTERN]

##### list-pdf
List pdf file for comic
Optional `PATTERN` search for matching

    pycomic.py list-pdf COMICNAME [PATTERN]

##### list-url
List pages' url of comic chapter  
Optional `PATTERN` search for matching

    pycomic.py list-url COMICNAME [PATTERN]

##### make-pdf
Make pdf file from downloaded images

    pycomic.py make-pdf COMICNAME FILETAG

##### source
Change or reference source type
Reference mode if no `SOURCE_TYPE` given

    pycomic.py source [SOURCE_TYPE]

##### state-change
Change comic progress state

    pycomic.py state-change COMICNAME

##### verify-image
Verify downloaded images integrity
Verify `origin` downloaded images

    pycomic.py verify-image COMICNAME FILETAG

##### version
Show current version of the program

    pycomic.py version

---

#### Type manhuagui
- add
- convert-image
- download 
- error-url
- fetch-menu
- fetch-url 
- help
- list
- list-books
- list-menu
- list-pdf
- list-url
- make-pdf
- source
- state-change
- url-image
- verify-image
- version

##### add
Store comic information to menu csv file

    pycomic.py add ENGLISHNAME CHINESENAME NUMBER

##### convert-image
Convert images to jpeg file type

    pycomic.py convert-image COMICNAME FILETAG

##### download (Status: Fixing)
Save comic images to local 

    pycomic.py download COMICNAME FILETAG

##### error-url
Show errors that occurs during url fetching process

    pycomic.py error-url COMICNAME IDENTITYNUM

##### fetch-menu
Store chapter's information of each comic

    pycomic.py fetch-menu COMICNAME

##### fetch-url 
Store each image link of comic's chapter

    pycomic.py fetch-url COMICNAME IDENTITYNUM

##### help
Show available command options

    pycomic.py help

##### list
List stored comic information  
Optional `PATTERN` search for matching

    pycomic.py list [PATTERN]

##### list-books
List stored comic chapters  
`origin` option to show raw image data  
`format` option to show jpeg image data

    pycomic.py list-books origin|format COMICNAME [PATTERN]

##### list-menu
List chapter's information of comic  
Optional `PATTERN` search for matching 

    pycomic.py list-menu [PATTERN]

##### list-pdf
List pdf file for comic
Optional `PATTERN` search for matching

    pycomic.py list-pdf COMICNAME [PATTERN]

##### list-url
List pages' url of comic chapter  
Optional `PATTERN` search for matching

    pycomic.py list-url COMICNAME [PATTERN]

##### make-pdf
Make pdf file from downloaded images

    pycomic.py make-pdf COMICNAME FILETAG

##### source
Change or reference source type
Reference mode if no `SOURCE_TYPE` given

    pycomic.py source [SOURCE_TYPE]

##### state-change
Change comic progress state

    pycomic.py state-change COMICNAME

##### url-image
Temporary substitution function for `download` and `fetch-url`  
Fetch image urls and download image at once

    pycomic.py url-image COMICNAME IDENTITYNUM

##### verify-image
Verify downloaded images integrity

    pycomic.py verify-image COMICNAME FILETAG

##### version
Show current version of the program

    pycomic.py version


### Error code
**Summary**
`1` - Program function usage error

`101` - Failed to read config ini file (ConfigNotFoundError)
`102` - Failed to read section in config file (NoSectionError)
`103` - Failed to read option in config file (NoOptionError)

**`pycomic.py`**  
`3` - Failed to read config ini file  

**`pycomic_pkg/pycomic_manhuagui`**  
`1` - Program usage error  
`3` - Webpage request error  
`11` - ComicNotFoundError catch  
`12` - UpdateError catch  
`13` - FileNotFoundError catch  
`16` - CSVError catch  
`18` - DataIndexEror catch  
`21` - Directory exist error  
`31` - HTTPError catch  
`32` - DriverError catch  
`33` - urlError catch

**`pycomic_pkg/pycomic_file`**
`1` - Program usage error  
`3` - Webpage request error  
`11` - ComicNotFoundError catch  
`12` - UpdateError catch  
`13` - FileNotFoundError catch  
`14` - FileExistError catch  
`15` - IOError catch  
`16` - CSVError catch  
`17` - TXTError catch  
`21` - Directory exist error  
`22` - Make pdf error  