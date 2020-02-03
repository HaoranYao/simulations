import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import os
from matplotlib import container
from common import *
from collections import OrderedDict
import pandas
from matplotlib.markers import MarkerStyle
import sys
import matplotlib

matplotlib.rc('figure', figsize=(6, 3.5))

prefix = "cyclescompare_req/"
series = ["Stateful_100K", "Stateful_1M", "Stateful_10M", "Cheetah_Stateful_1M", "Cheetah_Stateful_10M", "Cheetah_Stateless", "Hash_DPDK", "Hash_RSS" ]
labels = [s.replace("_"," ") for s in series]
labels[-2] = "Hash (SW)"
labels[-1] = "Hash (HW)"

c_stateful = graphcolor[0]
c_cheetah = graphcolor[8]
c_cheetah_stateful = graphcolor[4]
c_hash = graphcolor[2]
colors = [shade(c_stateful,0,3), shade(c_stateful,1,3), shade(c_stateful,2,3), shade(c_cheetah_stateful,0,2), shade(c_cheetah_stateful,1,2), shade(c_cheetah,0,1), shade(c_hash,0,3), shade(c_hash,1,3), shade(c_hash,2,3) ]

markers = [ "o", "o", "o", "d", "d", "D", "*", "*", "*" ]

lines = ["-","-","-","-","-","--","--","--","--","--","--"]

data = []
nbreq = []
for serie in series:
  try:
    f = prefix + serie + "LB_CYCLESPP.csv"
    data.append(pandas.read_csv(f, sep=" ", header=None, usecols=range(10)).to_numpy())
    f = prefix + serie + "REQUEST.csv"
    nbreq.append(pandas.read_csv(f, sep=" ", header=None, usecols=range(10)).to_numpy())
  except Exception as e:
    print("Could not read %s" % serie)
    print(e)
    print("%s:" % f)
    print(open(f, "r").readlines())

for i,serie in enumerate(series):
  try:
    x=data[i][:,0]
    y=data[i][:,1:]

    req=nbreq[i][:,1] * 1445
    diff = np.nanmedian(y,axis=1) / np.nanmedian(data[4][:,1:],axis=1)
    #print(serie,diff,np.max(diff) )
    mask = (x - req) < (0.01 * req)
    drop = (x - req) >= (0.01 * req)
    drop = [ (drop[i] or (mask[i - 1] if i > 0 else False)) for i in range(len(drop)) ]

    mean = True
    if mean:
        yv = np.nanmean(y,axis=1)
        errn = np.nanstd(y,axis=1)
        errp = np.nanstd(y,axis=1)
    else:
        yv = np.nanmedian(y,axis=1)
        errn = np.nanpercentile(y,75,axis=1) - yv
        errp = yv - np.nanpercentile(y,25,axis=1)

    plt.errorbar(x[mask],y=yv[mask],yerr=(errp[mask],errn[mask]),label=labels[i],marker=markers[i],color=colors[i],linestyle=lines[i])
    plt.errorbar(x[drop],y=yv[drop],yerr=(errp[drop],errn[drop]),label=None, fillstyle="none",marker=markers[i],linestyle=':',color=colors[i])
  except Exception as e:
      print("While processing %s" % serie)
      print(e)
      continue

plt.legend(loc="lower center", bbox_to_anchor=(0.5,1),ncol=3)

ax = plt.gca()
ax.set_xscale("symlog")
ax.set_xticks(data[0][:,0])
ax.set_xlabel("Requests per seconds")
ax.set_ylabel("Cycles / packets")
ax.set_yscale("symlog")
ax.set_ylim(50)
ax.set_yticks([50,100,200,400,600])
ax.grid(axis="y")
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
def f(x,pos):
    return "%dK" % (x / 1000)

ax.xaxis.set_minor_formatter(ticker.NullFormatter())
ax.xaxis.set_major_formatter(ticker.FuncFormatter(f))

#"cyclescompare_req/Hash_DPDKLB_CYCLESPP.csv"


plt.tight_layout()

plt.savefig('cycles.pdf')
