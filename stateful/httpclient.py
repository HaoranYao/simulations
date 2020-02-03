from threading import Thread
import sys
from queue import Queue
import time
import argparse
from threading import Lock
import numpy as np
from http.client import HTTPConnection
from urllib.parse import urlparse,quote
from asteval import Interpreter
active = True

lock = Lock()
results = []

def doWork():
    while True:
        url = q.get()
        start = time.monotonic()
        status, url, dbytes = getStatus(url)
        latency = time.monotonic() - start
        #doSomethingWithResult(status, url)

        lock.acquire()
        results.append((url,latency,dbytes,status))
        lock.release()
        q.task_done()


def printresults():
    global results
    global active
    start = time.monotonic()
    while (time.monotonic() - start < duration):
        time.sleep(interval)
        elapsed = int(time.monotonic() - start)
        lock.acquire()
        probes = []
        o = []
        n = 0
        nbytes = 0
        err = 0
        for url,latency,dbytes,status in results:
            if status == "error":
                err += 1
            else:
                n += 1
                nbytes += dbytes
                if url == probe:
                    probes.append(latency)
                else:
                    o.append(latency)
        results = []

        lock.release()

        print("GEN-%d-RESULT-GERR %f" % (elapsed,err / interval))
        print("GEN-%d-RESULT-GNBREQ %f" % (elapsed,n / interval))
        print("GEN-%d-RESULT-GBYTES %f" % (elapsed,nbytes / interval))
        if len(probes) > 0:
            print("GEN-%d-RESULT-GPROBELAT99 %f" % (elapsed,np.percentile(probes,99)))

            print("GEN-%d-RESULT-GPROBELATENCY %f" % (elapsed,np.mean(probes)))

        if len(o) > 0:
            print("GEN-%d-RESULT-GLAT99 %f" % (elapsed,np.percentile(o,99)))
            print("GEN-%d-RESULT-GLATENCY %f" % (elapsed,np.mean(o)))
    active=False

def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = HTTPConnection(url.netloc, source_address=None if not args.bind else (args.bind[0],0))
        conn.request("GET", url.path + "?" + url.query)
        res = conn.getresponse()
        return res.status, ourl, len(res.read())
    except Exception as e:
        print(e)
        return "error", ourl, 0

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('urllist', metavar='PATH', type=str, nargs=1,
                    help='URL file')
parser.add_argument('--host', metavar='HOST', type=str, nargs=1,
                    help='URL file')
parser.add_argument('--probe', metavar='PATH', type=str, nargs=1,
                    help='URL')

parser.add_argument('--bind', metavar='IP', type=str, nargs=1, default=None,               help='URL')
parser.add_argument('--rate', metavar='N', type=str, nargs=1, default=None,               help='URL')
parser.add_argument('--concurrent', metavar='N', type=int, nargs=1, default=[100],               help='URL')
parser.add_argument('--duration', metavar='SECONDS', type=int, nargs=1, default=[15],                 help='Duration of the experiment')
parser.add_argument('--interval', metavar='SECONDS', type=float, default=1, action='store',                 help='Report interval')
args = parser.parse_args()
host=args.host[0]
duration = args.duration[0]
concurrent = args.concurrent[0]
rate = None if args.rate == None else args.rate[0]
probe = host + args.probe[0]
interval = args.interval

q = Queue(concurrent * 2)

t = Thread(target=printresults)
t.daemon = True
t.start()

#results = Queue()
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:

    aeval = Interpreter()
    i = 0

    start = time.monotonic()
    while active:
        for url in open(args.urllist[0]):
            if i % 100 == 0:
                q.put(probe)
            i += 1
            q.put(host + url.strip())
            if rate is not None:
                aeval.symtable['x'] = time.monotonic() - start
                time.sleep(1 / float(aeval(rate)))
            if not active:
                break
    print("Waiting for last threads!")
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
