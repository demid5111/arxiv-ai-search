#!/bin/bash
source config/common.sh

set -ex

echo -e '\n'
echo 'Running flake8 check...'

configure_script

DIRS_TO_CHECK=("config" "arxiv_scrapper" "vector_db")

for LAB_NAME in ${DIRS_TO_CHECK[*]}; do
  python -m flake8 $LAB_NAME
done

echo "flake8 check passed."
