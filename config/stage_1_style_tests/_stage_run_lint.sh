#!/bin/bash
source config/common.sh

set -ex

echo -e '\n'
echo 'Running lint check...'

configure_script

DIRS_TO_CHECK=("config" "arxiv_scrapper" "vector_db")

python -m pylint --fail-under=8 \
        --disable=missing-function-docstring \
        --disable=missing-module-docstring \
        --disable=missing-class-docstring \
        --rcfile config/stage_1_style_tests/.pylintrc "${DIRS_TO_CHECK[@]}"

echo "Lint check passed."
