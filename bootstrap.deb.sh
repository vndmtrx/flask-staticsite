#!/usr/bin/env bash

sudo apt install python3-pip python3-venv
python3 -m venv .env/

source .env/bin/activate
python --version
pip --version

pip install wheel
pip install -r requirements.txt
deactivate
