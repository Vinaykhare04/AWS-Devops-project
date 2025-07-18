#!/bin/bash
sudo systemctl start nginx
cd /home/ubuntu/app
nohup python3 app.py > output.log 2>&1 &
