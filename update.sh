#!/bin/bash
cd /home/pi/DisneyStreaming/
git pull origin master
sleep 2
cp /home/pi/DisneyStreaming/Update.desktop /home/pi/Desktop/Update.desktop
cp /home/pi/DisneyStreaming/Update.desktop /home/pi/Desktop/Stream.desktop
sudo cp /home/pi/DisneyStreaming/splash.png /usr/share/plymouth/themes/pix/splash.png
sleep 3