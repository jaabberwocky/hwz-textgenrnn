# run as root user
sudo yum update -y

sudo yum install -y git
sudo yum install -y python3

sudo mkdir -p /var/scrapper
cd /var/scrapper
git clone https://github.com/jaabberwocky/hwz-textgenrnn .

sudo pip3 install virtualenv
sudo virtualenv venv
sudo source venv/bin/activate
sudo pip3 install -r requirements.txt


