#!/bin/bash
#
# Program:
#   pycomic setup script
#
# Exit Code:
#   1 - Calling syntax error
#   3 - Destination directory does not exist
#
#   11 - Copy file failed
#   13 - Change file permission failed


# Check exit code function
# USAGE:
#   checkCode EXITCODE MESSAGE
function checkCode() {
  if [[ ${?} -ne 0 ]]; then
    echo ${2}
    exit ${1}
  fi
}

function Installation() {
    DESTDIR=${1}

    # Setup process
    cp README.md ${DESTDIR}
    checkCode 11 "Copy README.md failed." &> /dev/null
    cp pycomic.py ${DESTDIR}
    checkCode 11 "Copy pycomic.py failed."  &> /dev/null
    chmod 755 ${DESTDIR}/pycomic.py
    checkCode 13 "Change file permission failed."   &> /dev/null
    cp pycomic_template.ini ${DESTDIR}/pycomic_config.ini
    checkCode 11 "Copy pycomic_template.ini failed."    &> /dev/null

    if [[ ! -f ${DESTDIR}/user_config.ini ]]; then
        cp user_template.ini ${DESTDIR}/user_config.ini
        checkCode 11 "Copy user_template.ini failed."    &> /dev/null
    fi

    chmod 600 ${DESTDIR}/user_config.ini
    checkCode 13 "Change file permission failed."
    cp requirements.txt ${DESTDIR}
    checkCode 11 "Copy requirements.txt failed." &> /dev/null
    cp -r pycomic_pkg ${DESTDIR}
    checkCode 11 "Copy pycomic_pkg directory failed."   &> /dev/null
}


# Calling setup format check
USAGE="setup.sh DESTINATION"

if [[ ${#} -ne 1 ]];  then
    echo -e "USAGE:\n    ${USAGE}"
    exit 1
fi

if [[ ! -d ${1} ]]; then
    echo "ERROR: Destination directory does not exist"
    exit 3
fi


# System checking
SYSTEM_RELEASE=$(uname -a)
case ${SYSTEM_RELEASE} in
  *Linux*)
    echo "Linux detected"
    echo ""
    Installation ${1}
    ;;
  *)
    echo "Not supported."
    exit 1
esac


echo "pycomic setup success."
exit 0
