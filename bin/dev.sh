#!/bin/sh

dnf install -y python3 which

python /root/wait_for_tcp.py kafka 9092 60
cd /root/chat
pip3 install pipenv
pipenv install
pipenv run python3 app.py
