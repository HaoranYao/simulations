import requests
import threading
import time
import sys
import psutil
url = "http://192.168.0.1/cheetah/load"
server = int(sys.argv[1])
while 1:
    time.sleep(5)
    try:
        #load = int(psutil.cpu_percent())
        cpu = psutil.cpu_percent(percpu=True)
        load = int(cpu[server])
        r = requests.post(url, data = 'The load is '+str(server)+' '+str(load))
    except:
        continue


