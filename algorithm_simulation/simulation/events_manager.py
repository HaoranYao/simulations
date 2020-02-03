import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.insert(0, dir_path)

import math
import random
import util.util
import numpy as np
from  heapq import heappush, heappop
class EventsManager():

    def __init__(self, connection_cdf, update_cdf, update_rate, connection_target, average_connection_time, connection_size_cdf, enable_updates, seed, cluster_size = 10):
        self.connection_cdf = connection_cdf
        self.update_cdf = update_cdf
        self.update_rate = update_rate
        self.connection_target = connection_target
        self.connection_rate = connection_target/average_connection_time
        self.connection_size_cdf = connection_size_cdf
        self.random = random.Random(seed)
        self.cluster_size = cluster_size
        if not enable_updates:
            self.events = [(0,"new-conn 0")]
        else:  
            self.events = [(0,"new-conn 0"), (0,"new-up 1")] 
        self.counter_on_demand = 2

    def next(self):
        time, event = heappop(self.events)
        event_type = event.split(" ")[0]
        conn_id = event.split(" ")[1]
        #print(str(time) + " " + str(event) + " " + str(len(self.events)))
        if event_type == "new-conn":
            connection_ends = util.util.getCDFValue(self.connection_cdf, self.random.random())
            heappush(self.events,(time+connection_ends, "del-conn " + str(conn_id) ))
            connection_next = -math.log(1-self.random.random(), math.e) / self.connection_rate
            heappush(self.events,(time + connection_next,  "new-conn " + str(self.counter_on_demand)))
            self.counter_on_demand += 1
        elif event_type == "new-up":
            update_ends = util.util.getCDFValue(self.update_cdf, self.random.random())
            heappush(self.events,(time+update_ends, "del-up " + str(conn_id)))
            update_next = -math.log(1 - self.random.random(), math.e)/ (self.update_rate/60)
            heappush(self.events,(time + update_next, "new-up " + str(self.counter_on_demand)))
            self.counter_on_demand += 1
        return (time, event)
            
