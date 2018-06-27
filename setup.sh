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
    sudo apt install -y virtualenv
  eslif echo ${distro} | grep -q "16.04";
    sudo apt-get install python-pip
    sudo pip install virtualenv
  fi
fi


virtualenv venv
echo 'install python requirements'
venv/bin/pip install -r requirements.txt
echo 'Done!'
