#!/usr/bin/env python3
from time import sleep,time
from parse import parse
from collections import defaultdict
import argparse

last_idle = defaultdict(int)
last_total = defaultdict(int)
def monitor(id,prefix):
  while True:
    t = time()
    with open('/proc/stat') as f:
      f.readline()
      while True:
        fields = f.readline().strip().split()
        matches = parse("cpu{}", fields[0])
        if matches is None:
            break
        cpuid = int(matches[0])
        if cpuid != id:
            continue
        fields = [float(column) for column in fields[1:]]
        idle, total = fields[3], sum(fields)
        idle_delta, total_delta = idle - last_idle[cpuid], total - last_total[cpuid]
        last_idle[cpuid], last_total[cpuid] = idle, total
        utilisation = 100.0 * (1.0 - idle_delta / total_delta)
        print('CPU-%d-RESULT-%s %f' % (round(t),prefix,utilisation))
    sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Print CPU load.')
    parser.add_argument('cpuid', metavar='N', type=int, nargs=1,
                                help='CPU id')
    parser.add_argument('serverid', metavar='N', type=int, nargs=1,
                                help='Server id')
    args = parser.parse_args()
    monitor(id=args.cpuid[0], prefix='SERVER-%d' % args.serverid[0])
