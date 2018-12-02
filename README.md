# pycomic
#### Program to download and save comic to local disk
Fetching comic from multiple sources

#### Additional Requirement
selenium `chromedriver` need to be installed before program can be run

#### Setup
Run `setup.sh` script to setup program for use  
`DESTINATION` is where you want to put all the comics data

    ./setup.sh DESTINATION

#### Configuration
`.pycomic.ini` config file will be create in user's home directory  
Modify `.pycomic.ini` for custom configuration

### In Development
- New program structure
- Multiple sources type

##### Type File
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
Verify download images' integrity

    pycomic.py verify COMICNAME


##### Type 999comics
- add
- error-url
- fetch-menu
- fetch-url
- help
- list
- list-menu
- list-url
- source

##### add
Store comic information to menu csv file

    pycomic.py add ENGLISHNAME CHINESENAME NUMBER

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

##### list-menu
List chapter's information of comic  
Optional `PATTERN` search for matching 

    pycomic.py list-menu [PATTERN]

##### list-url
List pages' url of comic chapter  
Optional `PATTERN` search for matching

    pycomic.py list-url COMICNAME [PATTERN]

##### source
Change or reference source type
Reference mode if no `SOURCE_TYPE` given

    pycomic.py source [SOURCE_TYPE]
