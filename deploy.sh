#!/bin/bash

cd ~
git clone https://github.com/wilglison/invest-bots.git
cd ~/invest-bots
apt install -y python3.10-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py &