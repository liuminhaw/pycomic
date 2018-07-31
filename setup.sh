#!/bin/bash
#
# Program:
#   pycomic setup script


# PATH=/bin:/sbin:/usr/bin:/user/sbin:/usr/local/bin:/usr/local/sbin
# export PATH


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
  EXEC_DIR=${HOME}/local

  # Check target directory before setup
  if [[ ! -d ${EXEC_DIR} ]]; then
    mkdir ${EXEC_DIR}
    checkCode 11 "mkdir local failed."
    echo "export PATH=${PATH}:${EXEC_DIR}" >> ${HOME}/.bashrc
    checkCode 13 "echo to .bashrc failed."
    source ${HOME}/.bashrc
    checkCode 15 "Reload .bashrc file failed."
  fi

  # Setup process
  cp pycomic.py ${EXEC_DIR}
  checkCode 3 "Copy pycomic.py failed"
  chmod 755 ${EXEC_DIR}/pycomic.py
  checkCode 5 "Change file permission failed."
  cp .pycomic_template.ini ${HOME}/.pycomic.ini
  checkCode 9 "Copy .pycomic.ini failed."
  cp -r pycomic_pkg ${EXEC_DIR}
  checkCode 7 "Copy pycomic_pkg directory failed."
}


# System checking
SYSTEM_RELEASE=$(uname -a)
case ${SYSTEM_RELEASE} in
  *Linux*)
    echo "Linux detected"
    Installation
    ;;
  *)
    echo "Not supported."
    exit 1
esac


echo "pycomic setup success."
exit 0
