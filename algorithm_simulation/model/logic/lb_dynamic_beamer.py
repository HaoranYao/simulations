from lb_logic import LBLogic
from stats.beamer_statistics_collector import DynamicBeamerCollecter

class DynamicBeamer(LBLogic):
    def __init__(self, args):
        super(DynamicBeamer, self).__init__(args)
        self.Imbalance_threshold = args.Imbalance_threshold
        self.converge_count = 0
        self.bucket_timeset = {}
        self.number_of_buckets = args.bucket_number  # self.connection_2_bucket = {}
        self.least_loaded_server = 0
        self.server_and_hash = {x: [] for x in range(self.number_of_servers)}
        self.origin_server_and_hash = {x: [] for x in range(self.number_of_servers)}
        self.hash_dictionary = {x: [[], []] for x in range(self.number_of_buckets)}
        self.bucket_timeset = {}
        self.average_load = 0
        self.converge_list = []
        for i in range(self.number_of_buckets):
            self.bucket_timeset[i] = 0
            index = i * self.number_of_servers / self.number_of_buckets
            self.hash_dictionary[i][0] = [index]
            self.server_and_hash[index].append(i)
            self.origin_server_and_hash[index].append(i)
            self.bucket_timeset[i] = 0
        self.balancing_servers = {}
        self.threshold = 0
        self.flag = False
        self.long_connection = []
        self.print_count = 0
        self.collector = DynamicBeamerCollecter(args)

    def addNewConnection(self, packet):
        hash_val = hash(packet.getHeader()) % self.number_of_buckets
        self.hash_dictionary[hash_val][0].append(packet.getHeader())
        self.connection_dictionary[packet.getHeader()] = [hash_val, self.hash_dictionary[hash_val][0][0]]
        self.server_dictionary[self.hash_dictionary[hash_val][0][0]].append(packet.getHeader())
        self.collector.total_con += 1
        self.collector.current_connection += 1
        self.load_calucation(hash_val)

    def removeConnection(self, packet):
        if self.connection_dictionary[packet.getHeader()]:
            self.collector.current_connection -= 1
            [hash_val, serverID] = self.connection_dictionary[packet.getHeader()]
            self.server_dictionary[serverID].remove(packet.getHeader())
            if self.hash_dictionary[hash_val][0][0] == serverID:
                self.hash_dictionary[hash_val][0].remove(packet.getHeader())
            else:
                self.hash_dictionary[hash_val][1].remove(packet.getHeader())

            if serverID in self.balancing_servers.keys():
                self.del_load_calculation(serverID)
        del self.connection_dictionary[packet.getHeader()]



    def del_load_calculation(self, server_id):
        for i in range(self.number_of_servers):
            self.server_load[i] = len(self.server_dictionary[i])
        total_load = {key: value for key, value in self.server_load.items() if
                      key not in self.balancing_servers}
        self.average_load = sum(total_load.values()) / (self.number_of_servers - len(self.balancing_servers))
        if self.server_load[server_id] < self.average_load and server_id in self.balancing_servers.keys():
            bucket_to_be_return = self.balancing_servers[server_id][:]
            for each_bucket in bucket_to_be_return:
                self.Moving(each_bucket, server_id)
            del self.balancing_servers[server_id]

    def Moving(self, hash_val, newserver):
        connections_in_previous_server = self.hash_dictionary[hash_val][1][1:]
        current_server = self.hash_dictionary[hash_val][0][0]

        if connections_in_previous_server !=[] :
            previous_server = self.hash_dictionary[hash_val][1][0]


        self.server_and_hash[current_server].remove(hash_val)
        self.server_and_hash[newserver].append(hash_val)
        self.hash_dictionary[hash_val][1] = self.hash_dictionary[hash_val][0]
        self.hash_dictionary[hash_val][0] = [newserver]
        if connections_in_previous_server !=[] :
            for each_connection in connections_in_previous_server:
                if each_connection not in self.long_connection and previous_server != newserver:
                    self.collector.unnecessary_move_count += 1

                    self.long_connection.append(each_connection)
                self.hash_dictionary[hash_val][0].append(each_connection)
                self.connection_dictionary[each_connection]=[hash_val,newserver]
                # print (each_connection)
                self.server_dictionary[previous_server].remove(each_connection)
                self.server_dictionary[newserver].append(each_connection)

    def load_calucation(self, current_hash_val):
        for i in range(self.number_of_servers):
            self.server_load[i] = len(self.server_dictionary[i])
        total_load = {key: value for key, value in self.server_load.items() if
                                  key not in self.balancing_servers}
        self.average_load = sum(total_load.values()) / (self.number_of_servers - len(self.balancing_servers))
        sorted_load = sorted(self.server_load.items(), key=lambda item: item[1])

        # server_id is the is of the server with maximum load
        server_id = sorted_load[-1][0]
        if self.average_load > self.threshold:
            self.flag = True
        if self.flag and self.server_load[server_id] > (self.average_load) *self.Imbalance_threshold and server_id not in self.balancing_servers.keys() :
            self.balancing_servers[server_id] = self.origin_server_and_hash[server_id][:]
            buckets_to_move = self.balancing_servers[server_id][:]
            for each_bucket in buckets_to_move:
                unbalancing_servers = {key: value for key, value in self.server_and_hash.items() if
                                       key not in self.balancing_servers}
                sort_servers = sorted(unbalancing_servers.items(), key=lambda x: len(x[1]))
                target_server = sort_servers[0][0]
                if target_server == server_id:
                    target_server = sort_servers[1][0]
                self.Moving(each_bucket, target_server)
                self.collector.moving_bucket += 1


        self.converge_print()


    def converge_print(self):
        self.converge_list.append(float(self.collector.unnecessary_move_count)/self.collector.total_con)
        # self.collector.conclusion()



