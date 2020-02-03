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


### Marco, Roshan ###
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

outname = "01-optimal-seq-7-bitcost"
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

dpscs = []
greedy = []
hierarchical = []
fastgreedy = []


dp = []
gr = []
hier = []
fast = []

dpscsmap = {}
greedymap = {}
hierarchicalmap = {}
fastgreedymap = {}

fname = "results_aggregation-renamed-final-4.txt"

filenames = []
filenames.append(fname)

dict_list = {"dpscs": dpscsmap, "greedy": greedymap, "hierarchical": hierarchicalmap, "fastgreedy": fastgreedymap}

for f in filenames:
  print "Analyzing file %s: " % (f)
  for line in open(f).readlines()[1:]:
    fields = [x.strip() for x in line.split()]
    algo = fields[0] # algo
    generator = fields[1] # random generator
    seed = fields[2] # random seed
    nof_sq = int(fields[3]) # no of sequences
    seq_size = int(fields[4]) # seq size
    cost = fields[5] # bitcost/entrycost
    scs_length = int(fields[6]) # scs length
    timems = float(fields[7]) # time in millisecond
    bitcost = (scs_length + seq_size) * scs_length
    if algo == "dpscs" and seq_size == 7 and generator == "random":
      dpscsmap.setdefault(nof_sq, [])
      dpscsmap[nof_sq].append(bitcost)
    elif algo == "hierarchical" and seq_size == 7 and generator == "random":
      hierarchicalmap.setdefault(nof_sq, [])
      hierarchicalmap[nof_sq].append(bitcost)
    elif algo == "greedy" and seq_size == 7 and generator == "random":
      greedymap.setdefault(nof_sq, [])
      greedymap[nof_sq].append(bitcost)
    elif algo == "fastgreedy" and seq_size == 7 and generator == "random":
      fastgreedymap.setdefault(nof_sq, [])
      fastgreedymap[nof_sq].append(bitcost)


for item in dict_list:
  dict_ = dict_list[item]
  for key in sorted(dict_.keys()):
    if len(dict_[key]) < 3:
      continue
    row = np.average(dict_[key])
    if item == "dpscs":
      dpscs.append(row)
      dp.append(key)
    elif (item == "greedy"):
      greedy.append(row)
      gr.append(key)
    elif (item == "hierarchical"):
      hierarchical.append(row)
      hier.append(key)
    elif (item == "fastgreedy"):
      fastgreedy.append(row)
      fast.append(key)

plt.xlabel("number of sequences", fontsize=10)
plt.ylabel("Memory cost [bit]")
#plt.xscale('log')
#plt.title('sizeofsequence=16')
#plt.ylim(0,2000)
plt.xlim(2, 8)
miny=0
plt.ylim(miny, 1100)
plt.yticks(range(miny, 1101, 200), [str(x) for x in range(miny, 1101, 200)])


plt.plot(dp, dpscs, label="dpscs",color='magenta', lw=1.0, linestyle='-',marker= 'x', mfc='none', mec='magenta', ms=3)
plt.plot(gr, greedy, label="greedy",color='red', lw=1.0, linestyle='-',marker= '>', mfc='none', mec='red', ms=3)
plt.plot(hier, hierarchical, label="hierarchical",color='blue', lw=1.0, linestyle='-',marker= 's', mfc='none', mec='blue', ms=3)
plt.plot(fast, fastgreedy, label="fastgreedy",color='green', lw=1.0, linestyle='-',marker= 'v', mfc='none', mec='green', ms=3)


plt.legend(loc='upper left', frameon=False, ncol=2)
plt.savefig("%s.pdf" % outname, format="pdf", bbox_inches='tight', pad_inches=0.05)

