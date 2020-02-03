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

from matplotlib import use, rc
use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# plot saving utility function
def writeout(filename_base, tight=True):
  for fmt in ['pdf']:
    if tight:
      plt.savefig("%s.%s" % (filename_base, fmt), format=fmt, bbox_inches='tight')
    else:
      plt.savefig("%s.%s" % (filename_base, fmt), format=fmt)


def append_or_create(d, i, e):
  if not i in d:
    d[i] = [e]
  else:
    d[i].append(e)

def add_or_create(d, i, e):
  if not i in d:
    d[i] = e
  else:
    d[i] = d[i] + e

paper_figsize_small = (1.1, 1.1)
paper_figsize_small_square = (1.5, 1.5)
paper_figsize_medium = (2, 1.33)
paper_figsize_medium_square = (2, 2)
#paper_figsize_medium = (1.66, 1.1)
paper_figsize_large = (3.33, 2.22)
paper_figsize_bigsim3 = (2.4, 1.7)

#8e053b red
#496ee2 blue
#ef9708 orange
paper_colors = ['#496ee2', '#8e053b', 'g', '#ef9708', '0', '#eeefff', '0.5', 'c', '0.7']

# -----------------------------------

def think_time_fn(x, y, s):
  return x + y * s

# -----------------------------------

def get_mad(median, data):
  devs = [abs(x - median) for x in data]
  mad = np.median(devs)
  return mad

# -----------------------------------
