sudo su -
yum update -y

yum install -y git
yum install -y python3

mkdir -p /var/scrapper
cd /var/scrapper
git clone https://github.com/jaabberwocky/hwz-textgenrnn .

pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt


