# uses https://github.com/ultrabug/uhashring

# from uhashring import HashRing

from lb_logic import LBLogic
import random
from stats.beamer_statistics_collector import StatisticsCollector

class SimulationLogic(LBLogic):
    def __init__(self, args):
        super(SimulationLogic, self).__init__(args)
        connection_target = args.connection_target
        update_rate = args.update_rate
        end_time = args.end_time
        server_number = args.server_number
        bucket_number = args.bucket_number
        threshold = connection_target / server_number * 0.9
        collector = StatisticsCollector(args)

        self.threshold = threshold
        self.collector = collector
        self.imbalance = 0 #
        self.count_imbalance = 0
        self.average_load = 0
        self.prin_count = 0
        self.max_imba = 0
        self.ave_imba = 0
        self.flag = False

    def addNewConnection(self, packet):
        server_ID = self.pick_server(packet)
        self.server_dictionary[server_ID].append(packet.getHeader())
        self.connection_dictionary[packet.getHeader()] = server_ID
        self.collector.total_con += 1

    def removeConnection(self, packet):
        serverID = self.connection_dictionary[packet.getHeader()]
        self.server_dictionary[serverID].remove(packet.getHeader())

    def calculateLoad(self):
        self.prin_count += 1
        for i in range(self.number_of_servers):
            self.server_load[i] = len(self.server_dictionary[i])
        self.average_load = sum(self.server_load.values()) / self.number_of_servers
        if self.average_load > self.threshold:
            self.flag = True

        if self.flag:
            self.count_imbalance += 1
            sorted_load = sorted(self.server_load.items(), key=lambda item: item[1])
            self.imbalance += float(sorted_load[-1][1]) / self.average_load
            if self.max_imba < float(sorted_load[-1][1]) / self.average_load:
                self.max_imba = float(sorted_load[-1][1]) / self.average_load
            self.ave_imba = float(self.imbalance) / self.count_imbalance
            self.collector.ave_imba = self.ave_imba
            self.collector.max_imba = self.max_imba
            if self.prin_count % 30000 == 0:
                print ('imbalance is ' + str(float(sorted_load[-1][1]) / self.average_load))
                print ('average imbalance is ' + str(self.ave_imba))
                print ("max imbalance is " + str(self.max_imba))

class LeastServerLB(SimulationLogic):

    def __init__(self, args):
        super(LeastServerLB, self).__init__(args)

    def pick_server(self, packet):
        self.calculateLoad()
        # print ("the min load server is " + str(min(self.server_load,key=self.server_load.get)))
        return min(self.server_load,key=self.server_load.get)

class RoundRobinLB(SimulationLogic):
    def __init__(self, args):
        super(RoundRobinLB, self).__init__(args)
        self.robin_counter = 0

    def pick_server(self, packet):
        self.calculateLoad()
        server_ID = self.robin_counter
        self.robin_counter = (self.robin_counter + 1) % self.number_of_servers
        return server_ID


class HashBasedLB(SimulationLogic):
    def __init__(self, args):
        super(HashBasedLB, self).__init__(args)
        self.number_of_buckets = args.bucket_number  # self.connection_2_bucket = {}
        self.server_and_hash = {x: [] for x in range(self.number_of_servers)}
        self.hash_dictionary = {x: [[], []] for x in range(self.number_of_buckets)}
        for i in range(self.number_of_buckets):
            index = i * self.number_of_servers / self.number_of_buckets
            self.hash_dictionary[i][0] = [index]
            self.server_and_hash[index].append(i)

    def addNewConnection(self, packet):
        bucket_id, server_id = self.pick_server(packet)
        self.hash_dictionary[bucket_id][0].append(packet.getHeader())
        self.connection_dictionary[packet.getHeader()] = [bucket_id, self.hash_dictionary[bucket_id][0][0]]
        self.server_dictionary[server_id].append(packet.getHeader())
        self.collector.total_con += 1

    def removeConnection(self, packet):
        if self.connection_dictionary[packet.getHeader()]:
            [hash_val, serverID] = self.connection_dictionary[packet.getHeader()]
            self.server_dictionary[serverID].remove(packet.getHeader())
            if self.hash_dictionary[hash_val][0][0] == serverID:
                self.hash_dictionary[hash_val][0].remove(packet.getHeader())
            else:
                self.hash_dictionary[hash_val][1].remove(packet.getHeader())
        del self.connection_dictionary[packet.getHeader()]

    def pick_server(self, packet):
        self.calculateLoad()
        hash_val = hash(packet.getHeader()) % self.number_of_buckets
        server_id = self.hash_dictionary[hash_val][0][0]
        return hash_val, server_id

class PowerOfTwoLB(HashBasedLB):
    def __init__(self, args):
        super(PowerOfTwoLB, self).__init__(args)

    def pick_server(self, packet):
        hash_1 = hash(packet.getHeader() + '0') % self.number_of_buckets
        hash_2 = hash(packet.getHeader() + '1') % (self.number_of_buckets - 1)
        if hash_2 >= hash_1:
            hash_2 += 1
        server_id1 = self.hash_dictionary[hash_1][0][0]
        server_id2 = self.hash_dictionary[hash_2][0][0]

        if self.server_load[server_id1] > self.server_load[server_id2]:
            return hash_2, server_id2
        else:

            return hash_1, server_id1




