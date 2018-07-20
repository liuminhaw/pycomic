#!/bin/bash
#
# Program:
#   Setup shell for pycomic
#
# Exit Code:
#   1 : Script not executed by root
#   3 : The Linux distribution is not supported by this script
#
#   11 : Failed to copy pycomic.py
#   13 : Failed to change pycomic.py file permission
#   15 : Failed to copy logging_class.py
#   17 : Failed to copy pycomic_class.py
#   19 : Failed to copy user_agent_class.py
#   21 : Failed to install python modules using pip


PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
export PATH


function centos7Install() {
    pycomicMod

    if [[ -d "/usr/lib64/python3.6" ]]; then
        moduleMod /usr/lib64/python3.6/
    fi

    if [[ -d "/usr/lib64/python3.7" ]]; then
        moduleMod /usr/lib64/python3.7/
    fi
}

# Copy pycomic.py and change permission
function pycomicMod() {
    cp pycomic.py /usr/local/bin/
    checkCode 11 "Failed to copy pycomic.py"
    chmod 755 /usr/local/bin/pycomic.py
    checkCode 13 "Failed to change pycomic.py file permission"
}

function moduleMod() {
    LIBPATH=${1}
    cp logging_class.py ${LIBPATH}
    checkCode 15 "Failed to copy logging_class.py"
    cp pycomic_class.py ${LIBPATH}
    checkCode 17 "Failed to copy pycomic_class.py"
    cp user_agent_class.py ${LIBPATH}
    checkCode 19 "Failed to copy user_agent_class.py"
}

# Check exit code function
# USAGE:
#   checkCode EXITCODE MESSAGE
function checkCode() {
  if [[ ${?} -ne 0 ]]; then
    echo ${2}
    exit ${1}
  fi
}

# Script need to be executed by root
if [[ ${UID} -ne 0 ]]; then
  echo "This script need to be executed by root."
  exit 1
fi

# Linux distribution checking
SYSTEM_RELEASE=$(uname -r)
case ${SYSTEM_RELEASE} in
    *el7.x86_64*)
        echo "Detected CentOS7"
        centos7Install
        ;;
    *)
        echo "Not supported distribution"
        exit 3
esac

# Install require python modules
pip3 install -r requirements.txt > /dev/null
checkCode 21 "Failed to install python modules using pip3"

# Setup success
echo "pycomic setup success"
exit 0
