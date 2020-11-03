#!/bin/bash
cd /home/pi/DisneyStreaming/
wget -qO- https://get.speedify.com | sudo -E bash -
sleep 5
sudo apt-get install speedifyui
sleep 10
