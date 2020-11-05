#!/usr/bin/python
import os
import subprocess
import time

time.sleep(300)

while True:
    try:
        ps=subprocess.Popen("ip link list wlx244bfe3a2a5c", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = subprocess.check_output(('grep','NO-CARRIER'),stdin=ps.stdout)
        print(output, flush=True)
        if 'NO-CARRIER' in output:
            os.system('sudo ip link set wlx244bfe3a2a5c down')
            os.system('sudo ip link set wlx244bfe3a2a5c up')
            time.sleep(30)
        else:
            time.sleep(30)
            #print("network ok", flush=True)
    except subprocess.CalledProcessError:
        time.sleep(30)
        #print("network ok", flush=True)