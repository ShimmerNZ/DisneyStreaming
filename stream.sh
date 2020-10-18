#!/bin/bash
cd /home/pi/DisneyStreaming
xset s 60
/usr/bin/python3 "/home/pi/DisneyStreaming/networkmonitor.py" >> "/home/pi/logs/stream.log" 2&>1