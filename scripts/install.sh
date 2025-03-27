#!/bin/bash

apt update -y;
apt install -y curl python3 python3-pip python3-venv;

python3 -m venv .venv

.venv/bin/pip3 install pip --upgrade
.venv/bin/pip3 install poetry
.venv/bin/poetry install
