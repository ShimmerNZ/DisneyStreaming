#!/bin/bash
cd /home/pi/DisneyStreaming/
git pull origin master
sudo cp /home/pi/DisneyStreaming/Update.txt /home/pi/Desktop/Update.desktop
sudo cp /home/pi/DisneyStreaming/Stream.txt /home/pi/Desktop/Stream.desktop
sudo cp /home/pi/DisneyStreaming/Stream.txt /home/pi/.config/autostart/Stream.desktop
sudo cp /home/pi/DisneyStreaming/Keyboard.txt /home/pi/Desktop/Keyboard.desktop
sudo cp /home/pi/DisneyStreaming/images/splash.png /usr/share/plymouth/themes/pix/splash.png
sudo cp /home/pi/DisneyStreaming/update.sh /home/pi/update.sh
sudo cp /home/pi/DisneyStreaming/stream.sh /home/pi/stream.sh
sudo cp /home/pi/DisneyStreaming/wifi.sh /home/pi/wifi.sh
sudo cp /home/pi/DisneyStreaming/keyboard.sh /home/pi/keyboard.sh
sudo chmod +x /home/pi/stream.sh
sudo chmod +x /home/pi/wifi.sh
sudo chmod +x /home/pi/update.sh
sudo chmod +x /home/pi/keyboard.sh
sleep 2
