#!/bin/bash
echo 'install virtualenv'
sudo apt install -y virtualenv
virtualenv venv
echo 'install python requirements'
venv/bin/pip install -r requirements.txt
echo 'Done!'