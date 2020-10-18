cd /home#!/bin/bash
cd /home/pi
sudo iptables -t mangle -I POSTROUTING 1 -j TTL --ttl-set 65
# set display then change screen timeout to 60 seconds so you dont wait forever for it to go to sleep
export DISPLAY=:0
xset s 60
/usr/bin/python3 "/home/pi/Wifi.py" >> "/home/pi/logs/wifi.log" 2&>1
