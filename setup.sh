#!/bin/bash
echo 'check linux distro'
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac
echo ${machine}
distro="$(lsb_release -r)"
if [[ ${machine} = 'Linux' ]]
then
  echo 'install virtualenv'
  if echo ${distro} | grep -q "18.04";
  then
    echo ${distro}
    sudo apt install -y python3
    python3 -m venv venv3
  eslif echo ${distro} | grep -q "16.04";
    sudo apt-get install python-pip3
    sudo pip3 install virtualenv
    virtualenv venv3
  fi
fi

echo "upgrade pip"
venv3/bin/pip install pip --upgrade
echo 'install python requirements'
venv3/bin/pip install -r requirements.txt
echo 'Done!'
