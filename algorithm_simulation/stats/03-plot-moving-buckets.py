# Copyright (c) 2015, Malte Schwarzkopf
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of qjump-nsdi15-plotting nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### Marco ###
'''
Adapted from the following original code:
https://github.com/camsas/qjump-nsdi15-plotting/blob/master/figure1b_3b/plot_memcached_latency_cdfs.py

'''

import os, sys, re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pylab
from utils import *
from matplotlib.ticker import FuncFormatter

#x-axis: number-of sequences (fix size_of_sequences to 16)
#y-axis: average(scs-length) over the 6 seeds

paper_mode = True
subset_mode = False

outname = "03-plot-moving-buckets"
fnames = []

for i in range(0, len(sys.argv) - 1, 1):
  #mode = sys.argv[2 + i]
  fnames.append(sys.argv[1 + i])

if paper_mode:
  fig = plt.figure(figsize=(3.33,1.2))
  set_paper_rcs()
else:
  fig = plt.figure()
  set_rcs()

colours = ['b', 'g', 'r', 'c', 'm', 'y', 'v']

hadoop = []
webservers = []
cachefollowers = []

hd = []
ws = []
cf = []

hdmap = {}
wsmap = {}
cfmap = {}

fname = "report.csv"

filenames = []
filenames.append(fname)

dict_list = {"hadoop": hdmap}
# dict_list = {"hadoop": hdmap, "webservers": wsmap, "cachefollowers": cfmap}
workload = "hadoop"

for f in filenames:
  print "Analyzing file %s: " % (f)
  for line in open(f).readlines()[1:]:
    fields = [x.strip() for x in line.split(",")]
    model = fields[0] #
    connection_target = fields[1] #
    end_time = fields[2] #
    server_number = fields[3] #
    update_rate = fields[4] #
    bucket_number = fields[5] #
    imbalance_threshold = fields[6] #
    total_connections = fields[7] #
    broken_connections = fields[8] #
    broken_rate = fields[9] #
    max_imbalance = fields[10] #
    ave_imbalance = fields[11] #
    moving_bucket_rate = fields[12]
    if model != "dy_beamer":
        continue
    if workload == "hadoop":
      hdmap.setdefault(imbalance_threshold, [])
      hdmap[imbalance_threshold].append(moving_bucket_rate)
    elif workload == "cachefollowers":
      cfmap.setdefault(imbalance_threshold, [])
      cfmap[imbalance_threshold].append(moving_bucket_rate)
    elif workload == "webservers":
      wsmap.setdefault(imbalance_threshold, [])
      wsmap[imbalance_threshold].append(moving_bucket_rate)

for item in dict_list:
  dict_ = dict_list[item]
  print str(item) + " " + str(dict_)
  for key in sorted(dict_.keys()):
    dict_float = [float(x) for x in dict_[key]]
    row = np.average(dict_float)
    if item == "hadoop":
      hadoop.append(row)
      hd.append(key)
    elif (item == "cachefollowers"):
      cachefollowers.append(row)
      cf.append(key)
    elif (item == "webservers"):
      webservers.append(row)
      ws.append(key)

plt.xlabel("Imabalance [\%]", fontsize=10)
plt.ylabel("Moving buckets rate", y=0.32)
#plt.xscale('log')
#plt.title('sizeofsequence=16')
#plt.ylim(0,2000)
plt.xlim(1.5, 6)
miny=0
plt.ylim(miny, 2)
#plt.yticks(range(miny, 1101, 200), [str(x) for x in range(miny, 1101, 200)])

xaxis = [str((float(i) -1)*100) for i in hd]
plt.plot(xaxis, hadoop, label="hadoop",color='red', lw=1.0, linestyle='-',marker= '>', mfc='none', mec='red', ms=3)
# plt.plot(cf, cachefollowers, label="cache-followers",color='blue', lw=1.0, linestyle='-',marker= 's', mfc='none', mec='blue', ms=3)
# plt.plot(ws, webservers, label="web-servers",color='green', lw=1.0, linestyle='-',marker= 'v', mfc='none', mec='green', ms=3)


plt.legend(loc='upper left', frameon=False, ncol=2, columnspacing=0.2, handletextpad=0.2)
plt.savefig("%s.pdf" % outname, format="pdf", bbox_inches='tight', pad_inches=0.05)

