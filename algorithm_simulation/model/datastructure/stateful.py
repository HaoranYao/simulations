
from lb_data_structure import LBDataStructure


class Stateful(LBDataStructure):
    connections = {}

    def newPacketMapping(self,packet, server):
        self.connections[packet.getHeader()] = server

    def removeMapping(self,packet):
        del self.connections[packet.packet.getHeader()]

    def getNextHop(self, packet):
        return self.connections[packet.getHeader()]