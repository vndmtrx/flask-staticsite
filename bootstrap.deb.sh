#!/usr/bin/env bash

#Python 3
sudo apt install python3-pip python3-venv
python3 -m venv .env3/

source .env3/bin/activate
python --version
pip --version

pip install wheel
pip install -r requirements.txt
deactivate

#Python 2
sudo apt install sudo apt install python-virtualenv
python2 -m virtualenv .env2/

source .env2/bin/activate
python --version
pip --version

pip install wheel
pip install -r requirements.txt
deactivate
