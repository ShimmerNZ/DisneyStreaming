#!/bin/bash
cd /home/pi/DisneyStreaming/
git pull origin master
sleep 3
sudo cp /home/pi/DisneyStreaming/Update.desktop /home/pi/Desktop/Update.desktop
sudo cp /home/pi/DisneyStreaming/Stream.desktop /home/pi/Desktop/Stream.desktop
sudo cp /home/pi/DisneyStreaming/splash.png /usr/share/plymouth/themes/pix/splash.png
sleep 3