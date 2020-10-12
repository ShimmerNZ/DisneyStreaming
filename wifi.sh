#!/bin/bash
cd /home/pi/DisneyStreaming/
sudo iptables -t mangle -A POSTROUTING -j TTL --ttl-set 65
/usr/bin/python "/home/pi/DisneyStreaming/Wifi.py" >> "/home/pi/logs/wifi.log" 2&>1