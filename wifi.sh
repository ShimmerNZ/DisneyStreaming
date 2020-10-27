cd /home#!/bin/bash
cd /home/pi
sudo iptables -t mangle -I POSTROUTING 1 -j TTL --ttl-set 65
sudo sysctl -w net.ipv4.ip_default_ttl=65
/usr/bin/python3 "/home/pi/DisneyStreaming/Wifi.py" >> "/home/pi/logs/wifi.log" 2>&1