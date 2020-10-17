cd /home#!/bin/bash
cd /home/pi/DisneyStreaming/
sudo iptables -t mangle -I POSTROUTING 1 -j TTL --ttl-set 65
/usr/bin/python "/home/pi/DisneyStreaming/Wifi.py" >> "/home/pi/logs/wifi.log" 2&>1