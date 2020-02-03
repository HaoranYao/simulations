# uses https://github.com/ultrabug/uhashring

from uhashring import HashRing

from lb_logic import LBLogic
from stats.beamer_statistics_collector import DipCollector

class LbDip(LBLogic):

    def __init__(self, args):
        super(LbDip, self).__init__(args)
        self.nodes_names = [x for x in range(0,self.number_of_servers)]
        self.collector = DipCollector(args)
        self.hr = HashRing(nodes=self.nodes_names,vnodes=args.vnodes) #TODO modify vnodes
        self.connection_2_bucket = {}
        self.past_connection = {} # dictionay, used to record the bucket that each connection connected to, find connections are moved unnecessarily
        self.server_2_buckets_connections = {x: {} for x in self.hr.get_nodes()}

        for bucket_id, node in self.hr.get_points():
            self.server_2_buckets_connections[node][bucket_id] = []

    def addNewConnection(self, packet):
        bucket_id = self.hr.get_server(packet.getHeader())
        serverID = bucket_id[1]
        bucketID = bucket_id[0]
        # bucket_id[1] is serverID, bucket_id[0] is the bucket
        self.past_connection[packet.getHeader()] = [serverID]
        self.collector.total_con += 1
        self.collector.current_connection += 1
        self.connection_2_bucket[packet.getHeader()] = bucket_id # add bucket for that connection
        self.server_2_buckets_connections[serverID][bucketID].append(packet.getHeader()) # add connection on that bucket
        self.collector.conclusion()
    def removeConnection(self,packet):
        bucket_id = self.connection_2_bucket[packet.getHeader()]
        self.collector.current_connection -= 1
        del self.connection_2_bucket[packet.getHeader()] # remove bucket for that connection
        del self.past_connection[packet.getHeader()]
        self.server_2_buckets_connections[bucket_id[1]][bucket_id[0]].remove(packet.getHeader()) #remove connection on that bucket

    def addServer(self, serverId):
        if serverId in self.nodes_names:
            return
        self.nodes_names.append(serverId)
        all_connections = []
        for D2value in self.server_2_buckets_connections.itervalues():
            for D1value in D2value.itervalues():
                all_connections += D1value
        self.hr.add_node(serverId) # change the hash function

        for each_connection in all_connections:
            new_bucket_id = self.hr.get_server(each_connection)
            old_bucket_id = self.connection_2_bucket[each_connection]
            if  str(old_bucket_id) != str(new_bucket_id):
                if  new_bucket_id[1] not in self.past_connection[each_connection]:
                    self.past_connection[each_connection].append(new_bucket_id[1])
                else:
                    temp_index = self.past_connection[each_connection].index(new_bucket_id[1])
                    self.past_connection[each_connection] = self.past_connection[each_connection][:temp_index+1]
                self.collector.unnecessary_move_count += 1
                self.server_2_buckets_connections[new_bucket_id[1]][new_bucket_id[0]].append(each_connection) # add connection on that bucket
                self.connection_2_bucket[each_connection] = new_bucket_id # change bucket for that connection
                self.server_2_buckets_connections[old_bucket_id[1]][old_bucket_id[0]].remove(each_connection) # delete connection on old bucket

    def removeServer(self, serverId):
        if serverId not in self.nodes_names:
            return
        self.nodes_names.remove(serverId)
        buckets_to_be_removed = self.server_2_buckets_connections[serverId]
        all_previous_connections=[]

        for bucket in self.server_2_buckets_connections[serverId]:
            for each_connection in self.server_2_buckets_connections[serverId][bucket]:
                all_previous_connections.append(each_connection)
        self.hr.remove_node(serverId)
        for each_connection in all_previous_connections:
            new_bucket = self.hr.get_server(each_connection)[0]
            new_serverID =self.hr.get_server(each_connection)[1]
            self.past_connection[each_connection].append(new_serverID)
            self.server_2_buckets_connections[new_serverID][new_bucket].append(each_connection)
            self.connection_2_bucket[each_connection] = (new_bucket,new_serverID)
        for each_bucket in buckets_to_be_removed:
            self.server_2_buckets_connections[serverId][each_bucket] = []

class LbDipChain(LbDip):

    def __init__(self, args):
        super(LbDipChain, self).__init__(args)

    def addNewConnection(self, packet):
        bucket_id = self.hr.get_server(packet.getHeader())
        serverID = bucket_id[1]
        bucketID = bucket_id[0]
        # bucket_id[1] is serverID, bucket_id[0] is the bucket
        self.past_connection[packet.getHeader()] = [serverID,'']
        self.collector.total_con += 1
        self.collector.current_connection += 1
        self.connection_2_bucket[packet.getHeader()] = bucket_id # add bucket for that connection
        self.server_2_buckets_connections[serverID][bucketID].append(packet.getHeader()) # add connection on that bucket
        self.collector.conclusion()
    def addServer(self, serverId):
        if serverId in self.nodes_names:
            return
        self.nodes_names.append(serverId)
        all_connections = []
        for D2value in self.server_2_buckets_connections.itervalues():
            for D1value in D2value.itervalues():
                all_connections += D1value
        self.hr.add_node(serverId)

        for each_connection in all_connections:
            new_bucket_id = self.hr.get_server(each_connection)
            old_bucket_id = self.connection_2_bucket[each_connection]
            if  str(old_bucket_id) != str(new_bucket_id):
                if self.past_connection[each_connection][1] != '':
                    self.collector.unnecessary_move_count += 1
                self.past_connection[each_connection] = [new_bucket_id[1], old_bucket_id[1]]
                self.server_2_buckets_connections[new_bucket_id[1]][new_bucket_id[0]].append(each_connection) # add connection on that bucket
                self.connection_2_bucket[each_connection] = new_bucket_id # change bucket for that connection
                self.server_2_buckets_connections[old_bucket_id[1]][old_bucket_id[0]].remove(each_connection) # delete connection on old bucket

    def removeServer(self, serverId):
        if serverId not in self.nodes_names:
            return
        self.nodes_names.remove(serverId)
        buckets_to_be_removed = self.server_2_buckets_connections[serverId]
        all_connections = []
        for D2value in self.server_2_buckets_connections.itervalues():
            for D1value in D2value.itervalues():
                all_connections += D1value
        self.hr.remove_node(serverId)

        for each_connection in all_connections:
            new_bucket_id = self.hr.get_server(each_connection)
            old_bucket_id = self.connection_2_bucket[each_connection]
            if str(old_bucket_id) != str(new_bucket_id):
                self.past_connection[each_connection] = [new_bucket_id[1],'']
                self.server_2_buckets_connections[new_bucket_id[1]][new_bucket_id[0]].append(each_connection) # add connection on that bucket
                self.connection_2_bucket[each_connection] = new_bucket_id # change bucket for that connection
                self.server_2_buckets_connections[old_bucket_id[1]][old_bucket_id[0]].remove(each_connection) # delete connection on old bucket
            elif serverId == self.past_connection[each_connection][1]:
                self.past_connection[each_connection][1] = ''

