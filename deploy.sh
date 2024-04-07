#!/bin/bash

cd ~
git clone https://github.com/wilglison/invest-bots.git
cd ~/invest-bots
git pull
sudo apt install -y python3.10-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
crontab -r
echo "0 21 * * 1-5 ~/invest-bots/start.sh" | crontab -
chmod +x start.sh
