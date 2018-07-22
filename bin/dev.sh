#!/bin/sh

dnf install -y python3 which

python /root/wait_for_tcp.py kafka1 9092 60
python /root/wait_for_tcp.py kafka2 9092 60
cd /root/chat
pip3 install pipenv
pipenv install
pipenv run python3 app.py
