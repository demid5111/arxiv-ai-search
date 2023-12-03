apt -y update
apt install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y python3.11 git python3.11-venv htop

wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >>
/etc/apt/sources.list.d/google.list'
apt update
apt install -y google-chrome-stable
rm /etc/apt/sources.list.d/google.list

python3.11 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt

export PYTHONPATH=$(pwd)
