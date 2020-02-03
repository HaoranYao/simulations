#!/bin/bash

workdir=$(cd $(dirname $0); pwd)
cd ${workdir}



for rate in 0.5,0.75,1;do
    echo $rate
    touch $rate
    #python simulation/compare.py data/hadoop_cdf.txt 1000 data/downtime_upgrade_cdf.txt $rate data/hadoop_size_cdf 100 3
done
