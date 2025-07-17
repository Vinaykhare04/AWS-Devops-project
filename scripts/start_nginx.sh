#!/bin/bash
sudo systemctl start nginx
cd /home/ubuntu/app
pkill -f app.py
nohup python3 app.py > output.log 2>&1 &

