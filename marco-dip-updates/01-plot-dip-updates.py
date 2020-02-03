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
#matplotlib.style.use('v2.0')
#x-axis: number-of sequences (fix size_of_sequences to 16)
#y-axis: average(scs-length) over the 6 seeds

paper_mode = True
subset_mode = False

outname = "01-plot-dip-updates"
fnames = []

for i in range(0, len(sys.argv) - 1, 1):
  #mode = sys.argv[2 + i]
  fnames.append(sys.argv[1 + i])

if paper_mode:
  fig = plt.figure(figsize=(5,2.5))
  #set_paper_rcs()
else:
  fig = plt.figure()
  #set_rcs()

colours = ['b', 'g', 'r', 'c', 'm', 'y', 'v']
markers = ['+', 'x', 'v', 's', 'd', 'o', '1']

cheetah = []
two_hashes = []
servers = []


ct = []
th = []
se = []

ctmap = {}
thmap = {}
semap ={}

fname = "results.csv"
fname2 = "temp_servers.csv"

filenames2 = []
filenames2.append(fname2)

dict_list = { "cheetah": ctmap, "hash" : thmap, "server" : semap}

file_list={"cheetah": "CheetahGNBREQ.csv","hash":"Hash_RSSGNBREQ.csv"}

for scheme,f in file_list.items():
  print( "Analyzing file %s: " % (f))

  for line in open(f).readlines():
    fields = [x.strip() for x in line.split(" ")]
    time = int(fields[0]) #
    reqs = [float(f) for f in fields[1:]]
    requests = np.median(reqs) #
    print(str(scheme) + " " + str(time) + " " + str(requests))
    #connections_per_bucket = int(float(connection_target)/float(servers)/float(buckets_to_server))
    if scheme == "cheetah":
        print("  " + str(time) + " " + str(requests))
        ctmap.setdefault(time, [])
        ctmap[time].append(requests)
    elif scheme == "hash":
        print("  " + str(time) + " " + str(requests))
        thmap.setdefault(time, [])
        thmap[time].append(requests)

for f in filenames2:
  for line in open(f).readlines()[1:]:
    fields = [x.strip() for x in line.split(" ")]
    time = int(fields[0]) #
    num_servers = fields[1] #
    print(str(time) + " " + str(num_servers))
    #connections_per_bucket = int(float(connection_target)/float(servers)/float(buckets_to_server))
    if time < 2:
        continue
    time = time-2
    semap.setdefault(time, [])

    semap[time].append(num_servers)
c1 = (148/255.0, 103/255.0, 189/255.0)
c2 = (255/255, 127/255.0, 14/255.0)

for item in dict_list:
  dict_ = dict_list[item]
  for key in sorted(dict_.keys()):
    dict_float = [float(x) for x in dict_[key]]
    row = np.average(dict_float)
    if (item == "cheetah"):
      cheetah.append(row)
      ct.append(key)
    elif (item == "hash"):
      two_hashes.append(row)
      th.append(key)
    elif (item == "server"):
      servers.append(row)
      se.append(key)

fig, ax1 = plt.subplots(figsize=(5,2.5))
ax2 = ax1.twinx()
color1 = (np.asarray(c2) + np.asarray(c1)) / 3
color2 = "darkolivegreen"
ax1.set_xlim(-2,40)
ax1.set_ylim(1050,1400)
ax2.set_ylim(23.8,38)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('#Completed requests/sec', color=color1)
ax2.set_ylabel('Active servers', color=color2)
ax1.tick_params(axis='y', labelcolor=color1)
ax2.tick_params(axis='y', labelcolor=color2)

#plt.xlabel("Time [s]",  fontsize=10)
#plt.ylabel("\#Completed requests/sec")
#plt.yscale('log')
#plt.title('sizeofsequence=16')
#plt.ylim(0,2000)
#plt.xlim(-2,42)
#miny=1050
#plt.ylim(miny, 1400)
#plt.yticks(range(1050, 1401, 100), [str(x) for x in range(1050, 1401, 100)])

#plt.annotate("10x", (122000, 3.65), fontsize='8' )
#plt.annotate("", (120000,1.65), xytext=(120000,17), arrowprops=dict(arrowstyle='<->, head_length=0.15, head_width=0.15',lw=0.7))
#plt.annotate("4x", (123000, 0.56), fontsize='8')
#plt.annotate("", (120000,0.41), xytext=(120000,1.74), arrowprops=dict(arrowstyle='<->, head_length=0.15, head_width=0.15',lw=0.7))
#plt.plot(rr, round_robin, label="round-robin",color='orange', lw=1.0, linestyle='-',marker= 's', mfc='none', mec='orange', ms=3)
#plt.plot(bm, beamer, label="beamer",color='red', lw=1.0, linestyle='-',marker= '>', mfc='none', mec='red', ms=3)
#plt.plot(ch, consistent_hashing, label="consistent-hash",color='blue', lw=1.0, linestyle='-',marker= 'x', mfc='none', mec='blue', ms=3)


ax2.plot(se, servers, label="#Servers",color='olive', lw=1.0, linestyle='dashdot',marker= None, mfc='none', mec='salmon', ms=3)
ax1.plot(th, two_hashes, label="Hash RSS",color=c2, lw=1.0, linestyle='-',marker= None, mfc='none', mec='lightsteelblue', ms=3)
ax1.plot(ct, cheetah, label="Cheetah",color=c1, lw=1.0, linestyle='-',marker= None, mfc='none', mec='royalblue', ms=3)
fig.tight_layout()
plt.show()


handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels, loc='upper left', frameon=False,ncol=1, columnspacing=0.4, handletextpad=0.2)
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles, labels, loc='upper right', frameon=False,ncol=1, columnspacing=0.4, handletextpad=0.2)


plt.savefig("%s.pdf" % outname, format="pdf", bbox_inches='tight', pad_inches=0.05)

