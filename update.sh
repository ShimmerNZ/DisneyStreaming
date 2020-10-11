#!/bin/bash
cd /home/pi/DisneyStreaming/
git pull origin master
sudo cp /home/pi/DisneyStreaming/Update.txt /home/pi/Desktop/Update.desktop
sudo cp /home/pi/DisneyStreaming/Stream.txt /home/pi/Desktop/Stream.desktop
sudo cp /home/pi/DisneyStreaming/splash.png /usr/share/plymouth/themes/pix/splash.png
sudo chmod +x /home/pi/DisneyStreaming/stream.sh
sleep 1