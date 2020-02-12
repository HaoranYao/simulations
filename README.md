# Python simulation
This is the code for the python simulation in "A High-Speed Load-Balancer Design with Guaranteed Per-Connection-Consistency" Section 2.
With this code, you can re-run all the python simulations. In general, this simulation contains 3 sub-simulations.  
  - Simulations for counting broken connections with DIP updates.
  - Simulations for observing average imbalance for existing load balancers. 
  - Simulations for counting broken connections in dynamic beamer.

### Simulation Method
This is a simulation in the connection level. We did not consider the details of the packets transmission. We just care 
about the start and end time of each connection.

The "events_manager" will generate events such as "new connection" based on 
the CDF fies in ```cheetah-experiments/algorithm_simulation/data```.

Each connection will be sent to the corresponding server according to the 
load balance logic in ```cheetah-experiments/algorithm_simulation/model/logic```.

The status of each server will be collected by the collector in ```cheetah-experiments/algorithm_simulation/model/stats```.


### Environment requirement
 - python 2.7
 - install uhashring using pip


### How to use

Enter the <algorithm_simulation/> folder:
```sh
$ cd algorithm_simulation/ 
```
The main function for this simulation is <compare.py> python file in <./simulation>.
You can see the help information with "-h" command:
```sh
$ python simulation/compare.py  -h 
```

### Basic Settings:
- ```-M``` or ```--model``` to choose the simulation model. For now, we have the simulation codes for these scenarios:
  - ```-M dip``` to run the simulation for counting broken connections with DIP updates. We do not use the daisy-chaining in this case.
  - ```-M dip_chain``` to run the simulation for counting broken connections with DIP updates. We use the daisy-chaining in this case.
  - ```-M load_imba_round``` to run the simulation for observing average imbalance for Round Robin load balancer.
  - ```-M load_imba_least``` to run the simulation for observing average imbalance for the least loaded balancer.
  - ```-M load_imba_hash``` to run the simulation for observing average imbalance for hash-beamer load balancer.
  - ```-M load_imba_power2``` to run the simulation for observing average imbalance for power-of-two load balancer.
  - ```-M dy_beamer``` to run the simulation for counting broken connections in dynamic beamer.
 
- ```-c``` or ```–connection_cdf_file``` to set the location of the connection cdf file. The default value is ```data/hadoop_cdf.txt```.
- ```-cs``` or ```–connection_size_cdf_file``` to set the location of connection size cdf file. The default value is ```data/hadoop_size_cdf```.
- ```-t``` or ```–connection_target``` to set the number of connection targets. The default value is ```10000```.
- ```-e``` or ```–end_time``` to set time duration of the simulation. The default value is ```30000```.
- ```-ns``` or ```–server_number``` to set the number of servers. The default value is ```468```.
- ```-nb``` or ```–bucket_number``` to set the number of buckets. The default value is ```468```.
- ```-sd``` or ```–seed``` to set the random seed. The default value is ```1```.

### Specific Settings for Different simulations
If you want to run simulations for counting broken connections with DIP updates.
You mush set:


- ```-en``` or ```–enable_updates``` to ```True``` to enable the DIP updates. The default value is ```False```.

Then you can use:


- ```-u``` or ```–update_cdf_file``` to set the location of the update cdf file. The default value is ```data/downtime_upgrade_cdf.txt```.
- ```-v``` or ```–vnodes``` to set the number of v-nodes in the hash ring. The default value is ```30```.
- ```-ur``` or ```–update_rate``` to set the number of updates per minute. The default value is ```10```.

If you want to run simulations for counting broken connections in dynamic beamer.
You can use:
- ```-th``` or ```–Imbalance_threshold``` to set the imbalance threshold. The default value is ```1.2```.

### Examples
- An example of simulations for counting broken connections with DIP updates:

```$ python simulation/compare.py  -M dip -e 10000 -t 20000 -ns 468 -en True```

- An example of simulations for observing average imbalance for existing load balancers: 

```$ python simulation/compare.py  -M load_imba_round -e 10000 -t 70000```

- An example of simulations for counting broken connections in dynamic beamer:

```$ python simulation/compare.py  -M dy_beamer -e 30000 -t 70000 -th 1.5```

### Results
The result is contained in ```cheetah-experiments/algorithm_simulation/stats/report.csv```.
All of the results are written in this csv file. The format is:

model,connection_target,end_time,server_number,update_rate,bucket_number,imbalance_threshold,total_connections,broken_connections,broken_rate,max_imbalance,ave_imbalance

The non-existent value will be represented as ```None```.

### Ploting
Results of our previous simulations can be found at ```cheetah-experiments/algorithm_simulation/stats/report.csv```. 

To generate the graphs:
- ```$ cd algorithm_simulation/stats```
- ```$ python 01-plot-dip.py``` to plot the graph of connections broken rate in DIP Updates experiment.
- ```$ python 02-plot-imbalance.py``` to plot the graph of average imbalance in Imbalance experiment.
- ```$ python 03-plot-moving-buckets.py``` to plot the graph of moving buckets rate in dynamic beamer experiment.
- ```$ python 04-plot-broken-connections.py``` to plot the graph of connections broken rate in dynamic beamer experiment.


### Acknowledgement
This python simulation is built from the prototype provided by Marco.

