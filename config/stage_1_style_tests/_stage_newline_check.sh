set -ex
source config/common.sh

echo -e '\n'

echo "Check newline at the end of the file"

configure_script

python config/stage_1_style_tests/newline_check.py
