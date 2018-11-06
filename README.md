# pycomic
#### Program to download and save comic to local disk
Fetching comic from multiple sources

#### Additional Requirement
selenium `driver` need to be installed before program can be run

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
