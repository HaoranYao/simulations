import os
import argparse
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.insert(0, dir_path)
import json
from events_manager import EventsManager
from model.packet import Packet
#from model.logic.lb_consistent_hashing import LBConsistentHashing
from model.logic.lB_no_updates import *
from model.logic.lb_dynamic_beamer import DynamicBeamer
from model.logic.lb_dip import *

from model.datastructure.beamer import Beamer

import util.util

class Compare():

    def __init__(self, connection_cdf, update_cdf_file, update_rate, connection_target, average_connection_time, connection_size_cdf, enable_updates, seed):
        self.events_manager = EventsManager(connection_cdf, update_cdf_file, update_rate, connection_target, average_connection_time, connection_size_cdf, enable_updates, seed)

    def setLBLogic(self,lblogic):
        self.lblogic = lblogic

    def setLBDataStructure(self,lbdatastructure):
        self.lbdatastructure = lbdatastructure

    def start_simulation(self, end_time, server_number, en_updates, model):
        events = []
        print_i = 1
        time,event = self.events_manager.next()
        while True:
            if time > end_time:
                break
            if (model == "dy_beamer") and (time > 60 * print_i):
                print_i += 1
                self.lblogic.collector.conclusion()

            event_type = event.split(" ")[0]
            conn_id = event.split(" ")[1]
            #print("event: " + str(time) + " " + str(event))
            if event_type == "new-conn":
                packet = Packet(0,0,0,conn_id)
                self.lblogic.addNewConnection(packet)
            elif event_type == "del-conn":
                packet = Packet(0, 0, 0, conn_id)
                self.lblogic.removeConnection(packet)
            if en_updates:
                if event_type == "new-up":
                    self.lblogic.removeServer(int(conn_id)%server_number) #need to know the number of server
                    pass
                elif event_type == "del-up":
                    self.lblogic.addServer(int(conn_id)%server_number)
            time,event = self.events_manager.next()
        print("printing statistics")
        self.lblogic.collector.conclusion()

if __name__ == "__main__":
    def boolean_string(s):
        if s not in {'False', 'True'}:
            raise ValueError('Not a valid boolean string')
        return s == 'True'

    parser = argparse.ArgumentParser()
    parser.description = 'please enter simulation parameters ...'
    parser.add_argument("-c", "--connection_cdf_file", help="location of connection cdf file", dest="connection_cdf_file", default="data/hadoop_cdf.txt")
    parser.add_argument("-t", "--connection_target", help="number of connection target", type=float, dest="connection_target", default="10000")
    parser.add_argument("-u", "--update_cdf_file", help="location of update cdf file", dest="update_cdf_file", default="data/downtime_upgrade_cdf.txt")
    parser.add_argument("-ur", "--update_rate", help="the update rate", type=float, dest="update_rate", default="10")
    parser.add_argument("-cs", "--connection_size_cdf_file", help="location of connection size cdf file", dest="connection_size_cdf_file", default="data/hadoop_size_cdf")
    parser.add_argument("-e", "--end_time", help="end time", type=float, dest="end_time", default="30000")
    parser.add_argument("-ns", "--server_number", help="number of servers", type=int, dest="server_number", default="468")
    parser.add_argument("-nb", "--bucket_number", help="number of buckets", type=int, dest="bucket_number", default="468")
    parser.add_argument("-th", "--Imbalance_threshold", help="the imbalance threshold", type=float, dest="Imbalance_threshold", default="1.2")
    parser.add_argument("-en", "--enable_updates", help="enable server update?", type=boolean_string, dest="enable_updates", default=False)
    parser.add_argument("-sd", "--seed", help="random seed", type=int, dest="seed", default="1")
    parser.add_argument("-M", "--model", help="choose the simulation model", dest="model",
                        default="load_imba_round")
    parser.add_argument("-v", "--vnodes", help="number of vnodes in hash ring", type=int, dest="vnodes",
                        default="30")
    args = parser.parse_args()
    connection_cdf_file = args.connection_cdf_file
    connection_target = args.connection_target
    update_cdf_file = args.update_cdf_file
    update_rate = args.update_rate
    connection_size_cdf_file = args.connection_size_cdf_file
    end_time = args.end_time
    server_number = args.server_number
    bucket_number = args.bucket_number
    Imbalance_threshold = args.Imbalance_threshold
    enable_updates = args.enable_updates
    seed = args.seed
    model = args.model

    with open(connection_cdf_file) as json_file:
        connection_cdf = json.load(json_file)

    with open(update_cdf_file) as json_file:
        update_cdf = json.load(json_file)

    with open(connection_size_cdf_file) as json_file:
        connection_size_cdf = json.load(json_file)

    print str(connection_cdf)
    print str(update_cdf)
    print str(connection_size_cdf)
    average_connection_time = util.util.getCDFAverage(connection_cdf)#change from ms to second
    print("average_connection_time: " + str(average_connection_time))
    connection_rate = connection_target/average_connection_time
    print("connection_rate: " + str(connection_rate))
    simulation = Compare(connection_cdf, update_cdf, update_rate, connection_target, average_connection_time, connection_size_cdf, enable_updates, seed)

    if (model == "load_imba_round"):
        print ("Run load imbalance simulation for Round Robin Algorithm")
        simulation.setLBLogic(RoundRobinLB(args))
    elif (model == "load_imba_least"):
        print ("Run load imbalance simulation for Least Loaded Algorithm")
        simulation.setLBLogic(LeastServerLB(args))
    elif (model == "load_imba_hash"):
        print ("Run load imbalance simulation for Hash Based Algorithm")
        simulation.setLBLogic(HashBasedLB(args))
    elif (model == "load_imba_power2"):
        print ("Run load imbalance simulation for Power of Two Algorithm")
        simulation.setLBLogic(PowerOfTwoLB(args))
    elif (model == "dy_beamer"):
        print ("Run dynamic beamer simulation")
        simulation.setLBLogic(DynamicBeamer(args))
    elif (model == "dip"):
        print ("Run DIP updates simulation without daisy chain")
        simulation.setLBLogic(LbDip(args))
    elif (model == "dip_chain"):
        print ("Run DIP updates simulation with daisy chain")
        simulation.setLBLogic(LbDipChain(args))
    simulation.start_simulation(end_time, server_number, enable_updates, model)

