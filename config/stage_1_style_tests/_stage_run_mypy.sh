#!/bin/bash
source config/common.sh

set -ex

echo -e '\n'
echo 'Running mypy check...'

configure_script

DIRS_TO_CHECK=("config" "arxiv_scrapper" "vector_db")

for LAB_NAME in ${DIRS_TO_CHECK[*]}; do
  if [[ ${LAB_NAME} == 'arxiv_scrapper' ]]; then
    continue
  fi

  if [[ ${LAB_NAME} == 'vector_db' ]]; then
    continue
  fi

  mypy $LAB_NAME
done

echo "Mypy check passed."
