#!/usr/bin/python
import os
import subprocess
import time

time.sleep(300)
ps=subprocess.Popen("ip link list wlan1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while True:
    try:
        output = subprocess.check_output(('grep','NO-CARRIER'),stdin=ps.stdout)
        print(output)
        os.system('sudo ip link set wlan1 down')
        os.system('sudo ip link set wlan1 up')
        time.sleep(30)
    except subprocess.CalledProcessError:
        time.sleep(10)