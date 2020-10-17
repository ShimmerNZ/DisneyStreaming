#!/usr/bin/python
import os
import subprocess
import time

time.sleep(300)

while True:
    try:
        ps=subprocess.Popen("ip link list wlan1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = subprocess.check_output(('grep','NO-CARRIER'),stdin=ps.stdout)
        print(output)
        if 'NO-CARRIER' in output:
            os.system('sudo ip link set wlan1 down')
            os.system('sudo ip link set wlan1 up')
            time.sleep(30)
        else:
            time.sleep(30)
            print("network ok")
    except subprocess.CalledProcessError:
        time.sleep(30)