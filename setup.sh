#!/bin/bash
#
# Program:
#   Setup shell for pycomic
#
# Exit Code:
#   1 : Script not executed by root
#
#   11 : Failed to copy pycomic.py
#   13 : Failed to change pycomic.py file permission
#   15 : Failed to copy logging_class.py
#   17 : Failed to copy pycomic_class.py
#   19 : Failed to copy user_agent_class.py
#   21 : Failed to install python modules using pip


PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
export PATH


# Check exit code function
# USAGE:
#   checkCode EXITCODE MESSAGE
function checkCode() {
  if [[ ${?} -ne 0 ]]; then
    echo ${2}
    exit ${1}
  fi
}

# Check exit code of class module
# USAGE:
#   checkClassCode EXITCODE FILENAME
function checkClassCode() {
  EXITCODE=${1}
  FILENAME=${2}

  if [[ -d "/usr/lib/python3.6" ]]; then
    cp ${FILENAME} /usr/lib/python3.6
    RETURN_VALUE_1=${?}
  fi

  if [[ -d "/usr/lib/python3.7" ]]; then
    cp ${FILENAME} /usr/lib/python3.7
    RETURN_VALUE_2=${?}
  fi

  if [[ (RETURN_VALUE_1 -ne 0) && (RETURN_VALUE_2 -ne 0) ]]; then
    echo "Failed to copy ${FILENAME}"
    exit ${EXITCODE}
  fi
}


# Script need to be executed by root
if [[ ${UID} -ne 0 ]]; then
  echo "This script need to be executed by root."
  exit 1
fi

# Copy pycomic.py file
cp pycomic.py /usr/local/bin/
checkCode 11 "Failed to copy pycomic.py"

# Change permission
chmod 755 /usr/local/bin/pycomic.py
checkCode 13 "Failed to change pycomic.py file permission"

# Copy logging_class.py
checkClassCode 15 "logging_class.py"

# Copy pycomic_class.py
checkClassCode 17 "pycomic_class.py"

# Copy user_agent_class.py
checkClassCode 19 "user_agent_class.py"


# Install require python modules
pip install -r requirements.txt > /dev/null
checkCode 21 "Failed to install python modules using pip"

echo "pycomic setup success"
exit 0
